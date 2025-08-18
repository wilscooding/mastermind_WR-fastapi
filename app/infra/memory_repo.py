from typing import Dict, List, Optional

class InMemoryGameRepository:
    def __init__ (self):
        self._storage: Dict[int, Dict] = {}
        self._next_id: int = 1

    def create_game(self, secret: List[int], mode: str, user_id: Optional[int] = None) -> int:
        game_id = self._next_id
        self._next_id += 1
        self._storage[game_id] = {
            "id": game_id,
            "secret": secret,
            "attempts_used": 0,
            "history": [],
            "won": False,
            "lost": False,
            "mode": mode,
            "user_id": user_id
        }

        return game_id
    
    def get_game(self, game_id: int) -> Optional[Dict]:
        return self._storage.get(game_id)


    def save_game(self, game_id: int, game_data: Dict) -> None:
        if game_id in self._storage:
            self._storage[game_id] = game_data