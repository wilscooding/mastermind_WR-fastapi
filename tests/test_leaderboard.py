from app.api.deps import get_game_service

def test_online_game_scoring(client):
    # signup
    signup_resp = client.post("/users/signup", json={
        "username": "testplayer",
        "email": "testplayer@example.com",
        "password": "password123"
    })
    assert signup_resp.status_code == 200

    # login
    login_resp = client.post("/users/login", json={
        "email": "testplayer@example.com",
        "password": "password123"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # start online game
    game_resp = client.post("/games/online", json={"mode": "easy"}, headers=headers)
    assert game_resp.status_code == 200
    game_id = game_resp.json()["id"]

    # fetch secret from repo
    secret = get_game_service().game_repository.get_game(game_id)["secret"]

    # make winning guess
    guess_resp = client.post(
        f"/games/{game_id}/guesses",
        json={"guess": secret},  # already a list of ints
        headers=headers
    )
    assert guess_resp.status_code == 200
    data = guess_resp.json()
    assert data["won"] is True
    assert data["score"] is not None

    # check leaderboard
    leaderboard_resp = client.get("/leaderboard/")
    assert leaderboard_resp.status_code == 200
    scores = leaderboard_resp.json()
    assert any(entry["score"] == data["score"] for entry in scores)
