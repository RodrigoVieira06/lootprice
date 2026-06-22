from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Index
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.store_product import StoreProduct


def utc_now() -> datetime:
    return datetime.now(UTC)


class Game(SQLModel, table=True):
    __tablename__ = "games"
    __table_args__ = (
        CheckConstraint(
            "platform IN ('pc', 'playstation', 'xbox', 'nintendo', 'mobile')",
            name="chk_games_platform",
        ),
        Index("uq_games_slug", "slug", unique=True),
        Index("idx_games_canonical_name", "canonical_name"),
        Index("idx_games_title", "title"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=255)
    canonical_name: str = Field(max_length=255)
    slug: str = Field(max_length=255)
    cover_url: str | None = None
    platform: str = Field(default="pc", max_length=30)
    is_active: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, default=True),
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False, default=utc_now),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False, default=utc_now),
    )

    store_products: list["StoreProduct"] = Relationship(back_populates="game")
