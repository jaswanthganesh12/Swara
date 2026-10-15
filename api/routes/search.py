
from fastapi import APIRouter, Query
from pydantic import BaseModel

from integrations.youtube import search_youtube_tracks
from schemas.track import Track

router = APIRouter()


class SearchResponse(BaseModel):
    query: str
    limit: int
    total: int
    source: str
    tracks: list[Track]


@router.get("/api/v1/search", response_model=SearchResponse)
async def search_tracks(
    q: str = Query(min_length=1, max_length=100),
    limit: int = Query(default=10, ge=1, le=25),
):
    tracks = await search_youtube_tracks(q=q, limit=limit)

    return {
        "query": q,
        "limit": limit,
        "total": len(tracks),
        "source": "youtube",
        "tracks": tracks,
    }

