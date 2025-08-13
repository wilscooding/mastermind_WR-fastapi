from app.infra.memory_repo import InMemoryGameRepository

def test_create_game():
    repo = InMemoryGameRepository()
    game_id = repo.create_game([1, 2, 3, 4], "fallback")
    game = repo.get_game(game_id)
    assert game is not None
    assert game ['id'] == game_id
    assert game['secret'] == [1, 2, 3, 4]
    assert game['attempts_used'] == 0
    assert game['history'] == []
    assert game['won'] is False
    assert game['lost'] is False    
    assert game['mode'] == "fallback"

def test_save_game():
    repo = InMemoryGameRepository()
    game_id = repo.create_game([1, 2, 3, 4], "fallback")
    game = repo.get_game(game_id)
    game['attempts_used'] = 4
    game['won'] = True
    repo.save_game(game_id, game)
    updated_game = repo.get_game(game_id)
    assert updated_game["attempts_used"] == 4
    assert updated_game["won"] is True

def test_get_nonexistent_game():
    repo = InMemoryGameRepository()
    game = repo.get_game(999)  # Nonexistent game ID
    assert game is None