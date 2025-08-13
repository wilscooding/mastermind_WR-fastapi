from pydantic import BaseModel, conint
from typing import List, Optional, Annotated
import annotated_types

Digit = conint(ge=0, le=9)  
GuessList: Annotated[List[Digit], annotated_types.len(4)]

class GuessRequest(BaseModel):
    guess: GuessList

class HistoryEntry(BaseModel):
    guess: List[int]
    correct_position: int
    correct_number: int
    attempts_left: int

class GameResponse(BaseModel):
    id: int
    attempts_used: int
    attempts_left: int
    history: List[HistoryEntry]
    won: bool
    lost: bool
    mode: str
    secret: Optional[List[int]] = None

class CreateGameResponse(BaseModel):
    id: int
    mode: str
    attempts_left: int

