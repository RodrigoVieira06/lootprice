"""add store policy and affiliate clicks

Revision ID: 202606270002
Revises: 202606270001
Create Date: 2026-06-27 00:00:02

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "202606270002"
down_revision: str | Sequence[str] | None = "202606270001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "stores",
        sa.Column(
            "ingestion_source",
            sqlmodel.sql.sqltypes.AutoString(length=30),
            server_default="disabled",
            nullable=False,
        ),
    )
    op.add_column(
        "stores",
        sa.Column(
            "allows_price_display",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    op.add_column(
        "stores",
        sa.Column(
            "allows_affiliate_deeplink",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    op.add_column(
        "stores",
        sa.Column(
            "allows_tracking_subid",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    op.add_column(
        "stores",
        sa.Column(
            "allows_scraping",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    op.add_column(
        "stores",
        sa.Column(
            "affiliate_network",
            sqlmodel.sql.sqltypes.AutoString(length=100),
            nullable=True,
        ),
    )
    op.add_column(
        "stores",
        sa.Column(
            "affiliate_link_template",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=True,
        ),
    )
    op.add_column(
        "stores",
        sa.Column(
            "compliance_status",
            sqlmodel.sql.sqltypes.AutoString(length=30),
            server_default="unknown",
            nullable=False,
        ),
    )
    op.add_column(
        "stores",
        sa.Column(
            "risk_level",
            sqlmodel.sql.sqltypes.AutoString(length=20),
            server_default="medium",
            nullable=False,
        ),
    )
    op.add_column(
        "stores",
        sa.Column("terms_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column(
        "stores",
        sa.Column(
            "compliance_notes",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=True,
        ),
    )

    op.create_check_constraint(
        "chk_stores_ingestion_source",
        "stores",
        "ingestion_source IN ('api', 'feed', 'scraper', 'manual', 'disabled')",
    )
    op.create_check_constraint(
        "chk_stores_compliance_status",
        "stores",
        "compliance_status IN ('unknown', 'approved', 'blocked', 'needs_review')",
    )
    op.create_check_constraint(
        "chk_stores_risk_level",
        "stores",
        "risk_level IN ('low', 'medium', 'high')",
    )
    op.create_index("idx_stores_ingestion_source", "stores", ["ingestion_source"])
    op.create_index("idx_stores_compliance_status", "stores", ["compliance_status"])
    op.create_index("idx_stores_risk_level", "stores", ["risk_level"])

    op.execute(
        sa.text(
            """
            UPDATE stores
            SET
                ingestion_source = 'api',
                allows_price_display = true,
                allows_affiliate_deeplink = false,
                allows_tracking_subid = false,
                allows_scraping = false,
                compliance_status = 'needs_review',
                risk_level = 'medium'
            WHERE slug = 'steam'
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE stores
            SET
                ingestion_source = 'disabled',
                allows_price_display = false,
                allows_affiliate_deeplink = false,
                allows_tracking_subid = false,
                allows_scraping = false,
                compliance_status = 'needs_review',
                risk_level = 'medium'
            WHERE slug = 'nuuvem'
            """
        )
    )

    op.create_table(
        "affiliate_clicks",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("click_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("store_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("store_product_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("price_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("game_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "session_id",
            sqlmodel.sql.sqltypes.AutoString(length=120),
            nullable=True,
        ),
        sa.Column(
            "placement",
            sqlmodel.sql.sqltypes.AutoString(length=80),
            nullable=False,
        ),
        sa.Column("position", sa.Integer(), nullable=True),
        sa.Column("price_brl", sa.Numeric(10, 2), nullable=False),
        sa.Column(
            "destination_url",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column("referrer", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("user_agent", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "ip_hash",
            sqlmodel.sql.sqltypes.AutoString(length=128),
            nullable=True,
        ),
        sa.Column(
            "clicked_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["price_id"], ["prices.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["store_id"], ["stores.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["store_product_id"],
            ["store_products.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uq_affiliate_clicks_click_id",
        "affiliate_clicks",
        ["click_id"],
        unique=True,
    )
    op.create_index(
        "idx_affiliate_clicks_store_clicked",
        "affiliate_clicks",
        ["store_id", sa.text("clicked_at DESC")],
    )
    op.create_index(
        "idx_affiliate_clicks_game_clicked",
        "affiliate_clicks",
        ["game_id", sa.text("clicked_at DESC")],
    )
    op.create_index(
        "idx_affiliate_clicks_product_clicked",
        "affiliate_clicks",
        ["store_product_id", sa.text("clicked_at DESC")],
    )


def downgrade() -> None:
    op.drop_index(
        "idx_affiliate_clicks_product_clicked",
        table_name="affiliate_clicks",
    )
    op.drop_index("idx_affiliate_clicks_game_clicked", table_name="affiliate_clicks")
    op.drop_index("idx_affiliate_clicks_store_clicked", table_name="affiliate_clicks")
    op.drop_index("uq_affiliate_clicks_click_id", table_name="affiliate_clicks")
    op.drop_table("affiliate_clicks")

    op.drop_index("idx_stores_risk_level", table_name="stores")
    op.drop_index("idx_stores_compliance_status", table_name="stores")
    op.drop_index("idx_stores_ingestion_source", table_name="stores")
    op.drop_constraint("chk_stores_risk_level", "stores", type_="check")
    op.drop_constraint("chk_stores_compliance_status", "stores", type_="check")
    op.drop_constraint("chk_stores_ingestion_source", "stores", type_="check")
    op.drop_column("stores", "compliance_notes")
    op.drop_column("stores", "terms_url")
    op.drop_column("stores", "risk_level")
    op.drop_column("stores", "compliance_status")
    op.drop_column("stores", "affiliate_link_template")
    op.drop_column("stores", "affiliate_network")
    op.drop_column("stores", "allows_scraping")
    op.drop_column("stores", "allows_tracking_subid")
    op.drop_column("stores", "allows_affiliate_deeplink")
    op.drop_column("stores", "allows_price_display")
    op.drop_column("stores", "ingestion_source")
