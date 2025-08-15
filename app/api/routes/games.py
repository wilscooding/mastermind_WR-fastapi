from fastapi import APIRouter, Body, Depends, HTTPException
from app.api.schemas import GuessRequest, CreateGameOut, GuessOut, CreateGameRequest
from app.api.deps import get_game_service
from app.services.game_service import GameService
from typing import Optional

router = APIRouter(prefix="/games", tags=["games"])

@router.post("/", response_model=CreateGameOut)
def create_game(body: Optional[CreateGameRequest] = Body(default=None), game_service: GameService = Depends(get_game_service)):
    if body is None:
        game_id = game_service.start_game(mode="normal")
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
        raise HTTPException(status_code=404, detail=result["error"])
    return result

