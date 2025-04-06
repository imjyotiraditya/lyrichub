from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.config import settings
from api.genius.routes import router as genius_router
from api.spotify.routes import router as spotify_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url=None,
    redoc_url=None,
)

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def get_api_docs(request: Request):
    return templates.TemplateResponse(
        'docs.html',
        {
            'request': request,
            'title': settings.PROJECT_NAME,
            'description': settings.PROJECT_DESCRIPTION,
            'version': settings.VERSION,
        },
    )


app.include_router(spotify_router, prefix='/api/spotify')
app.include_router(genius_router, prefix='/api/genius')
