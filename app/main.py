from fastapi import FastAPI
from app.api.routes import games, queries

app = FastAPI(title="Mastermind API", version="0.0.1")

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(games.router)
app.include_router(queries.router)