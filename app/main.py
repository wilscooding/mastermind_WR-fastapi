from fastapi import FastAPI
from app.api.routes import games, queries, user, leaderboard

app = FastAPI(title="Mastermind API", version="0.0.1")

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(games.router)
app.include_router(queries.router)
app.include_router(user.router)
app.include_router(leaderboard.router)