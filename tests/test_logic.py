from app.domain.logic import evaluate_guess, is_win
import pytest


def test_evaluate_guess_basic():
    secret = [1, 2, 3, 4]
    guess = [1, 2, 3, 4]
    correct_position, correct_number = evaluate_guess(secret,guess)
    assert correct_position == 4
    assert correct_number == 4
    

def test_evaluate_guess_duplicates():
    secret = [1, 2, 3, 4]
    guess = [1, 2, 2, 4]
    correct_position, correct_number = evaluate_guess(secret, guess)
    assert correct_position == 3
    assert correct_number == 3

def test_invalid_guess_length():
    secret = [1, 2, 3, 4]
    guess = [1, 2, 3]
    with pytest.raises(ValueError):
        evaluate_guess(secret, guess)
    
def test_range_check():
    secret = [1, 2, 3, 4]
    guess = [1, 2, 10, 4]  # only numbers allowed are 0-9
    with pytest.raises(ValueError):
        evaluate_guess(secret, guess)
    

def test_is_win():
    assert is_win(4, 4) is True
    assert is_win(3, 4) is False
    assert is_win(0, 4) is False
    assert is_win(2, 4) is False
    assert is_win(4, 5) is False  # Length mismatch