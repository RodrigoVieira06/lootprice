from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.store_product import StoreProduct


def utc_now() -> datetime:
    return datetime.now(UTC)


class Price(SQLModel, table=True):
    __tablename__ = "prices"
    __table_args__ = (
        CheckConstraint(
            "price_brl >= 0 "
            "AND (original_price_brl IS NULL OR original_price_brl >= 0)",
            name="chk_prices_money_non_negative",
        ),
        CheckConstraint(
            "discount_percent IS NULL OR discount_percent BETWEEN 0 AND 100",
            name="chk_prices_discount_percent",
        ),
        Index("uq_prices_store_product_id", "store_product_id", unique=True),
        Index("idx_prices_price_brl", "price_brl"),
        Index("idx_prices_scraped_at", "scraped_at"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    store_product_id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("store_products.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    price_brl: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False),
    )
    original_price_brl: Decimal | None = Field(
        default=None,
        sa_column=Column(Numeric(10, 2), nullable=True),
    )
    discount_percent: int | None = Field(
        default=None,
        sa_column=Column(Integer, nullable=True),
    )
    currency: str = Field(default="BRL", max_length=3)
    affiliate_url: str
    is_available: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, default=True),
    )
    scraped_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False, default=utc_now),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False, default=utc_now),
    )

    store_product: "StoreProduct" = Relationship(back_populates="price")
