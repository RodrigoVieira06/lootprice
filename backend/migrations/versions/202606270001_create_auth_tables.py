"""create auth tables

Revision ID: 202606270001
Revises: 202606220001
Create Date: 2026-06-27 00:00:01

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "202606270001"
down_revision: str | Sequence[str] | None = "202606220001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("email", postgresql.CITEXT(), nullable=False),
        sa.Column(
            "display_name",
            sqlmodel.sql.sqltypes.AutoString(length=120),
            nullable=True,
        ),
        sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("avatar_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "role",
            sqlmodel.sql.sqltypes.AutoString(length=20),
            server_default="user",
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("role IN ('user', 'admin')", name="chk_users_role"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("uq_users_email", "users", ["email"], unique=True)

    op.create_table(
        "oauth_accounts",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "provider",
            sqlmodel.sql.sqltypes.AutoString(length=20),
            nullable=False,
        ),
        sa.Column(
            "provider_user_id",
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=False,
        ),
        sa.Column("provider_email", postgresql.CITEXT(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "provider IN ('google', 'discord')",
            name="chk_oauth_provider",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_oauth_accounts_user_id", "oauth_accounts", ["user_id"])
    op.create_index(
        "uq_oauth_provider_user",
        "oauth_accounts",
        ["provider", "provider_user_id"],
        unique=True,
    )

    op.create_table(
        "revoked_tokens",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("token_jti", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "revoked_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_revoked_tokens_expires_at",
        "revoked_tokens",
        ["expires_at"],
    )
    op.create_index(
        "uq_revoked_tokens_jti",
        "revoked_tokens",
        ["token_jti"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_revoked_tokens_jti", table_name="revoked_tokens")
    op.drop_index("idx_revoked_tokens_expires_at", table_name="revoked_tokens")
    op.drop_table("revoked_tokens")

    op.drop_index("uq_oauth_provider_user", table_name="oauth_accounts")
    op.drop_index("idx_oauth_accounts_user_id", table_name="oauth_accounts")
    op.drop_table("oauth_accounts")

    op.drop_index("uq_users_email", table_name="users")
    op.drop_table("users")
