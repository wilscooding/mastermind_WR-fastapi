from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas import GameOut
from app.api.deps import get_game_service
from app.services.game_service import GameService

router = APIRouter(tags=["queries"])

@router.get("/games/{game_id}", response_model=GameOut)
def get_game(
    game_id: int, 
    game_service: GameService = Depends(get_game_service)
):
    game = game_service.get_game(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game