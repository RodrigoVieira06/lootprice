from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Index, String, text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.affiliate_click import AffiliateClick
    from app.models.store_product import StoreProduct


def utc_now() -> datetime:
    return datetime.now(UTC)


class Store(SQLModel, table=True):
    __tablename__ = "stores"
    __table_args__ = (
        CheckConstraint(
            "ingestion_source IN ('api', 'feed', 'scraper', 'manual', 'disabled')",
            name="chk_stores_ingestion_source",
        ),
        CheckConstraint(
            "compliance_status IN ('unknown', 'approved', 'blocked', 'needs_review')",
            name="chk_stores_compliance_status",
        ),
        CheckConstraint(
            "risk_level IN ('low', 'medium', 'high')",
            name="chk_stores_risk_level",
        ),
        Index("uq_stores_slug", "slug", unique=True),
        Index(
            "uq_stores_crawler_key",
            "crawler_key",
            unique=True,
            postgresql_where=text("crawler_key IS NOT NULL"),
        ),
        Index("idx_stores_ingestion_source", "ingestion_source"),
        Index("idx_stores_compliance_status", "compliance_status"),
        Index("idx_stores_risk_level", "risk_level"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=100)
    slug: str = Field(max_length=100)
    base_url: str
    logo_url: str | None = None
    crawler_key: str | None = Field(default=None, max_length=100)
    ingestion_source: str = Field(
        default="disabled",
        sa_column=Column(
            String(30),
            nullable=False,
            default="disabled",
            server_default="disabled",
        ),
    )
    allows_price_display: bool = Field(
        default=False,
        sa_column=Column(
            Boolean,
            nullable=False,
            default=False,
            server_default=text("false"),
        ),
    )
    allows_affiliate_deeplink: bool = Field(
        default=False,
        sa_column=Column(
            Boolean,
            nullable=False,
            default=False,
            server_default=text("false"),
        ),
    )
    allows_tracking_subid: bool = Field(
        default=False,
        sa_column=Column(
            Boolean,
            nullable=False,
            default=False,
            server_default=text("false"),
        ),
    )
    allows_scraping: bool = Field(
        default=False,
        sa_column=Column(
            Boolean,
            nullable=False,
            default=False,
            server_default=text("false"),
        ),
    )
    affiliate_network: str | None = Field(default=None, max_length=100)
    affiliate_link_template: str | None = None
    compliance_status: str = Field(
        default="unknown",
        sa_column=Column(
            String(30),
            nullable=False,
            default="unknown",
            server_default="unknown",
        ),
    )
    risk_level: str = Field(
        default="medium",
        sa_column=Column(
            String(20),
            nullable=False,
            default="medium",
            server_default="medium",
        ),
    )
    terms_url: str | None = None
    compliance_notes: str | None = None
    is_marketplace: bool = Field(
        default=False,
        sa_column=Column(
            Boolean,
            nullable=False,
            default=False,
            server_default=text("false"),
        ),
    )
    is_active: bool = Field(
        default=True,
        sa_column=Column(
            Boolean,
            nullable=False,
            default=True,
            server_default=text("true"),
        ),
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

    store_products: list["StoreProduct"] = Relationship(back_populates="store")
    affiliate_clicks: list["AffiliateClick"] = Relationship(back_populates="store")
