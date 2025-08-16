from fastapi import APIRouter, Body, Depends, HTTPException
from app.api.schemas import GuessRequest, CreateGameOut, GuessOut, CreateGameRequest, HintOut
from app.api.deps import get_game_service
from app.services.game_service import GameService
from typing import Optional

router = APIRouter(prefix="/games", tags=["games"])

@router.post("/", response_model=CreateGameOut)
def create_game(body: Optional[CreateGameRequest] = Body(default=None), game_service: GameService = Depends(get_game_service)):
    print("DEBUG create_game body:", body.dict() if body else None)

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




@router.get("/{game_id}/hint", response_model=HintOut)
def get_hint(
    game_id: int,
    game_service: GameService = Depends(get_game_service)
):
    try:
        result = game_service.get_hint(game_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result
