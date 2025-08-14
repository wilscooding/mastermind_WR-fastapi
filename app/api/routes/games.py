from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas import GuessRequest, CreateGameOut, GuessOut
from app.api.deps import get_game_service
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["games"])

@router.post("/", response_model=CreateGameOut)
def create_game(game_service: GameService = Depends(get_game_service)):
    game_id = game_service.start_game()
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

