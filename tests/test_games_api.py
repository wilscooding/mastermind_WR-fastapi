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
            return list(range(min_num, min_num + length)), "fixed_provider"

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

    guess_res = client.post(f"/games/{game_id}/guesses", json={"guess": [0, 1, 2, 3]})
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


def test_get_hint_success():
    game_id = client.post("/games", json={"mode": "easy"}).json()["id"]

    client.post(f"/games/{game_id}/guesses", json={"guess": [1, 2, 3]})

    # request a hint
    response = client.get(f"/games/{game_id}/hint")
    assert response.status_code == 200
    data = response.json()
    assert "position" in data
    assert "digit" in data
    assert isinstance(data["position"], int)
    assert isinstance(data["digit"], int)


def test_get_hint_game_not_found():
    response = client.get("/games/9999/hint")
    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}

def test_hints_do_not_repeat_positions():
    game_id = client.post("/games", json={"mode": "easy"}).json()["id"]

    # Make a guess before requesting hints
    client.post(f"/games/{game_id}/guesses", json={"guess": [1, 2, 3]})

    first_hint = client.get(f"/games/{game_id}/hint").json()
    second_hint = client.get(f"/games/{game_id}/hint").json()

    assert "position" in first_hint
    assert "position" in second_hint
    assert first_hint["position"] != second_hint["position"]



def test_hints_exhaust_all_positions():
    game_id = client.post("/games", json={"mode": "easy"}).json()["id"]

    client.post(f"/games/{game_id}/guesses", json={"guess": [1, 2, 3]})

    # In easy mode, secret has 3 digits → max 3 hints
    for _ in range(3):
        res = client.get(f"/games/{game_id}/hint")
        assert res.status_code == 200

    # Asking again should fail
    res = client.get(f"/games/{game_id}/hint")
    assert res.status_code == 400
    assert res.json()["detail"] == "No more hints available"

def test_hint_consumes_attempt():
    game_id = client.post("/games", json={"mode": "easy"}).json()["id"]

    # Make a guess and confirm it's accepted
    guess_response = client.post(f"/games/{game_id}/guesses", json={"guess": [1, 2, 3]})
    assert guess_response.status_code == 200

    # Confirm game state reflects the guess
    game_state = client.get(f"/games/{game_id}").json()
    assert game_state["attempts_used"] == 1

    # ✅ Check that the guess was added to history
    assert "history" in game_state
    assert isinstance(game_state["history"], list)
    assert len(game_state["history"]) == 1
    assert game_state["history"][0]["guess"] == [1, 2, 3]

    # Now request a hint
    hint_response = client.get(f"/games/{game_id}/hint")
    assert hint_response.status_code == 200

    # Confirm hint consumed an attempt
    updated_state = client.get(f"/games/{game_id}").json()
    assert updated_state["attempts_used"] == 2

def test_hint_requires_first_guess():
    game_id = client.post("/games", json={"mode": "easy"}).json()["id"]

    # Immediately asking for a hint should fail
    res = client.get(f"/games/{game_id}/hint")
    assert res.status_code == 400
    assert "No guesses made yet" in res.json()["detail"]


def test_hint_not_allowed_on_last_attempt():
    game_id = client.post("/games", json={"mode": "easy"}).json()["id"]

    # Make one guess to unlock hints
    client.post(f"/games/{game_id}/guesses", json={"guess": [1, 2, 3]})

    # Burn all but 1 attempt
    for _ in range(10):  # easy mode has 12 attempts, so use 11
        client.post(f"/games/{game_id}/guesses", json={"guess": [9, 9, 9]})

    res = client.get(f"/games/{game_id}/hint")
    assert res.status_code == 400
    assert "final attempt" in res.json()["detail"]

def test_hint_before_first_guess():
    response = client.post("/games/local", json={"mode": "easy"})
    game_id = response.json()["id"]

    response = client.get(f"/games/{game_id}/hint")
    assert response.status_code == 400
    assert "no guesses made yet" in response.json()["detail"].lower()

def test_hint_on_last_attempt():
    response = client.post("/games/local", json={"mode": "easy"})
    game_id = response.json()["id"]

    # Burn almost all attempts
    for _ in range(11):
        client.post(f"/games/{game_id}/guesses", json={"guess": [0, 0, 0]})

    response = client.get(f"/games/{game_id}/hint")
    assert response.status_code == 400
    assert "final attempt" in response.json()["detail"].lower()



def test_guess_endpoint_works():
    game_id = client.post("/games", json={"mode": "easy"}).json()["id"]
    print("Created game ID:", game_id)

    # Confirm game exists
    res = client.get(f"/games/{game_id}")
    assert res.status_code == 200

    # Try making a guess
    guess_res = client.post(f"/games/{game_id}/guesses", json={"guess": [1, 2, 3]})
    print("Guess response:", guess_res.json())
    assert guess_res.status_code == 200

def test_guess_too_short_or_long():
    # Start normal game
    response = client.post("/games/local", json={"mode": "normal"})
    game_id = response.json()["id"]

    # Too short
    response = client.post(f"/games/{game_id}/guesses", json={"guess": [1, 2]})
    assert response.status_code == 400
    assert "must be" in response.json()["detail"].lower()

    # Too long
    response = client.post(f"/games/{game_id}/guesses", json={"guess": [1, 2, 3, 4, 5]})
    assert response.status_code == 400
    assert "must be" in response.json()["detail"].lower()

def test_guess_out_of_range(monkeypatch, capsys):
    inputs = iter(["1", "999", "123", "quit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    from cli import play

    try:
        play(online=False)
    except StopIteration:
        pass

    captured = capsys.readouterr()
    assert "Digits must be between" in captured.out



def test_game_loss_after_max_attempts():
    response = client.post("/games/local", json={"mode": "easy"})
    game_id = response.json()["id"]

    # Burn all attempts with wrong guess
    for _ in range(12):
        client.post(f"/games/{game_id}/guesses", json={"guess": [0, 0, 0]})

    result = client.get(f"/games/{game_id}").json()
    assert result["lost"] is True


