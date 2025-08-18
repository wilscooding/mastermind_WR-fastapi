from app.infra.sqlalchemy_leaderboard_repo import SQLAlchemyLeaderboardRepo

"""Leaderboard service.

Handles recording scores, ranking users, and retrieving leaderboard data.
"""


class LeaderboardService:
    def __init__(self, repo: SQLAlchemyLeaderboardRepo):
        self.repo = repo

    def record_score(self, user_id: int, score: int):
        return self.repo.add_entry(user_id, score)

    def get_leaderboard(self, limit: int = 10):
        return self.repo.get_top_scores(limit)
