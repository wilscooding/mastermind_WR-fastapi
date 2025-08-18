import random
import os
from typing import List, Optional, Dict
from app.domain.logic import evaluate_guess, is_win
from app.infra.sqlalchemy_leaderboard_repo import SQLAlchemyLeaderboardRepo
from app.services.leaderboard_service import LeaderboardService
from sqlalchemy.orm import Session

ENV = os.getenv("ENV", "local")


class GameService:
    def __init__(self, game_repository, secret_provider, max_attempts: int = 10):
        self.game_repository = game_repository
        self.secret_provider = secret_provider
        self.max_attempts = max_attempts

    def start_game(self, mode: str = "normal", length: Optional[int] = None, max_attempts: Optional[int] = None, min_num: Optional[int] = 0, max_num: Optional[int] = 9, user_id: Optional[int] = None) -> int:

        print(f"DEBUG start_game called with mode={mode}, length={length}, max_attempts={max_attempts}, min_num={min_num}, max_num={max_num}, user_id={user_id}")

        difficulty_presets = {
            "easy": {"length": 3, "max_attempts": 12, "min_num": 0, "max_num": 6},
            "normal": {"length": 4, "max_attempts": 10, "min_num": 0, "max_num": 9},
            "hard": {"length": 5, "max_attempts": 8, "min_num": 0, "max_num": 9}
        }

       
        if mode in difficulty_presets and length is None and max_attempts is None:
            selected_difficulty = difficulty_presets[mode]
        
        else:
            selected_difficulty = {
                "length": length or (difficulty_presets.get(mode, {}).get("length", 4)),
                "max_attempts": max_attempts or (difficulty_presets.get(mode, {}).get("max_attempts", 10)),
                "min_num": min_num if min_num is not None else (difficulty_presets.get(mode, {}).get("min_num", 0)),
                "max_num": max_num if max_num is not None else (difficulty_presets.get(mode, {}).get("max_num", 9)),
            }

        secret, _ = self.secret_provider.generate_secret(
            length=selected_difficulty["length"],
            min_num=selected_difficulty["min_num"],
            max_num=selected_difficulty["max_num"]
        )

        self.max_attempts = selected_difficulty["max_attempts"]



        game_id = self.game_repository.create_game(secret, mode, user_id=user_id)
        game_data = self.game_repository.get_game(game_id)
        game_data['revealed_hints'] = []
        self.game_repository.save_game(game_id, game_data)

        return game_id


    def make_guess(self, game_id: int, guess: List[int], database: Optional[Session] = None) -> Dict:
        game = self.game_repository.get_game(game_id)
        if game is None:
            return {"error": "Game not found"}

        expected_length = len(game['secret'])
        if len(guess) != expected_length:
            return {"error": f"Guess must be {expected_length} digits long"}

     
        correct_position, correct_number = evaluate_guess(guess, game['secret'])

        game['history'].append({
            "guess": guess,
            "correct_position": correct_position,
            "correct_number": correct_number,
        })
        game['attempts_used'] += 1
        game['won'] = is_win(correct_position, len(game['secret']))
        game['lost'] = (not game['won'] and (game['attempts_used'] >= self.max_attempts))

        self.game_repository.save_game(game_id, game)

        score = None

        
        if game['won'] and database and game.get("user_id"):
            attempts_used = game['attempts_used']
            penalty = 100 // self.max_attempts
            score = max(0, 100 - (attempts_used * penalty))

            if score > 0:
                try:
                    repo = SQLAlchemyLeaderboardRepo(database)
                    leaderboard = LeaderboardService(repo)
                    leaderboard.record_score(game["user_id"], score)
                except Exception as e:
                    
                    print(f"⚠️ Failed to save score to leaderboard for user {game.get('user_id')}: {e}")

        return {
            "id": game_id,
            "attempts_left": self.max_attempts - game['attempts_used'],
            "won": game['won'],
            "lost": game['lost'],
            "last_feedback": {
                "correct_position": correct_position,
                "correct_number": correct_number
            },
            "score": score
        }



    def get_hint(self, game_id: int) -> Dict:

        game = self.game_repository.get_game(game_id)
        if not game:
            raise ValueError("Game not found")

        if "revealed_hints" not in game:
            game["revealed_hints"] = []

        
        if len(game['history']) == 0:
            raise ValueError("Must make at least one guess before using hints")

        attempts_left = self.max_attempts - game['attempts_used']
        if attempts_left <= 1:
            raise ValueError("Hint not allowed on final attempt")

        available_positions = [
            index for index in range(len(game['secret'])) if index not in game["revealed_hints"]
        ]

        if not available_positions:
            raise ValueError("No more hints available")

        position = random.choice(available_positions)
        digit = game['secret'][position]

        game['revealed_hints'].append(position)
        game['attempts_used'] += 1
        self.game_repository.save_game(game_id, game)

        return {"position": position, "digit": digit}

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

    def list_games(self) -> List[Dict]:
        return self.game_repository.list_games()
    
