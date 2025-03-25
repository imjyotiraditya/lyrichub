from fastapi import FastAPI

from api.config import settings
from api.genius.routes import router as genius_router
from api.spotify.routes import router as spotify_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url='/',
    redoc_url=None,
)

app.include_router(spotify_router, prefix='/api/spotify')
app.include_router(genius_router, prefix='/api/genius')
