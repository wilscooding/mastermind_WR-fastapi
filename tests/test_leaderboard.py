from app.api.deps import get_game_service

import pytest
from app.infra.database import Base
from app.infra.models import LeaderboardEntry, User  

@pytest.fixture(autouse=True)
def clean_tables(database_session):
    database_session.query(LeaderboardEntry).delete()
    database_session.query(User).delete()
    database_session.commit()
    yield
    database_session.query(LeaderboardEntry).delete()
    database_session.query(User).delete()
    database_session.commit()


def test_online_game_scoring(client):
    signup_resp = client.post("/users/signup", json={
        "username": "testplayer",
        "email": "testplayer@example.com",
        "password": "password123"
    })
    assert signup_resp.status_code == 200

    login_resp = client.post("/users/login", json={
        "email": "testplayer@example.com",
        "password": "password123"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    game_resp = client.post("/games/online", json={"mode": "easy"}, headers=headers)
    assert game_resp.status_code == 200
    game_id = game_resp.json()["id"]

    secret = get_game_service().game_repository.get_game(game_id)["secret"]

    guess_resp = client.post(
        f"/games/{game_id}/guesses",
        json={"guess": secret},  
        headers=headers
    )
    assert guess_resp.status_code == 200
    data = guess_resp.json()
    assert data["won"] is True
    assert data["score"] is not None

    leaderboard_resp = client.get("/leaderboard/")
    assert leaderboard_resp.status_code == 200
    scores = leaderboard_resp.json()
    assert any(entry["score"] == data["score"] for entry in scores)

def test_leaderboard_sorting(database_session, test_user_factory, game_service):
    user1 = test_user_factory(username="user1", email="u1@example.com", password="password123")
    user2 = test_user_factory(username="user2", email="u2@example.com", password="password123")

    from app.services.leaderboard_service import LeaderboardService
    from app.infra.sqlalchemy_leaderboard_repo import SQLAlchemyLeaderboardRepo

    repo = SQLAlchemyLeaderboardRepo(database_session)
    leaderboard = LeaderboardService(repo)
    leaderboard.record_score(user1.id, 50)
    leaderboard.record_score(user2.id, 80)

    scores = leaderboard.get_leaderboard(limit=10)
    assert scores[0]["username"] == "user2"
    assert scores[0]["score"] == 80
    assert scores[1]["username"] == "user1"
    assert scores[1]["score"] == 50


def test_empty_leaderboard(database_session):
    from app.services.leaderboard_service import LeaderboardService
    from app.infra.sqlalchemy_leaderboard_repo import SQLAlchemyLeaderboardRepo

    repo = SQLAlchemyLeaderboardRepo(database_session)
    leaderboard = LeaderboardService(repo)
    scores = leaderboard.get_leaderboard(limit=10)
    assert scores == []
