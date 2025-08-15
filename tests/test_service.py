from app.services.game_service import GameService
from app.infra.memory_repo import InMemoryGameRepository


class FixedSecretProvider:
    def generate_secret(self, length=None, min_num=None, max_num=None):
        return [1, 2, 3, 4],    "fallback"

def test_start_and_win_game(monkeypatch):
    monkeypatch.setenv("USE_SQL", "false") 

    game_repository = InMemoryGameRepository()
    secret_provider = FixedSecretProvider()
    game_service = GameService(game_repository, secret_provider)

    game_id = game_service.start_game()
    assert game_id is not None

    guess = [1, 2, 3, 4]
    result = game_service.make_guess(game_id, guess)

    assert result['won'] is True
    assert result['attempts_left'] == 9
    assert result['last_feedback']['correct_position'] == 4
    assert result['last_feedback']['correct_number'] == 4

    game = game_service.get_game(game_id)
    assert game is not None
    assert game['won'] is True
    assert game['secret'] == [1, 2, 3, 4]