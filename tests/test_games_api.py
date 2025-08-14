import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.game_service import GameService
from app.infra.memory_repo import InMemoryGameRepository
from app.api import deps


@pytest.fixture(autouse=True)

def override_dependencies(monkeypatch):
    monkeypatch.setenv("USE_SQL", "false") 
    repo = InMemoryGameRepository()

    class FixedSecretProvider:
        def generate_secret(self, length=4, min_num=0, max_num=9):
            return [1, 2, 3, 4], "fixed"

    deps.get_game_repository = lambda: repo
    deps.get_secret_provider = lambda: FixedSecretProvider()
    deps.get_game_service = lambda: GameService(
        game_repository=repo,
        secret_provider=FixedSecretProvider(),
        max_attempts=10
    )
    yield

client = TestClient(app)


def test_create_game():
    res = client.post("/games")
    assert res.status_code == 200
    data = res.json()
    print(f"Created game ID: {data['id']}")
    assert "id" in data
    assert isinstance(data["id"], int)


def test_make_guess_correct_and_incorrect():
    game_id = client.post("/games").json()["id"]

    guess_res = client.post(f"/games/{game_id}/guesses", json={"guess": [1, 9, 9, 9]})
    assert guess_res.status_code == 200
    guess_data = guess_res.json()
    assert "last_feedback" in guess_data
    assert guess_data["last_feedback"]["correct_position"] >= 0
    assert guess_data["last_feedback"]["correct_number"] >= 0

    guess_res = client.post(f"/games/{game_id}/guesses", json={"guess": [1, 2, 3, 4]})
    assert guess_res.status_code == 200
    guess_data = guess_res.json()
    assert guess_data["won"] is True


def test_get_game_state():
    game_id = client.post("/games").json()["id"]

    client.post(f"/games/{game_id}/guesses", json={"guess": [1, 2, 3, 9]})

    res = client.get(f"/games/{game_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == game_id
    assert isinstance(data["history"], list)
    assert "guess" in data["history"][0]
