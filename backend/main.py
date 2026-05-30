from fastapi import FastAPI

app = FastAPI(title="LootPrice API")


@app.get("/")
async def root():
    return {"message": "LootPrice API is running"}
