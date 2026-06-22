from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, Index, text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.store_product import StoreProduct


def utc_now() -> datetime:
    return datetime.now(UTC)


class Store(SQLModel, table=True):
    __tablename__ = "stores"
    __table_args__ = (
        Index("uq_stores_slug", "slug", unique=True),
        Index(
            "uq_stores_crawler_key",
            "crawler_key",
            unique=True,
            postgresql_where=text("crawler_key IS NOT NULL"),
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=100)
    slug: str = Field(max_length=100)
    base_url: str
    logo_url: str | None = None
    crawler_key: str | None = Field(default=None, max_length=100)
    is_marketplace: bool = Field(
        default=False,
        sa_column=Column(Boolean, nullable=False, default=False),
    )
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

    store_products: list["StoreProduct"] = Relationship(back_populates="store")
