from typing import List, Optional, Dict
from app.domain.logic import evaluate_guess, is_win

class GameService:
    def __init__(self, game_repository, secret_provider, max_attempts: int = 10):
        self.game_repository = game_repository
        self.secret_provider = secret_provider
        self.max_attempts = max_attempts

    def start_game(self) -> int:
        secret, mode = self.secret_provider.generate_secret()
        return self.game_repository.create_game(secret, mode)
    
    def make_guess(self, game_id: int, guess: List[int]) -> Dict:
        game = self.game_repository.get_game(game_id)
        if game is None:
            return {"error": "Game not found"}
        if game['won'] or game['lost']:
            return {"error": "Game already finished"}
        
        correct_position, correct_number = evaluate_guess(game['secret'], guess)

        game['history'].append({
            "guess": guess,
            "correct_position": correct_position,
            "correct_number": correct_number,
        })
        game['attempts_used'] += 1
        game['won'] = is_win(correct_position, len(game['secret']))
        game['lost'] = (not game['won'] and (game['attempts_used'] >= self.max_attempts))

        self.game_repository.save_game(game_id, game)

        return {
            "attempts_left": self.max_attempts - game['attempts_used'],
            "won": game['won'],
            "lost": game['lost'],
            "last_feedback": {
                "correct_position": correct_position,
                "correct_number": correct_number    
            }
        }
    

    def get_game(self, game_id: int) -> Optional[Dict]:
        game = self.game_repository.get_game(game_id)
        if game is None:
            return None

        return {
            "id": game_id,
            "attempts_used": game['attempts_used'],
            "attempts_left": self.max_attempts - game['attempts_used'],
            "history": game['history'],
            "won": game['won'],
            "lost": game['lost'],
            "mode": game['mode'],
            "secret": game['secret'] if game['won'] or game['lost'] else None
        }
