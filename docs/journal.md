## Journal  

---

### Day 1: August 12, 2025  

#### <ins>What I Accomplished Today</ins>  

### Repo & Runtime  
- Created a new public GitHub repo and pushed the initial scaffold.  
- Set up a local `venv` and installed `fastapi`, `uvicorn`, `pydantic`, `pytest`.  
- Built a minimal FastAPI app in `app/main.py` with `GET /health` returning `{"status": "ok"}`.  

### Core Game Rules (Pure Domain Logic)  
- Added `app/domain/logic.py` with:  
  - `evaluate_guess(secret, guess)` using `collections.Counter` to handle duplicates.  
  - `is_win(correct_pos, length=4)` helper.  
- Standardized return contract to `(total_correct, correct_pos)` and updated tests accordingly.  
- Chose Mastermind constraints: length = 4, digits 0–9, duplicates allowed.  

### Testing  
- Wrote unit tests in `tests/test_logic.py` for basics, duplicates, invalid input, and win condition.  
- Confirmed tests pass with `pytest -q`.  

### Architecture Direction  
- Decided on a modular monolith structure (`api/`, `services/`, `domain/`, `infra/`).  
- Picked FastAPI for validation and auto-generated docs.  

#### <ins>Today’s Blockers</ins>  
- **ASGI load error**: fixed by adding `__init__.py` and correct uvicorn command.  
- **Pytest import error**: fixed with `__init__.py` and clean `pytest.ini`.  
- **Test expectation mismatch**: clarified contract (`total_correct = blacks + whites`).  

#### <ins>What I Plan To Do Tomorrow</ins>  
- Implement in-memory `GameRepository` and `GameService`.  
- Add endpoints for creating games and making guesses.  
- Expand tests to cover service and API layer.  

---

### Day 2: August 13, 2025  

#### <ins>What I Accomplished Today</ins>  

### Game Repository & Service  
- Implemented `MemoryGameRepository` for temporary game state.  
- Added `GameService` with game creation, guess evaluation, win/loss detection.  

### API Endpoints  
- Added `POST /games/` (create) and `POST /games/{id}/guesses` (guess).  
- Error handling for invalid game IDs and guesses.  

### Database Integration (Initial)  
- Created `app/infra/database.py` with SQLAlchemy.  
- Set up Alembic migrations.  
- Added `Game` and `User` models.  

### Testing  
- Added tests for repository and service.  
- Expanded API tests for new routes.  

#### <ins>Today’s Blockers</ins>  
- Confusion with Alembic migrations — fixed after re-reading docs.  
- Serialization errors returning ORM objects — solved with Pydantic schemas.  

#### <ins>What I Plan To Do Tomorrow</ins>  
- Add user authentication with JWT.  
- Persist games with SQLAlchemy repositories.  
- Tie games to users in the database.  

---

### Day 3: August 14, 2025  

#### <ins>What I Accomplished Today</ins>  

### Authentication  
- Added user registration/login routes.  
- Password hashing with `bcrypt`.  
- JWT authentication in `auth_service.py`.  

### Database Persistence  
- Wired SQLAlchemy repositories for `User` and `Game`.  
- Updated `GameService` to persist games.  
- Added migrations for `users` and `games`.  

### API Updates  
- Restricted endpoints to authenticated users.  
- Linked games to `user_id`.  

### Testing  
- Added auth tests for registration/login.  
- Integration tests ensuring games are tied to users.  

#### <ins>Today’s Blockers</ins>  
- JWT decoding issues — fixed by adjusting secret/algorithm.  
- Relationship setup between `users` and `games` — fixed with `back_populates`.  

#### <ins>What I Plan To Do Tomorrow</ins>  
- Begin leaderboard system with scoring rules.  
- Add difficulty modes to games.  
- Explore hint system design.  

---

### Day 4: August 15, 2025  

#### <ins>What I Accomplished Today</ins>  

### Leaderboard Setup  
- Added `LeaderboardEntry` model.  
- Created Alembic migration for leaderboard.  
- Defined repository interface in `ports.py`.  
- Stubbed `SQLAlchemyLeaderboardRepo`.  

### Game Enhancements  
- Added difficulty modes (`easy`, `normal`, `hard`, `custom`).  
- Integrated scoring logic based on attempts left.  

### API Updates  
- Added `GET /leaderboard` route (basic version).  

### Testing  
- Added tests for scoring logic.  
- Began testing leaderboard repo.  

#### <ins>Today’s Blockers</ins>  
- Unsure of hint system design.  
- Leaderboard migration issues.  

#### <ins>What I Plan To Do Tomorrow</ins>  
- Finalize hint system in service + API.  
- Add hints to CLI.  
- Expand test coverage for hints.  

---

### Day 5: August 16, 2025  

#### <ins>What I Accomplished Today</ins>  

### Hints Endpoint  
- Implemented `POST /games/{id}/hint`.  
- Connected to `GameService.get_hint()`.  
- Added `HintOut` schema for responses.  

### CLI Integration  
- Added `hint` command in CLI.  
- Deducts attempt when used.  
- Blocks hints when exhausted or after game end.  

### Testing  
- Service tests for hints (unique positions, exhaustion).  
- API tests for valid/invalid requests.  

### Code Cleanup  
- Unified error handling.  
- Refactored `GameService` to share attempt logic across guesses/hints.  

#### <ins>Today’s Blockers</ins>  
- Edge case: hints allowed after loss — fixed with guard clause.  

#### <ins>What I Plan To Do Tomorrow</ins>  
- Clean up `README.md` formatting.  
- Fix journal inconsistencies.  
- Continue leaderboard integration.  

---

### Day 6: August 17, 2025  

#### <ins>What I Accomplished Today</ins>  

### Documentation Cleanup  
- Cleaned up `README.md` with proper code blocks/headings.  
- Fixed inconsistencies in setup instructions.  

### Journal Updates  
- Standardized structure of `journal.md`.  
- Synced plan → actual consistency across days.  

### Leaderboard Work  
- Reviewed repo + service wiring.  
- Began connecting leaderboard to API routes.  

### Bug Fixes  
- Fixed duplicate header issue in UI.  
- Resolved migration conflicts with leaderboard table.  

#### <ins>Today’s Blockers</ins>  
- Still finalizing leaderboard scoring formula.  
- Migration chain messy; considering reset.  

#### <ins>What I Plan To Do Tomorrow</ins>  
- Final cleanup and polish.  
- Run full test suite.  
- Prepare project submission.  

---

### Day 7: August 18, 2025  

#### <ins>What I Accomplished Today</ins>  

### Final Cleanup & Documentation  
- Added Table of Contents to `README.md`.  
- Verified consistent formatting across all docs.  
- Completed `journal.md` through Day 7.  

### Bug Fixes & Stability  
- Fixed minor formatting errors in error messages.  
- Verified schema consistency by recreating DB.  
- Confirmed CLI + API flows end-to-end.  

### Testing & Verification  
- Ran full test suite — all passing.  
- Verified auth → game → guess → hint → leaderboard flow.  
- Confirmed Alembic migrations apply cleanly.  

#### <ins>Today’s Blockers</ins>  
- Minor mismatch between test DB and local DB schema — fixed by recreating.  

#### <ins>What I Plan To Do Tomorrow</ins>  
- **Project submission complete.**  
- Future work could include Docker setup, frontend client, and multiplayer.  
