
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch(
    "api.routes.search.search_youtube_tracks",
    new_callable=AsyncMock,
)
def test_search_returns_tracks(mock_search):
    mock_search.return_value = [
        {
            "id": "abc123",
            "title": "Telugu Song",
            "artist": "Example Music",
            "thumbnail": "https://example.com/thumbnail.jpg",
            "url": "https://www.youtube.com/watch?v=abc123",
            "published_at": "2026-01-01T00:00:00Z",
        }
    ]

    response = client.get(
        "/api/v1/search",
        params={"q": "Telugu songs", "limit": 5},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["query"] == "Telugu songs"
    assert data["limit"] == 5
    assert data["total"] == 1
    assert data["source"] == "youtube"
    assert len(data["tracks"]) == 1
    assert data["tracks"][0]["title"] == "Telugu Song"

    mock_search.assert_awaited_once_with(
        q="Telugu songs",
        limit=5,
    )


def test_search_rejects_empty_query():
    response = client.get(
        "/api/v1/search",
        params={"q": ""},
    )

    assert response.status_code == 422


def test_search_rejects_limit_above_maximum():
    response = client.get(
        "/api/v1/search",
        params={"q": "Telugu songs", "limit": 26},
    )

    assert response.status_code == 422
