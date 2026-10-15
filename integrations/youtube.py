
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=True)

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"


async def search_youtube_tracks(q: str, limit: int = 10) -> list[dict]:
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="YouTube API key is not configured.",
        )

    params = {
        "key": api_key,
        "part": "snippet",
        "q": q,
        "type": "video",
        "videoCategoryId": "10",
        "regionCode": "IN",
        "maxResults": limit,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(YOUTUBE_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="YouTube search timed out.",
        )

    except httpx.HTTPStatusError as exc:
        # Keep the provider's response and API key out of client errors.
        if exc.response.status_code == 403:
            raise HTTPException(
                status_code=502,
                detail="YouTube rejected the request. Check API access, key restrictions, or quota.",
            )

        raise HTTPException(
            status_code=502,
            detail="YouTube search provider returned an error.",
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to YouTube.",
        )

    tracks = []

    for item in data.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        snippet = item.get("snippet", {})

        if not video_id:
            continue

        thumbnails = snippet.get("thumbnails", {})
        thumbnail = (
            thumbnails.get("high")
            or thumbnails.get("medium")
            or thumbnails.get("default")
            or {}
        )

        tracks.append({
            "id": video_id,
            "title": snippet.get("title", ""),
            "artist": snippet.get("channelTitle", ""),
            "thumbnail": thumbnail.get("url"),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "published_at": snippet.get("publishedAt"),
        })

    return tracks
