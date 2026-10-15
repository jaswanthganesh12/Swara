
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import HTTPException

from integrations.youtube import search_youtube_tracks


@pytest.mark.asyncio
async def test_youtube_timeout_returns_504():
    with patch(
        "integrations.youtube.httpx.AsyncClient"
    ) as mock_client_class:
        mock_client = mock_client_class.return_value.__aenter__.return_value
        mock_client.get = AsyncMock(
            side_effect=httpx.TimeoutException("Request timed out")
        )

        with pytest.raises(HTTPException) as exc_info:
            await search_youtube_tracks("Telugu songs", 5)

        assert exc_info.value.status_code == 504


@pytest.mark.asyncio
async def test_youtube_http_error_returns_502():
    request = httpx.Request(
        "GET",
        "https://www.googleapis.com/youtube/v3/search",
    )
    response = httpx.Response(403, request=request)

    with patch(
        "integrations.youtube.httpx.AsyncClient"
    ) as mock_client_class:
        mock_client = mock_client_class.return_value.__aenter__.return_value
        mock_client.get = AsyncMock(
            side_effect=httpx.HTTPStatusError(
                "Forbidden",
                request=request,
                response=response,
            )
        )

        with pytest.raises(HTTPException) as exc_info:
            await search_youtube_tracks("Telugu songs", 5)

        assert exc_info.value.status_code == 502
