from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'LyricHub'
    PROJECT_DESCRIPTION: str = 'A centralized API hub for retrieving lyrics from multiple music platforms'
    VERSION: str = '1.0.0'

    SPOTIFY_DC: str = ''
    GENIUS_ACCESS_TOKEN: str = ''

    class Config:
        env_file = '.env'


settings = Settings()

if not settings.GENIUS_ACCESS_TOKEN:
    print('WARNING: GENIUS_ACCESS_TOKEN environment variable not set.')

if not settings.SPOTIFY_DC:
    print('WARNING: SPOTIFY_DC environment variable not set.')
