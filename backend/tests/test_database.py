import socket

import pytest
from sqlalchemy.engine import make_url
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.core.database import check_database_connection, engine, get_session


def skip_if_postgresql_is_unavailable() -> None:
    database_url = make_url(get_settings().database_url)
    host = database_url.host or "localhost"
    port = database_url.port or 5432

    try:
        with socket.create_connection((host, port), timeout=1):
            return
    except OSError as exc:
        pytest.skip(f"PostgreSQL is not available: {exc}")


@pytest.mark.asyncio
async def test_get_session_yields_async_session() -> None:
    session_generator = get_session()
    try:
        session = await anext(session_generator)
        assert session.is_active
    finally:
        await session_generator.aclose()


@pytest.mark.asyncio
async def test_database_connection_executes_select_one() -> None:
    skip_if_postgresql_is_unavailable()

    try:
        assert await check_database_connection() is True
    except (OSError, TimeoutError, SQLAlchemyError) as exc:
        pytest.skip(f"PostgreSQL is not available: {exc}")
    finally:
        await engine.dispose()
