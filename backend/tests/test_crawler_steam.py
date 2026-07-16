from decimal import Decimal

import httpx
import pytest

from app.crawlers import SteamCrawler


async def collect(crawler: SteamCrawler) -> list[object]:
    return [item async for item in crawler.fetch()]


@pytest.mark.asyncio
async def test_steam_crawler_maps_prices_and_skips_unavailable_items() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["cc"] == "br"
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": 1091500,
                        "name": "Cyberpunk 2077",
                        "price_overview": {"final": 4999, "initial": 19990},
                    },
                    {"id": 10, "name": "Counter-Strike", "price_overview": None},
                ]
            },
            request=request,
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        products = await collect(SteamCrawler(["Cyberpunk"], client=client))
    finally:
        await client.aclose()

    assert len(products) == 1
    assert products[0].external_id == "1091500"
    assert products[0].price_brl == Decimal("49.99")
    assert products[0].original_price_brl == Decimal("199.90")
    assert products[0].affiliate_url is None


@pytest.mark.asyncio
async def test_steam_crawler_continues_after_request_failure() -> None:
    calls = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ConnectError("offline", request=request)
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": 620,
                        "name": "Portal 2",
                        "price_overview": {"final": 1999},
                    }
                ]
            },
            request=request,
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        products = await collect(SteamCrawler(["broken", "Portal"], client=client))
    finally:
        await client.aclose()

    assert calls == 2
    assert [product.title for product in products] == ["Portal 2"]
