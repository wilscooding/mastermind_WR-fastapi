from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from app.infra.models import Game
from app. infra.database import sessionLocal


class SQLAlchemyGameRepository:
    def __init__(self, database_session: Session = None):
        self.database_session = database_session or sessionLocal()

    def create_game(self, secret: List[int], mode: str) -> int:
        new_game = Game(secret=secret, mode=mode)
        self.database_session.add(new_game)
        self.database_session.commit()
        self.database_session.refresh(new_game)
        return new_game.id
    
    def get_game(self, game_id: int) -> Optional[Dict]:
        game = self.database_session.query(Game).filter(Game.id == game_id).first()
        return game.__dict__ if game else None
    
    def save_game(self, game_id: int, game_data: Dict) -> None:
        game = self.database_session.query(Game).filter(Game.id == game_id).first()
        if game:
            game.secret = game_data['secret']
            game.attempts_used = game_data["attemps_used"]
            game.history = game_data["history"]
            game.won = game_data["won"]
            game.lost = game_data["lost"]
            game.mode = game_data["mode"] 
            self.database_session.commit()
