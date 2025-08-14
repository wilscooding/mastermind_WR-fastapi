## Journal  
### Day 1: August 12, 2025  

#### <ins>What I Accomplished Today</ins>  

### Repo & Runtime  
- Created a new public GitHub repo and pushed the initial scaffold.  
- Set up a local `venv` and installed `fastapi`, `uvicorn`, `pydantic`, `pytest`.  
- Built a minimal FastAPI app in `app/main.py` with `GET /health` returning `{"status": "ok"}`.  

### Core Game Rules (Pure Domain Logic)  
- Added `app/domain/logic.py` with:  
  - `evaluate_guess(secret, guess)` using `collections.Counter` to correctly handle duplicates.  
  - `is_win(correct_pos, length=4)` helper.  
- Standardized return contract to `(total_correct, correct_pos)` and updated tests accordingly.  
- Chose Mastermind constraints for the challenge:  
  - Length = 4  
  - Digits 0–9  
  - Duplicates allowed  

### Testing  
- Wrote unit tests in `tests/test_logic.py` for basics, duplicates, invalid length, out-of-range values, and win condition.  
- Confirmed tests pass locally with `pytest -q`.  

### Architecture Direction  
- Decided on a modular monolith organized by modules (`api/`, `services/`, `domain/`, `infra/`) using a hexagonal approach (pure core + pluggable adapters).  
- Picked FastAPI over Flask for built-in validation and auto-generated docs.  

#### <ins>Today’s Blockers</ins>  

- **ASGI load error**: Attribute `"app"` not found in module `"app.main"`.  
  - Fix: added `app/__init__.py`, ensured command is `uvicorn app.main:app --reload`, ran from project root.  

- **Pytest import error**: `ModuleNotFoundError: No module named 'app'`.  
  - Fix: added `__init__.py` in `app/` and `app/domain/`, created a clean `pytest.ini`.


- **Test expectation mix-ups**:  
  - Mixed up parameter order and tuple unpacking in tests.  
  - Clarified the definition: `total_correct = blacks + whites`, not just whites. Updated tests and names to match.  

#### <ins>What I Plan To-Do Tomorrow</ins>  

### Service & State  
- Implement an in-memory `GameRepository` and a `GameService` to track attempts, history, and won/lost without exposing the secret.  

### HTTP API (First Endpoints)  
- `POST /games` → start a new game.  
- `POST /games/{id}/guess` → validate input, return `(total_correct, correct_pos)`, and update state.  
- `GET /games/{id}` → return public game state (attempts, history, won/lost, mode).  

### Validation & Errors  
- Add Pydantic request/response models and consistent error shapes.  

### Testing  
- Write API tests using FastAPI’s `TestClient` (happy paths + invalid inputs + terminal states).  

### Random.org Integration  
- Create a `SecretProvider` adapter that fetches digits from Random.org with retry/timeout and fallback to local PRNG; tag mode (`"random_org"` or `"fallback"`).  

### Docs  
- Update `README` with run steps and cURL examples.  


## Journal  
### Day 2: August 13, 2025  

#### <ins>What I Accomplished Today</ins>  

### - Infra & Ports  
- Finished `ports.py` with stable interfaces:  
  - `GameRepository`  
  - `SecretProvider`  
- Implemented `InMemoryGameRepository`:  
  - Auto-incrementing IDs  
  - Tracks history and win/loss state  
- Added secret providers:  
  - `LocalRandomSecretProvider` using Python’s `random`  
  - `CombinedSecretProvider` with fallback logic  
  - `RandomOrgSecretProvider` with:  
    - Timeout and retry support  
    - Response validation  
    - Returns `(digits, "random_org")`  

### - Dependency Injection (`deps.py`)  
- Created `app/api/deps.py` to wire:  
  - Game repository  
  - Secret providers  
  - `GameService`  
- Added environment toggles:  
  - `USE_RANDOM`  
  - `RANDOM_ORG_TIMEOUT`  
  - `RANDOM_ORG_RETRIES`  
  - `MAX_ATTEMPTS`  
- Confirmed `deps.py` belongs under `api/` (not `infra/`) and moved it accordingly  

### - Game Service  
- Implemented `GameService` with:  
  - `start_game`  
  - `make_guess`  
  - `get_game`  
- Finalized feedback fields:  
  - `correct` (total matches)  
  - `correct_pos` (exact matches)  

### - Tests  
- Wrote unit tests for:  
  - `InMemoryGameRepository`  
  - `CombinedSecretProvider` (fallback path)  
  - `RandomOrgSecretProvider` (monkeypatched)  
- Added tests for `deps.py` to verify:  
  - Environment toggle behavior  
  - `@lru_cache` behavior  
- Fixed flaky naming/contract issues by standardizing field names and error strings  

#### <ins>Today’s Blockers & Fixes</ins>  
- Import errors from mismatched class/file names (`LocalRandomSecretProvider`, `CombinedSecretProvider`)  
  - Standardized names, added missing `__init__.py`, cleared `__pycache__`  
- Local provider returned a 1-item tuple due to trailing comma  
  - Fixed to return `(digits, "fallback")`  
- `RandomOrgSecretProvider` didn’t accept timeout/retries  
  - Updated `__init__`, added validation and retry loop  
- `@lru_cache` hid env changes  
  - Added `.cache_clear()` in tests before re-resolving deps  

#### <ins>What I Plan To-Do Tomorrow</ins>  

### - HTTP API  
- Expose endpoints with FastAPI:  
  - `POST /games` → start  
  - `POST /games/{id}/guess`  
  - `GET /games/{id}`  

### - Validation & Errors  
- Add Pydantic schemas  
- Implement consistent error handling:  
  - `404 Not Found`  
  - `409 Game Finished`  

### - API Tests  
- Use FastAPI’s `TestClient`  
- Override DI with fixed secret for determinism  
- Optional: opt-in live Random.org test gated by `LIVE_RANDOM_ORG`  

### - Docs  
- Update `README`  
- Append cURL examples  


