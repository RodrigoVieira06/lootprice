"""create core catalog tables

Revision ID: 202606220001
Revises: 202606210001
Create Date: 2026-06-22 00:00:01

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "202606220001"
down_revision: str | Sequence[str] | None = "202606210001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "stores",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column("slug", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column("base_url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("logo_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "crawler_key",
            sqlmodel.sql.sqltypes.AutoString(length=100),
            nullable=True,
        ),
        sa.Column(
            "is_marketplace",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("uq_stores_slug", "stores", ["slug"], unique=True)
    op.create_index(
        "uq_stores_crawler_key",
        "stores",
        ["crawler_key"],
        unique=True,
        postgresql_where=sa.text("crawler_key IS NOT NULL"),
    )

    op.create_table(
        "games",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "title",
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=False,
        ),
        sa.Column(
            "canonical_name",
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=False,
        ),
        sa.Column("slug", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column("cover_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "platform",
            sqlmodel.sql.sqltypes.AutoString(length=30),
            server_default="pc",
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
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
            "platform IN ('pc', 'playstation', 'xbox', 'nintendo', 'mobile')",
            name="chk_games_platform",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("uq_games_slug", "games", ["slug"], unique=True)
    op.create_index("idx_games_canonical_name", "games", ["canonical_name"])
    op.create_index("idx_games_title", "games", ["title"])

    op.create_table(
        "store_products",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("store_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("game_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "external_id",
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=True,
        ),
        sa.Column(
            "store_title",
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=False,
        ),
        sa.Column("store_url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("cover_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "platform",
            sqlmodel.sql.sqltypes.AutoString(length=30),
            server_default="pc",
            nullable=False,
        ),
        sa.Column(
            "is_available",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "first_seen_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
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
            "platform IN ('pc', 'playstation', 'xbox', 'nintendo', 'mobile')",
            name="chk_store_products_platform",
        ),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["store_id"], ["stores.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uq_store_products_external_id",
        "store_products",
        ["store_id", "external_id"],
        unique=True,
        postgresql_where=sa.text("external_id IS NOT NULL"),
    )
    op.create_index(
        "uq_store_products_url",
        "store_products",
        ["store_id", "store_url"],
        unique=True,
    )
    op.create_index(
        "idx_store_products_game_id",
        "store_products",
        ["game_id"],
    )
    op.create_index(
        "idx_store_products_store_id",
        "store_products",
        ["store_id"],
    )

    op.create_table(
        "prices",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("store_product_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("price_brl", sa.Numeric(10, 2), nullable=False),
        sa.Column("original_price_brl", sa.Numeric(10, 2), nullable=True),
        sa.Column("discount_percent", sa.Integer(), nullable=True),
        sa.Column(
            "currency",
            sqlmodel.sql.sqltypes.AutoString(length=3),
            server_default="BRL",
            nullable=False,
        ),
        sa.Column("affiliate_url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "is_available",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("scraped_at", sa.DateTime(timezone=True), nullable=False),
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
            "price_brl >= 0 "
            "AND (original_price_brl IS NULL OR original_price_brl >= 0)",
            name="chk_prices_money_non_negative",
        ),
        sa.CheckConstraint(
            "discount_percent IS NULL OR discount_percent BETWEEN 0 AND 100",
            name="chk_prices_discount_percent",
        ),
        sa.ForeignKeyConstraint(
            ["store_product_id"],
            ["store_products.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uq_prices_store_product_id",
        "prices",
        ["store_product_id"],
        unique=True,
    )
    op.create_index("idx_prices_price_brl", "prices", ["price_brl"])
    op.create_index("idx_prices_scraped_at", "prices", ["scraped_at"])

    stores_table = sa.table(
        "stores",
        sa.column("name", sa.String()),
        sa.column("slug", sa.String()),
        sa.column("base_url", sa.String()),
        sa.column("crawler_key", sa.String()),
        sa.column("is_marketplace", sa.Boolean()),
    )
    op.bulk_insert(
        stores_table,
        [
            {
                "name": "Steam",
                "slug": "steam",
                "base_url": "https://store.steampowered.com",
                "crawler_key": "steam",
                "is_marketplace": False,
            },
            {
                "name": "Nuuvem",
                "slug": "nuuvem",
                "base_url": "https://www.nuuvem.com",
                "crawler_key": "nuuvem",
                "is_marketplace": False,
            },
        ],
    )


def downgrade() -> None:
    op.drop_index("idx_prices_scraped_at", table_name="prices")
    op.drop_index("idx_prices_price_brl", table_name="prices")
    op.drop_index("uq_prices_store_product_id", table_name="prices")
    op.drop_table("prices")

    op.drop_index("idx_store_products_store_id", table_name="store_products")
    op.drop_index("idx_store_products_game_id", table_name="store_products")
    op.drop_index("uq_store_products_url", table_name="store_products")
    op.drop_index("uq_store_products_external_id", table_name="store_products")
    op.drop_table("store_products")

    op.drop_index("idx_games_title", table_name="games")
    op.drop_index("idx_games_canonical_name", table_name="games")
    op.drop_index("uq_games_slug", table_name="games")
    op.drop_table("games")

    op.drop_index("uq_stores_crawler_key", table_name="stores")
    op.drop_index("uq_stores_slug", table_name="stores")
    op.drop_table("stores")
