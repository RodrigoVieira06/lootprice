import pytest


@pytest.mark.asyncio
async def test_health_returns_200(client):
    """GET /health should return 200 with status ok."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
