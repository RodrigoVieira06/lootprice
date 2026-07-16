from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.prices import get_visible_prices
from app.core.database import get_session
from app.models.game import Game
from app.schemas.game import GameRead, GameWithPrices

router = APIRouter(tags=["games"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/games", response_model=list[GameRead])
async def list_games(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[Game]:
    statement = (
        select(Game)
        .where(Game.is_active.is_(True))
        .order_by(Game.title)
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(statement)
    return list(result.scalars())


@router.get("/games/{slug}", response_model=GameWithPrices)
async def get_game_by_slug(slug: str, session: SessionDep) -> GameWithPrices:
    result = await session.execute(
        select(Game).where(Game.slug == slug, Game.is_active.is_(True))
    )
    game = result.scalar_one_or_none()
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    return GameWithPrices(
        **GameRead.model_validate(game).model_dump(),
        prices=await get_visible_prices(session, game.id),
    )
