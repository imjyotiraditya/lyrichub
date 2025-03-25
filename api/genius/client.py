import re
from typing import Any

import httpx

from api.config import settings
from api.core.errors import ServiceError

GENIUS_BASE_URL = 'https://api.genius.com'
GENIUS_SEARCH_URL = f'{GENIUS_BASE_URL}/search/song'


async def search_tracks(query: str) -> list[dict[str, Any]]:
    params = {'q': query}
    headers = {'Authorization': f'Bearer {settings.GENIUS_ACCESS_TOKEN}'}

    try:
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.get(
                GENIUS_SEARCH_URL, params=params, headers=headers
            )
            response.raise_for_status()
            data = response.json()

            if (
                'response' in data
                and 'sections' in data['response']
                and data['response']['sections']
            ):
                return data['response']['sections'][0]['hits']

            return []

    except httpx.HTTPError as e:
        raise ServiceError(f'Error searching Genius: {str(e)}')


async def fetch_lyrics(url: str) -> str:
    headers = {'Authorization': f'Bearer {settings.GENIUS_ACCESS_TOKEN}'}

    try:
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            lyrics_dom = data['response']['song']['lyrics']['dom']
            if not lyrics_dom:
                return 'No lyrics found for this track.'

            def extract_lyrics(dom_node: dict) -> str:
                lyrics = []

                for child in dom_node['children']:
                    if isinstance(child, str):
                        lyrics.append(child)
                    elif isinstance(child, dict):
                        if child['tag'] == 'br':
                            lyrics.append('\n')
                        else:
                            lyrics.append(extract_lyrics(child))

                lyrics_text = ''.join(lyrics).strip()
                lyrics_text = re.sub(r'\[.*?\]\n?', '', lyrics_text)
                lyrics_text = re.sub(r'\n{3,}', '\n\n', lyrics_text)

                return lyrics_text.strip()

            return extract_lyrics(lyrics_dom)

    except httpx.HTTPError as e:
        raise ServiceError(f'Error fetching lyrics from Genius: {str(e)}')


async def get_track_lyrics(query: str) -> dict[str, Any]:
    try:
        search_results = await search_tracks(query)

        if not search_results:
            return {'error': 'No tracks found on Genius for your search query.'}

        track = search_results[0]['result']

        result = {
            'title': track['title'],
            'artist': track['primary_artist']['name'],
            'cover': track['song_art_image_url'],
            'lyrics': 'Not Found.',
        }

        url = f'{GENIUS_BASE_URL}{track["api_path"]}'
        try:
            result['lyrics'] = await fetch_lyrics(url)
        except Exception:
            pass

        return result

    except Exception as e:
        return {'error': str(e)}
