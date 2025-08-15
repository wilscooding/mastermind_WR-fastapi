from app.api import deps
from sqlalchemy import text

def test_sqlalchemy_repo_can_connect():
    repo = deps.SQLAlchemyGameRepository()

    result = repo.database_session.execute(text("SELECT 1")).scalar()

    assert result == 1
    