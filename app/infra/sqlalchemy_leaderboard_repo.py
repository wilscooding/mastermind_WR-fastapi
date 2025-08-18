from sqlalchemy.orm import Session
from app.infra.models import LeaderboardEntry

class SQLAlchemyLeaderboardRepo:
    def __init__(self, db: Session):
        self.db = db

    def add_entry(self, user_id: int, score: int):
        entry = LeaderboardEntry(user_id=user_id, score=score)
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_top_scores(self, limit: int = 10):
        return (
            self.db.query(LeaderboardEntry)
            .order_by(LeaderboardEntry.score.desc())
            .limit(limit)
            .all()
        )
