from functools import lru_cache
import os

from app.infra.memory_repo import InMemoryGameRepository
from app.infra.random_org import RandomOrgSecretProvider
from app.infra.local_random import LocalRandomSecretProvider
from app.infra.combined_secret import CombinedSecretProvider
from app.services.game_service import GameService

def _bool_env(var_name: str, default: bool) -> bool:

    return os.getenv(var_name, str(default)).lower() in ('true', '1', 'yes', 't', 'y', 'on')

@lru_cache
def get_game_repository() -> InMemoryGameRepository:
    return InMemoryGameRepository()

@lru_cache
def get_secret_provider():
    use_random = _bool_env("USE_RANDOM", True)

    if use_random:
        timeout = float(os.getenv("RANDOM_ORG_TIMEOUT", 2.0))
        retries = int(os.getenv("RANDOM_ORG_RETRIES", 3))
        primary = RandomOrgSecretProvider(timeout=timeout, retries=retries)
        fallback = LocalRandomSecretProvider()
        return CombinedSecretProvider(primary=primary, fallback=fallback)
    
    return LocalRandomSecretProvider()

@lru_cache
def get_game_service() -> GameService:
    game_repository = get_game_repository()
    secret_provider = get_secret_provider()
    max_attempts = int(os.getenv("MAX_ATTEMPTS", 10))
    return GameService(game_repository=game_repository, secret_provider=secret_provider, max_attempts=max_attempts)

