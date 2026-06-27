from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


def utc_now() -> datetime:
    return datetime.now(UTC)


class OAuthAccount(SQLModel, table=True):
    __tablename__ = "oauth_accounts"
    __table_args__ = (
        CheckConstraint(
            "provider IN ('google', 'discord')",
            name="chk_oauth_provider",
        ),
        Index("uq_oauth_provider_user", "provider", "provider_user_id", unique=True),
        Index("idx_oauth_accounts_user_id", "user_id"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    provider: str = Field(max_length=20)
    provider_user_id: str = Field(max_length=255)
    provider_email: str | None = Field(
        default=None,
        sa_column=Column(CITEXT(), nullable=True),
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

    user: "User" = Relationship(back_populates="oauth_accounts")
