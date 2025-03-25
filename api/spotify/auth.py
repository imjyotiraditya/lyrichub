import hashlib
import hmac
import time

import httpx

from api.config import settings
from api.core.errors import ServiceError

SPOTIFY_TOKEN_URL = 'https://open.spotify.com/get_access_token'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/138.0'


def generate_totp() -> str:
    secret_values = [
        12,
        56,
        76,
        33,
        88,
        44,
        88,
        33,
        78,
        78,
        11,
        66,
        22,
        22,
        55,
        69,
        54,
    ]

    transformed = ''.join(
        str(value ^ ((index % 33) + 9))
        for index, value in enumerate(secret_values)
    )
    secret_bytes = transformed.encode('utf-8')

    algorithm = hashlib.sha1
    digits = 6
    period = 30

    counter = int(time.time() // period)
    counter_bytes = counter.to_bytes(8, byteorder='big')

    hmac_hash = hmac.new(secret_bytes, counter_bytes, algorithm).digest()

    offset = hmac_hash[-1] & 0x0F
    code = (
        (hmac_hash[offset] & 0x7F) << 24
        | (hmac_hash[offset + 1] & 0xFF) << 16
        | (hmac_hash[offset + 2] & 0xFF) << 8
        | (hmac_hash[offset + 3] & 0xFF)
    )

    code = code % (10**digits)
    return f'{code:0{digits}d}'


async def get_spotify_token() -> str:
    spotify_dc = settings.SPOTIFY_DC
    if not spotify_dc:
        raise ServiceError('SPOTIFY_DC environment variable not set')

    totp_code = generate_totp()
    params = {'productType': 'web-player', 'totp': totp_code, 'totpVer': '5'}
    headers = {
        'user-agent': USER_AGENT,
        'cookie': f'sp_dc={spotify_dc}',
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                SPOTIFY_TOKEN_URL, params=params, headers=headers
            )
            response.raise_for_status()
            data = response.json()

            if 'accessToken' not in data:
                raise ServiceError('Access token not found in response')

            return data['accessToken']

    except httpx.HTTPError as e:
        raise ServiceError(f'Error communicating with Spotify: {str(e)}')


def get_request_headers(token: str) -> dict:
    return {
        'User-Agent': USER_AGENT,
        'Accept': 'application/json',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://open.spotify.com/',
        'Authorization': f'Bearer {token}',
        'app-platform': 'WebPlayer',
        'spotify-app-version': '1.2.61.35.gecc15164',
        'Origin': 'https://open.spotify.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }
