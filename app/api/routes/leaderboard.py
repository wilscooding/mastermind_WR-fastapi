from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_database
from app.services.leaderboard_service import LeaderboardService
from app.infra.sqlalchemy_leaderboard_repo import SQLAlchemyLeaderboardRepo
from app.api.schemas import LeaderboardOut

"""API routes for leaderboard operations.

Provides endpoints to fetch leaderboard rankings and user scores.
"""


router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/", response_model=list[LeaderboardOut])
def get_leaderboard(database: Session = Depends(get_database)):
    repo = SQLAlchemyLeaderboardRepo(database)
    service = LeaderboardService(repo)
    return service.get_leaderboard()


@router.post("/")
def add_score(user_id: int, score: int, db: Session = Depends(get_database)):
    repo = SQLAlchemyLeaderboardRepo(db)
    service = LeaderboardService(repo)
    return service.record_score(user_id, score)
