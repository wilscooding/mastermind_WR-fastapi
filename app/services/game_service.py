from typing import List, Optional, Dict
from app.domain.logic import evaluate_guess, is_win

class GameService:
    def __init__(self, game_repository, secret_provider, max_attempts: int = 10):
        self.game_repository = game_repository
        self.secret_provider = secret_provider
        self.max_attempts = max_attempts

    def start_game(self, mode: str = "normal", length: Optional[int] = None, max_attempts: Optional[int] = None, min_num: Optional[int] = 0, max_num: Optional[int] = 9) -> int:

        difficulty_presets = {
            "easy": {"length": 3, "max_attempts": 12, "min_num": 0, "max_num": 6},
            "normal": {"length": 4, "max_attempts": 10, "min_num": 0, "max_num": 9},
            "hard": {"length": 5, "max_attempts": 8, "min_num": 0, "max_num": 9}
        }

        if mode in difficulty_presets: 
            selected_difficulty = difficulty_presets[mode]
        
        else:
            selected_difficulty = {
                "length": length or 4,
                "max_attempts": max_attempts or 10,
                "min_num": min_num,
                "max_num": max_num
            }


        secret, _ = self.secret_provider.generate_secret(
            length=selected_difficulty["length"],
            min_num=selected_difficulty["min_num"],
            max_num=selected_difficulty["max_num"]
        )

        self.max_attempts = selected_difficulty["max_attempts"]
        return self.game_repository.create_game(secret, mode)
    
    def make_guess(self, game_id: int, guess: List[int]) -> Dict:
        game = self.game_repository.get_game(game_id)
        if game is None:
            return {"error": "Game not found"}
        
        expected_length = len(game['secret'])
        if len(guess) != expected_length:
            return {"error": f"Guess must be {expected_length} digits long"}            
        
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

