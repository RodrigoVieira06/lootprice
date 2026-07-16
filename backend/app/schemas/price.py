from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class PriceRead(BaseModel):
    id: UUID
    store: str
    store_slug: str
    price_brl: Decimal
    original_price_brl: Decimal | None
    discount_percent: int | None
    currency: str
    outbound_url: str
    is_marketplace: bool
    is_available: bool
    scraped_at: datetime
