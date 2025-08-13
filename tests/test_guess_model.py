import pytest
from pydantic import BaseModel, conint, ValidationError
from typing import Annotated, List
import annotated_types

GuessList = Annotated[List[conint(ge=0, le=9)], annotated_types.Len(4)]

class GuessRequest(BaseModel):
    guess: GuessList

def test_valid_guess():
    model = GuessRequest(guess=[1, 2, 3, 4])
    assert model.guess == [1, 2, 3, 4]

def test_invalid_length():
    with pytest.raises(ValidationError) as exc_info:
        GuessRequest.model_validate({"guess": [1, 2, 3]})
    assert "at least 4 items" in str(exc_info.value)

def test_invalid_digit():
    with pytest.raises(ValidationError) as exc_info:
        GuessRequest.model_validate({"guess": [1, 2, 3, 12]})
    assert "less than or equal to 9" in str(exc_info.value)
