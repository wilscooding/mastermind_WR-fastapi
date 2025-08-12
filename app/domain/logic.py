from collections import Counter
from typing import List, Tuple

def evaluate_guess(guess: List[int], secret: List[int]) -> Tuple[int, int]:
    if len(guess) != len(secret):
        raise ValueError("Guess and secret must be of the same length.")
    
    if any(not (0 <= n <= 9) for n in guess + secret):
        raise ValueError("Numbers must be between 0 and 9.")
    
    correct_position = sum(g == s for g, s in zip(guess, secret))
    guess_counter = Counter(guess)
    secret_counter = Counter(secret)
    correct_number = sum((guess_counter & secret_counter).values()) 

    return correct_position, correct_number


def is_win(correct_position: int, length: int) -> bool:
    return correct_position == length