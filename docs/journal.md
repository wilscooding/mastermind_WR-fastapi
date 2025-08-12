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
  - Digits 0–7  
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
