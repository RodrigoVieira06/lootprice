from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Index, text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.oauth_account import OAuthAccount
    from app.models.revoked_token import RevokedToken


def utc_now() -> datetime:
    return datetime.now(UTC)


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'admin')", name="chk_users_role"),
        Index("uq_users_email", "email", unique=True),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(sa_column=Column(CITEXT(), nullable=False))
    display_name: str | None = Field(default=None, max_length=120)
    hashed_password: str | None = None
    avatar_url: str | None = None
    role: str = Field(default="user", max_length=20)
    is_active: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, default=True),
    )
    last_login_at: datetime | None = Field(
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

    oauth_accounts: list["OAuthAccount"] = Relationship(back_populates="user")
    revoked_tokens: list["RevokedToken"] = Relationship(back_populates="user")
