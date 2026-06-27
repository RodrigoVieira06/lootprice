from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, Numeric, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.store import Store


def utc_now() -> datetime:
    return datetime.now(UTC)


class AffiliateClick(SQLModel, table=True):
    __tablename__ = "affiliate_clicks"
    __table_args__ = (
        Index("uq_affiliate_clicks_click_id", "click_id", unique=True),
        Index("idx_affiliate_clicks_store_clicked", "store_id", "clicked_at"),
        Index("idx_affiliate_clicks_game_clicked", "game_id", "clicked_at"),
        Index(
            "idx_affiliate_clicks_product_clicked",
            "store_product_id",
            "clicked_at",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    click_id: UUID = Field(default_factory=uuid4)
    store_id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("stores.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    store_product_id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("store_products.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    price_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("prices.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    game_id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("games.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    session_id: str | None = Field(default=None, max_length=120)
    placement: str = Field(max_length=80)
    position: int | None = Field(
        default=None,
        sa_column=Column(Integer, nullable=True),
    )
    price_brl: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False),
    )
    destination_url: str
    referrer: str | None = None
    user_agent: str | None = None
    ip_hash: str | None = Field(default=None, max_length=128)
    clicked_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
            server_default=text("now()"),
        ),
    )

    store: "Store" = Relationship(back_populates="affiliate_clicks")
