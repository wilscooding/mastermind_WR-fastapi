import app.api.deps as deps
from app.services.game_service import GameService
from app.infra.memory_repo import InMemoryGameRepository
from app.infra.local_random import LocalRandomSecretProvider
from app.infra.combined_secret import CombinedSecretProvider

def _clear_caches():
    deps.get_secret_provider.cache_clear()
    deps.get_game_service.cache_clear()
    deps.get_game_repository.cache_clear()

def test_secret_provider_uses_local_when_disabled(monkeypatch):
    monkeypatch.setenv("USE_RANDOM", "0")
    _clear_caches()
    sp = deps.get_secret_provider()
    assert isinstance(sp, LocalRandomSecretProvider)

def test_secret_provider_uses_combined_when_enabled(monkeypatch):
    monkeypatch.setenv("USE_RANDOM", "1")
    _clear_caches()
    sp = deps.get_secret_provider()
    assert isinstance(sp, CombinedSecretProvider)

def test_game_service_respects_max_attempts(monkeypatch):
    monkeypatch.setenv("MAX_ATTEMPTS", "7")
    _clear_caches()
    svc = deps.get_game_service()
    assert isinstance(svc, GameService)
    assert svc.max_attempts == 7

def test_lru_cache_means_env_change_needs_cache_clear(monkeypatch):
    # First resolve with local
    monkeypatch.setenv("USE_RANDOM", "0")
    _clear_caches()
    first = deps.get_secret_provider()
    assert isinstance(first, LocalRandomSecretProvider)

    # Flip env to enable Random.org BUT do not clear cache yet
    monkeypatch.setenv("USE_RANDOM", "1")
    cached = deps.get_secret_provider()
    # still the same object due to caching
    assert cached is first

    # Now clear caches and re-resolve -> should switch type
    _clear_caches()
    second = deps.get_secret_provider()
    assert isinstance(second, CombinedSecretProvider)
