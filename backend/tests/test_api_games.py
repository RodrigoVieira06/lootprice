from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Game, Price, Store, StoreProduct


@pytest_asyncio.fixture
async def catalog(db_session: AsyncSession) -> Game:
    suffix = uuid4().hex
    steam = Store(
        name="Steam",
        slug=f"steam-{suffix}",
        base_url="https://store.steampowered.com",
        compliance_status="approved",
        allows_price_display=True,
    )
    hidden_store = Store(
        name="Hidden Store",
        slug=f"hidden-store-{suffix}",
        base_url="https://hidden.example",
        compliance_status="needs_review",
        allows_price_display=True,
    )
    inactive_store = Store(
        name="Inactive Store",
        slug=f"inactive-store-{suffix}",
        base_url="https://inactive.example",
        compliance_status="approved",
        allows_price_display=True,
        is_active=False,
    )
    game = Game(
        title="Cyberpunk 2077",
        canonical_name="cyberpunk 2077",
        slug=f"cyberpunk-2077-{suffix}",
    )
    other_game = Game(
        title="Baldur's Gate 3",
        canonical_name="baldurs gate 3",
        slug=f"baldurs-gate-3-{suffix}",
    )
    inactive_game = Game(
        title="Inactive Game",
        canonical_name="inactive game",
        slug=f"inactive-game-{suffix}",
        is_active=False,
    )
    db_session.add_all(
        [steam, hidden_store, inactive_store, game, other_game, inactive_game]
    )
    await db_session.flush()

    products = [
        StoreProduct(
            store_id=steam.id,
            game_id=game.id,
            store_title=game.title,
            store_url="https://store.steampowered.com/app/1091500",
        ),
        StoreProduct(
            store_id=hidden_store.id,
            game_id=game.id,
            store_title=game.title,
            store_url="https://hidden.example/cyberpunk-2077",
        ),
        StoreProduct(
            store_id=inactive_store.id,
            game_id=game.id,
            store_title=game.title,
            store_url="https://inactive.example/cyberpunk-2077",
        ),
    ]
    db_session.add_all(products)
    await db_session.flush()

    scraped_at = datetime.now(UTC)
    db_session.add_all(
        [
            Price(
                store_product_id=products[0].id,
                price_brl=Decimal("49.90"),
                affiliate_url="https://affiliate.example/steam",
                scraped_at=scraped_at,
            ),
            Price(
                store_product_id=products[1].id,
                price_brl=Decimal("39.90"),
                affiliate_url="https://affiliate.example/hidden",
                scraped_at=scraped_at,
            ),
            Price(
                store_product_id=products[2].id,
                price_brl=Decimal("29.90"),
                affiliate_url="https://affiliate.example/inactive",
                scraped_at=scraped_at,
            ),
        ]
    )
    await db_session.flush()
    return game


@pytest.mark.asyncio
async def test_search_returns_active_games_by_canonical_name(
    api_client: AsyncClient, catalog: Game
) -> None:
    response = await api_client.get("/api/v1/search", params={"q": "CYBER"})

    assert response.status_code == 200
    assert [game["slug"] for game in response.json()] == [catalog.slug]


@pytest.mark.asyncio
async def test_games_are_paginated_and_exclude_inactive_games(
    api_client: AsyncClient, catalog: Game
) -> None:
    response = await api_client.get("/api/v1/games", params={"offset": 1, "limit": 1})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["slug"] == catalog.slug


@pytest.mark.asyncio
async def test_game_detail_returns_only_compliant_prices(
    api_client: AsyncClient, catalog: Game
) -> None:
    response = await api_client.get(f"/api/v1/games/{catalog.slug}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["slug"] == catalog.slug
    assert len(payload["prices"]) == 1
    assert payload["prices"][0]["store"] == "Steam"
    assert payload["prices"][0]["outbound_url"].startswith("/api/v1/out/")
    assert "affiliate_url" not in payload["prices"][0]


@pytest.mark.asyncio
async def test_prices_return_only_compliant_prices(
    api_client: AsyncClient, catalog: Game
) -> None:
    response = await api_client.get(
        "/api/v1/prices", params={"game_id": str(catalog.id)}
    )

    assert response.status_code == 200
    payload = response.json()
    assert [price["price_brl"] for price in payload] == ["49.90"]
