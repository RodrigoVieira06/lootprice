from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.price import Price
from app.models.store import Store
from app.models.store_product import StoreProduct
from app.schemas.price import PriceRead

router = APIRouter(tags=["prices"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_visible_prices(session: AsyncSession, game_id: UUID) -> list[PriceRead]:
    statement = (
        select(Price, Store, StoreProduct)
        .join(StoreProduct, Price.store_product_id == StoreProduct.id)
        .join(Store, StoreProduct.store_id == Store.id)
        .where(
            StoreProduct.game_id == game_id,
            Store.compliance_status == "approved",
            Store.allows_price_display.is_(True),
            Store.is_active.is_(True),
        )
        .order_by(Price.price_brl)
    )
    result = await session.execute(statement)

    return [
        PriceRead(
            id=price.id,
            store=store.name,
            store_slug=store.slug,
            price_brl=price.price_brl,
            original_price_brl=price.original_price_brl,
            discount_percent=price.discount_percent,
            currency=price.currency,
            outbound_url=f"/api/v1/out/{price.id}",
            is_marketplace=store.is_marketplace,
            is_available=price.is_available and store_product.is_available,
            scraped_at=price.scraped_at,
        )
        for price, store, store_product in result.all()
    ]


@router.get("/prices", response_model=list[PriceRead])
async def list_prices(
    game_id: Annotated[UUID, Query()], session: SessionDep
) -> list[PriceRead]:
    return await get_visible_prices(session, game_id)
