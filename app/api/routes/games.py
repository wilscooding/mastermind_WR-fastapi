import os
from fastapi import APIRouter, Body, Depends, HTTPException
from app.api.schemas import GuessRequest, CreateGameOut, GuessOut, CreateGameRequest, HintOut, GameOut
from app.api.deps import get_game_service
from app.infra.models import User
from app.services.game_service import ENV, GameService
from app.services.auth_service import get_current_user
from typing import Any, Optional

router = APIRouter(prefix="/games", tags=["games"])

ENV = os.getenv("ENV", "local")

@router.post("/", response_model=CreateGameOut)
def create_game(body: Optional[CreateGameRequest] = Body(default=None), game_service: GameService = Depends(get_game_service), current_user: Any = Depends(get_current_user) if ENV == "production" else None):
    print("DEBUG create_game body:", body.model_dump() if body else None)

    user_id = current_user.id if current_user else None

    if body is None:
        game_id = game_service.start_game(mode="normal", user_id=user_id)
    elif body.mode in ["easy", "normal", "hard"]:
        game_id = game_service.start_game(mode=body.mode, user_id=user_id)
    else:
        game_id = game_service.start_game(
            mode=body.mode or "normal",
            length=body.length,
            max_attempts=body.max_attempts,
            min_num=body.min_num,
            max_num=body.max_num
    )
    return {"id": game_id}


@router.post("/{game_id}/guesses", response_model=GuessOut)
def make_guess(
    game_id: int,
    body: GuessRequest,
    game_service: GameService = Depends(get_game_service)
):
    result = game_service.make_guess(game_id, body.guess)

    if "error" in result:
        # You can choose 404 or 400 based on the error type
        status = 404 if result["error"] == "Game not found" else 400
        raise HTTPException(status_code=status, detail=result["error"])

    return result

@router.get("/", response_model=list[CreateGameOut])
def list_games(game_service: GameService = Depends(get_game_service)):
    return game_service.list_games()




@router.get("/{game_id}/hint", response_model=HintOut)
def get_hint(
    game_id: int,
    game_service: GameService = Depends(get_game_service)
):
    game = game_service.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if not game["history"] or len(game["history"]) == 0:
        raise HTTPException(status_code=400, detail="No guesses made yet")
    try:
        result = game_service.get_hint(game_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.post("/local", response_model=CreateGameOut)
def create_local_game(
    body: Optional[CreateGameRequest] = Body(default=None),
    game_service: GameService = Depends(get_game_service)
):
    print("DEBUG create_local_game body:", body.model_dump() if body else None)

    if body is None:
        game_id = game_service.start_game(mode="normal")
    elif body.mode in ["easy", "normal", "hard"]:
        game_id = game_service.start_game(mode=body.mode)
    else:
        game_id = game_service.start_game(
            mode=body.mode or "normal",
            length=body.length,
            max_attempts=body.max_attempts,
            min_num=body.min_num,
            max_num=body.max_num,
            user_id=None
        )
    return {"id": game_id}

@router.post("/online", response_model=CreateGameOut)
def create_online_game(
    body: Optional[CreateGameRequest] = Body(default=None),
    game_service: GameService = Depends(get_game_service),
    current_user: User = Depends(get_current_user)
):
    print("DEBUG create_online_game body:", body.model_dump() if body else None)

    if body is None:
        game_id = game_service.start_game(mode="normal", user_id=current_user.id)
    elif body.mode in ["easy", "normal", "hard"]:
        game_id = game_service.start_game(mode=body.mode, user_id=current_user.id)
    else:
        game_id = game_service.start_game(
            mode=body.mode or "normal",
            length=body.length,
            max_attempts=body.max_attempts,
            min_num=body.min_num,
            max_num=body.max_num,
            user_id=current_user.id

        )
    return {"id": game_id}

@router.get("/{game_id}", response_model=GameOut)
def get_game(game_id: int, game_service: GameService = Depends(get_game_service)):
    game = game_service.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game