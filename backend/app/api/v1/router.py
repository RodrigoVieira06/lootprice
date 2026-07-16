from fastapi import APIRouter

from app.api.v1.games import router as games_router
from app.api.v1.prices import router as prices_router
from app.api.v1.search import router as search_router

router = APIRouter(prefix="/api/v1")
router.include_router(search_router)
router.include_router(games_router)
router.include_router(prices_router)
