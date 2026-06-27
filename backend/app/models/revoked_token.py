from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Index, text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


def utc_now() -> datetime:
    return datetime.now(UTC)


class RevokedToken(SQLModel, table=True):
    __tablename__ = "revoked_tokens"
    __table_args__ = (
        Index("uq_revoked_tokens_jti", "token_jti", unique=True),
        Index("idx_revoked_tokens_expires_at", "expires_at"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    token_jti: UUID = Field(default_factory=uuid4)
    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    revoked_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
            server_default=text("now()"),
        ),
    )
    expires_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    user: Optional["User"] = Relationship(back_populates="revoked_tokens")
