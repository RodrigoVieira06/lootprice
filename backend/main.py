from fastapi import FastAPI

app = FastAPI(title="LootPrice API", version="0.3.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
