from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import CheckConstraint, Numeric
from sqlalchemy.dialects.postgresql import CITEXT
from sqlmodel import SQLModel

from app.models import (
    Game,
    OAuthAccount,
    Price,
    RevokedToken,
    Store,
    StoreProduct,
    User,
)
from app.schemas.user import UserRead


def constraint_names(model: type[SQLModel]) -> set[str]:
    return {
        constraint.name
        for constraint in model.__table__.constraints
        if isinstance(constraint, CheckConstraint)
    }


def index_names(model: type[SQLModel]) -> set[str]:
    return {index.name for index in model.__table__.indexes}


def server_default_sql(model: type[SQLModel], column_name: str) -> str:
    server_default = model.__table__.c[column_name].server_default

    assert server_default is not None
    return str(server_default.arg)


def test_core_catalog_models_are_registered_in_metadata() -> None:
    assert {"stores", "games", "store_products", "prices"}.issubset(
        SQLModel.metadata.tables
    )


def test_auth_models_are_registered_in_metadata() -> None:
    assert {"users", "oauth_accounts", "revoked_tokens"}.issubset(
        SQLModel.metadata.tables
    )


def test_store_model_indexes_and_defaults() -> None:
    store = Store(
        name="Steam",
        slug="steam",
        base_url="https://store.steampowered.com",
        crawler_key="steam",
    )

    assert store.is_active is True
    assert store.is_marketplace is False
    assert {"uq_stores_slug", "uq_stores_crawler_key"}.issubset(index_names(Store))


def test_user_model_constraints_indexes_and_defaults() -> None:
    user = User(email="USER@example.com")

    assert user.role == "user"
    assert user.is_active is True
    assert user.hashed_password is None
    assert isinstance(User.__table__.c.email.type, CITEXT)
    assert "chk_users_role" in constraint_names(User)
    assert "uq_users_email" in index_names(User)


def test_user_read_schema_does_not_expose_hashed_password() -> None:
    user = User(
        email="user@example.com",
        display_name="User",
        hashed_password="secret-hash",
    )

    payload = UserRead.model_validate(user, from_attributes=True).model_dump()

    assert payload["email"] == "user@example.com"
    assert "hashed_password" not in payload


def test_oauth_account_constraints_indexes_and_foreign_keys() -> None:
    oauth_account = OAuthAccount(
        user_id=uuid4(),
        provider="google",
        provider_user_id="google-123",
        provider_email="user@example.com",
    )

    assert oauth_account.provider == "google"
    assert isinstance(OAuthAccount.__table__.c.provider_email.type, CITEXT)
    assert "chk_oauth_provider" in constraint_names(OAuthAccount)
    assert {
        "uq_oauth_provider_user",
        "idx_oauth_accounts_user_id",
    }.issubset(index_names(OAuthAccount))

    foreign_keys = {
        foreign_key.target_fullname
        for foreign_key in OAuthAccount.__table__.foreign_keys
    }
    assert foreign_keys == {"users.id"}


def test_revoked_token_indexes_defaults_and_foreign_keys() -> None:
    token_jti = uuid4()
    revoked_token = RevokedToken(
        token_jti=token_jti,
        user_id=uuid4(),
        expires_at=datetime.now(UTC),
    )

    assert revoked_token.token_jti == token_jti
    assert {
        "uq_revoked_tokens_jti",
        "idx_revoked_tokens_expires_at",
    }.issubset(index_names(RevokedToken))

    foreign_keys = {
        foreign_key.target_fullname
        for foreign_key in RevokedToken.__table__.foreign_keys
    }
    assert foreign_keys == {"users.id"}


def test_game_model_constraints_indexes_and_defaults() -> None:
    game = Game(
        title="Cyberpunk 2077",
        canonical_name="cyberpunk 2077",
        slug="cyberpunk-2077",
    )

    assert game.platform == "pc"
    assert game.is_active is True
    assert "chk_games_platform" in constraint_names(Game)
    assert {
        "uq_games_slug",
        "idx_games_canonical_name",
        "idx_games_title",
    }.issubset(index_names(Game))


def test_store_product_model_constraints_indexes_and_foreign_keys() -> None:
    store_product = StoreProduct(
        store_id=uuid4(),
        game_id=uuid4(),
        external_id="1091500",
        store_title="Cyberpunk 2077",
        store_url="https://store.example/cyberpunk-2077",
    )

    assert store_product.platform == "pc"
    assert store_product.is_available is True
    assert "chk_store_products_platform" in constraint_names(StoreProduct)
    assert {
        "uq_store_products_external_id",
        "uq_store_products_url",
        "idx_store_products_game_id",
        "idx_store_products_store_id",
    }.issubset(index_names(StoreProduct))

    foreign_keys = {
        foreign_key.target_fullname
        for foreign_key in StoreProduct.__table__.foreign_keys
    }
    assert foreign_keys == {"stores.id", "games.id"}


def test_price_model_uses_decimal_numeric_and_constraints() -> None:
    price = Price(
        store_product_id=uuid4(),
        price_brl=Decimal("49.90"),
        original_price_brl=Decimal("199.90"),
        discount_percent=75,
        affiliate_url="https://store.example/cyberpunk-2077",
        scraped_at=datetime.now(UTC),
    )

    assert price.currency == "BRL"
    assert price.is_available is True
    assert isinstance(price.price_brl, Decimal)
    assert isinstance(Price.__table__.c.price_brl.type, Numeric)
    assert Price.__table__.c.price_brl.type.precision == 10
    assert Price.__table__.c.price_brl.type.scale == 2
    assert isinstance(Price.__table__.c.original_price_brl.type, Numeric)
    assert Price.__table__.c.original_price_brl.type.precision == 10
    assert Price.__table__.c.original_price_brl.type.scale == 2
    assert {
        "chk_prices_money_non_negative",
        "chk_prices_discount_percent",
    }.issubset(constraint_names(Price))
    assert {
        "uq_prices_store_product_id",
        "idx_prices_price_brl",
        "idx_prices_scraped_at",
    }.issubset(index_names(Price))


def test_timestamp_columns_keep_database_defaults_in_metadata() -> None:
    assert server_default_sql(Store, "created_at") == "now()"
    assert server_default_sql(Store, "updated_at") == "now()"
    assert server_default_sql(Game, "created_at") == "now()"
    assert server_default_sql(Game, "updated_at") == "now()"
    assert server_default_sql(StoreProduct, "first_seen_at") == "now()"
    assert server_default_sql(StoreProduct, "created_at") == "now()"
    assert server_default_sql(StoreProduct, "updated_at") == "now()"
    assert server_default_sql(Price, "created_at") == "now()"
    assert server_default_sql(Price, "updated_at") == "now()"
    assert server_default_sql(User, "created_at") == "now()"
    assert server_default_sql(User, "updated_at") == "now()"
    assert server_default_sql(OAuthAccount, "created_at") == "now()"
    assert server_default_sql(OAuthAccount, "updated_at") == "now()"
    assert server_default_sql(RevokedToken, "revoked_at") == "now()"
