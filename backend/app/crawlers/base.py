from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class RawGameData(BaseModel):
    """Dados normalizados de um produto retornado por uma fonte de loja."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=255)
    external_id: str | None = None
    store_url: str = Field(min_length=1)
    price_brl: Decimal = Field(ge=Decimal("0"), decimal_places=2)
    original_price_brl: Decimal | None = Field(
        default=None,
        ge=Decimal("0"),
        decimal_places=2,
    )
    affiliate_url: str | None = None
    is_available: bool = True
    store_slug: str = Field(min_length=1, max_length=100)


class BaseCrawler(ABC):
    store_slug: str

    @abstractmethod
    async def fetch(self) -> AsyncGenerator[RawGameData, None]:
        """Coleta produtos válidos da fonte da loja."""
        raise NotImplementedError
