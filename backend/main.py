from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router

app = FastAPI(title="LootPrice API", version="0.3.0")
app.include_router(api_v1_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
