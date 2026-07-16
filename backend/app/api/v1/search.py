from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.game import Game
from app.schemas.game import GameRead

router = APIRouter(tags=["search"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/search", response_model=list[GameRead])
async def search_games(
    q: Annotated[str, Query(min_length=1)],
    session: SessionDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[Game]:
    statement = (
        select(Game)
        .where(
            Game.is_active.is_(True),
            Game.canonical_name.ilike(f"%{q.strip()}%"),
        )
        .order_by(Game.title)
        .limit(limit)
    )
    result = await session.execute(statement)
    return list(result.scalars())
