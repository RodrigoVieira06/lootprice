from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.price import Price
    from app.models.store import Store


def utc_now() -> datetime:
    return datetime.now(UTC)


class StoreProduct(SQLModel, table=True):
    __tablename__ = "store_products"
    __table_args__ = (
        CheckConstraint(
            "platform IN ('pc', 'playstation', 'xbox', 'nintendo', 'mobile')",
            name="chk_store_products_platform",
        ),
        Index(
            "uq_store_products_external_id",
            "store_id",
            "external_id",
            unique=True,
            postgresql_where=text("external_id IS NOT NULL"),
        ),
        Index("uq_store_products_url", "store_id", "store_url", unique=True),
        Index("idx_store_products_game_id", "game_id"),
        Index("idx_store_products_store_id", "store_id"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    store_id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("stores.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    game_id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("games.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    external_id: str | None = Field(default=None, max_length=255)
    store_title: str = Field(max_length=255)
    store_url: str
    cover_url: str | None = None
    platform: str = Field(default="pc", max_length=30)
    is_available: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, default=True),
    )
    first_seen_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
            server_default=text("now()"),
        ),
    )
    last_seen_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
            server_default=text("now()"),
        ),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
            server_default=text("now()"),
        ),
    )

    store: "Store" = Relationship(back_populates="store_products")
    game: "Game" = Relationship(back_populates="store_products")
    price: "Price" = Relationship(back_populates="store_product")
