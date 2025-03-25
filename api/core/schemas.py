from __future__ import annotations

from pydantic import BaseModel, HttpUrl


class ErrorResponse(BaseModel):
    error: str


class LyricsResponse(BaseModel):
    title: str
    artist: str
    cover: HttpUrl | None = None
    lyrics: str
