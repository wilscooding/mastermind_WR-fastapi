from sqlalchemy.orm import Session, joinedload
from app.infra.models import LeaderboardEntry, User


class SQLAlchemyLeaderboardRepo:
    def __init__(self, database: Session):
        self.database = database

    def add_entry(self, user_id: int, score: int):
        user = self.database.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} does not exist in Database, cannot add leaderboard entry.")
        
        entry = LeaderboardEntry(user_id=user_id, score=score)
        self.database.add(entry)
        self.database.commit()
        self.database.refresh(entry)
        return entry

    def get_top_scores(self, limit: int = 10):
        results = (
            self.database.query(LeaderboardEntry)
            .options(joinedload(LeaderboardEntry.user))
            .order_by(LeaderboardEntry.score.desc())
            .limit(limit)
            .all()
        )
        
        return [
            {
                "username": entry.user.username if entry.user else f"User {entry.user_id}",
                "score": entry.score,
                "user_id": entry.user_id
            }
            for entry in results
        ]