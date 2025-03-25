import json
from typing import Any

import httpx

from api.core.errors import ServiceError
from api.spotify.auth import get_request_headers, get_spotify_token

SEARCH_URL = 'https://api-partner.spotify.com/pathfinder/v1/query'
LYRICS_URL = 'https://spclient.wg.spotify.com/color-lyrics/v2/track/'


async def search_tracks(query: str, limit: int = 20) -> list[dict[str, Any]]:
    token = await get_spotify_token()
    headers = get_request_headers(token)
    headers['content-type'] = 'application/json;charset=UTF-8'

    params = {
        'operationName': 'searchTracks',
        'variables': json.dumps(
            {
                'includePreReleases': False,
                'numberOfTopResults': limit,
                'searchTerm': query,
                'offset': 0,
                'limit': limit,
                'includeAudiobooks': True,
                'includeAuthors': False,
            }
        ),
        'extensions': json.dumps(
            {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': 'bc1ca2fcd0ba1013a0fc88e6cc4f190af501851e3dafd3e1ef85840297694428',
                }
            }
        ),
    }

    try:
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.get(
                SEARCH_URL, headers=headers, params=params
            )
            response.raise_for_status()
            data = response.json()

            if (
                'data' in data
                and 'searchV2' in data['data']
                and 'tracksV2' in data['data']['searchV2']
            ):
                return data['data']['searchV2']['tracksV2']['items']
            return []

    except httpx.HTTPError as e:
        raise ServiceError(f'Search error: {str(e)}')


async def fetch_lyrics(track_id: str) -> dict[str, Any]:
    token = await get_spotify_token()
    url = f'{LYRICS_URL}{track_id}'
    headers = get_request_headers(token)
    params = {'format': 'json', 'vocalRemoval': 'false', 'market': 'from_token'}

    try:
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as e:
        raise ServiceError(f'Error fetching lyrics: {str(e)}')


def format_lyrics(lyrics_data: dict[str, Any]) -> str:
    if not lyrics_data or 'lyrics' not in lyrics_data:
        return 'No lyrics found for this track.'

    if 'lines' not in lyrics_data['lyrics']:
        return 'No lyrics content found.'

    formatted_lines = []
    for line in lyrics_data['lyrics']['lines']:
        if not (line.get('startTimeMs') and line.get('words')):
            continue

        time_ms = int(line['startTimeMs'])
        seconds = time_ms / 1000
        minutes = int(seconds // 60)
        seconds_remainder = seconds % 60

        timestamp = f'[{minutes:02d}:{seconds_remainder:05.2f}]'
        formatted_lines.append(f'{timestamp}{line["words"]}')

    return '\n'.join(formatted_lines)


async def get_track_lyrics(query: str) -> dict[str, Any]:
    try:
        tracks = await search_tracks(query)

        if not tracks:
            return {'error': 'No tracks found for your search query.'}

        track = tracks[0]['item']['data']
        track_id = track['id']

        result = {
            'title': track['name'],
            'artist': track['artists']['items'][0]['profile']['name'],
            'cover': None,
            'lyrics': 'Not Found.',
        }

        if (
            'albumOfTrack' in track
            and 'coverArt' in track['albumOfTrack']
            and 'sources' in track['albumOfTrack']['coverArt']
        ):
            sources = track['albumOfTrack']['coverArt']['sources']
            if sources:
                result['cover'] = sources[-1]['url']

        try:
            lyrics_data = await fetch_lyrics(track_id)
            result['lyrics'] = format_lyrics(lyrics_data)
        except Exception:
            pass

        return result

    except Exception as e:
        return {'error': str(e)}
