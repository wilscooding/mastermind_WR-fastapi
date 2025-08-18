from typing import Protocol, List, Dict, Optional, Tuple

"""Abstract interfaces (ports) for repositories and services.

Defines contracts for GameRepository, LeaderboardRepository, and other persistence adapters.
"""


class GameRepository(Protocol):
    def create_game(self, secret: List[int], mode: str) -> int: ...
    def get_game(self, game_id: int) -> Optional[Dict]: ...
    def save_game(self, game_id: int, game_data: Dict) -> None: ...
    def list_games(self) -> List[Dict]: ...



class SecretProvider(Protocol):
    def generate_secret(self, length: int = 4, min_num: int = 0, max_num: int = 9) -> Tuple[List[int], str]: ...