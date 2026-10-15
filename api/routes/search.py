
from fastapi import APIRouter, Query

from integrations.youtube import search_youtube_tracks

router = APIRouter()


@router.get("/api/v1/search")
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
