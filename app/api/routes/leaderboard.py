from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_database
from app.services.leaderboard_service import LeaderboardService
from app.infra.sqlalchemy_leaderboard_repo import SQLAlchemyLeaderboardRepo

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/")
def get_leaderboard(limit: int = 10, db: Session = Depends(get_database)):
    repo = SQLAlchemyLeaderboardRepo(db)
    service = LeaderboardService(repo)
    entries = service.get_leaderboard(limit)

    # Format for clean JSON
    return [
        {
            "username": entry.user.username if entry.user else None,
            "score": entry.score,
            "created_at": entry.created_at.isoformat() if entry.created_at else None,
        }
        for entry in entries
    ]

@router.post("/")
def add_score(user_id: int, score: int, db: Session = Depends(get_database)):
    repo = SQLAlchemyLeaderboardRepo(db)
    service = LeaderboardService(repo)
    return service.record_score(user_id, score)
