import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.game_service import GameService
from app.infra.memory_repo import InMemoryGameRepository
from app.api import deps

@pytest.fixture(autouse=True)
def override_dependencies():
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

def test_get_existing_game():
    game_id = client.post("/games").json()["id"]
    res = client.get(f"/games/{game_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == game_id
    assert isinstance(data["history"], list)

def test_get_non_existing_game():
    res = client.get("/games/9999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Game not found"
