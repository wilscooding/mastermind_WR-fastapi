from pydantic import BaseModel, conint, conlist
from typing import List, Optional, Annotated
import annotated_types

Digit = conint(ge=0, le=9)  
GuessList: conlist(Digit, min_length=4, max_length=4)= Annotated[List[Digit], annotated_types.Len(4)]

class GuessRequest(BaseModel):
    guess: GuessList

class HistoryEntry(BaseModel):
    guess: List[int]
    correct_position: int
    correct_number: int
    


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

class CreateGameOut(BaseModel):
    id: int

class GuessOut(BaseModel):
    attempts_left: int
    won: bool
    lost: bool
    last_feedback: dict

class GameOut(BaseModel):
    id: int
    attempts_used: int
    attempts_left: int
    history: List[HistoryEntry]
    won: bool
    lost: bool
    mode: str
    secret: Optional[List[int]] = None

