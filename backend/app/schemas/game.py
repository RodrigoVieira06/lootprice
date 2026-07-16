from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.price import PriceRead


class GameRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    canonical_name: str
    slug: str
    cover_url: str | None
    platform: str


class GameWithPrices(GameRead):
    prices: list[PriceRead]
