from pydantic import BaseModel, ConfigDict, conint, conlist
from typing import List, Optional, Annotated
import annotated_types

Digit = conint(ge=0, le=9)  
# minimal length will be 1 and max length will be 10

GuessList = Annotated[List[Digit], annotated_types.Len(min_length=1, max_length=10)]

class GuessRequest(BaseModel):
    guess: GuessList



class CreateGameRequest(BaseModel):
    mode: Optional[str] = "normal"
    length: Optional[int] = None
    max_attempts: Optional[int] = None
    min_num: Optional[int] = None
    max_num: Optional[int] = None

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
    secret: Optional[List[int]] 

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

class HintOut(BaseModel):
    position: int
    digit: int
    
