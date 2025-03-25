from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse

from api.core.errors import NotFoundError, ServiceError
from api.core.schemas import ErrorResponse, LyricsResponse
from api.spotify.client import get_track_lyrics

router = APIRouter(tags=['Spotify'])


@router.get(
    '',
    response_model=LyricsResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': ErrorResponse},
    },
)
async def get_lyrics(
    query: str = Query(
        ..., description="Search query (e.g., 'song name artist')"
    ),
):
    try:
        result = await get_track_lyrics(query)

        if 'error' in result:
            raise NotFoundError(result['error'])

        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        raise ServiceError(f'Failed to retrieve lyrics: {str(e)}')
