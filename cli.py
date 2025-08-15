from urllib import response
import requests

BASE_URL = "http://127.0.0.1:8000"

MODES = {
    "easy": {"length": 3, "max_attempts": 12},
    "normal": {"length": 4, "max_attempts": 10},
    "hard": {"length": 5, "max_attempts": 8}
}

def choose_mode():
    print("Choose a mode")
    print("1. Easy (3 digits, 12 attempts)")
    print("2. Normal (4 digits, 10 attempts)")
    print("3. Hard (5 digits, 8 attempts)")
    
    choice = input("> ").strip()

    if choice == "1":
        return "easy"
    elif choice == "2":
        return "normal"
    elif choice == "3":
        return "hard"
    else:
        print("Invalid choice, defaulting to Normal mode.")
        return "normal"
    

def start_game(mode):
    response = requests.post(f"{BASE_URL}/games", json={"mode": mode})
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print("Failed to start game.")
        exit(1)


def make_guess(game_id, guess):
    response = requests.post(f"{BASE_URL}/games/{game_id}/guesses", json={"guess": [int(digit) for digit in guess]})
    if response.status_code == 200:
       return response.json()
    elif response.status_code == 404:
       print("Game not found.")
       exit(1)
    else:
       print("Failed to make guess.", response.text)
       exit(1)

def get_game_state(game_id):
    response = requests.get(f"{BASE_URL}/games/{game_id}")
    response.raise_for_status()
    return response.json()

def play():
    mode = choose_mode()
    game_length = MODES[mode]["length"]
    game_id = start_game(mode)
    
    state = get_game_state(game_id)
    print(f"The secret was: {state['secret']}")
    print(f"\nNew game started: Mode: {mode.capitalize()} | GAME ID: {game_id}")
    print(f"You have {MODES[mode]['max_attempts']} attempts to guess {game_length} digits.")

    while True:
        guess = input(f"Enter your guess ({game_length} digits): ").strip()

        if not guess.isdigit() or len(guess) != game_length:
            print(f"Invalid guess. please enter {game_length} digits.")
            continue

        result = make_guess(game_id, guess)
        if "error" in result:
            print(f"Error: {result['error']}")
            continue

        if result.get("last_feedback"):
            feedback = result["last_feedback"]
            print(f"feedback: {feedback['correct_position']} correct position(s), {feedback['correct_number']} correct number(s)")

        if result.get("won"):
            print("🏆 You won!")
            break
        elif result.get("lost"):
            print("💀 You lost!")
            state = get_game_state(game_id)
            print(f"The secret was: {state['secret']}")
            break

    # print("=== Mastermind CLI ===")
    # print("Try to guess the 4-digit secret code (digits 0–9, duplicates allowed).")
    # print("Type 'exit' to quit at any time.\n")

    # game_id = start_game()

    # while True:
    #     guess = input("Enter your guess (4 digits): ").strip()
    #     if guess.lower() == "exit":
    #         print("🚪 Exiting game.")
    #         break

    #     if not guess.isdigit() or len(guess) != 4:
    #         print("❌ Invalid guess. Must be exactly 4 digits.")
    #         continue

    #     result = make_guess(game_id, guess)
    #     print(f"Feedback: {result['last_feedback']['correct_position']} correct position, "
    #           f"{result['last_feedback']['correct_number']} correct number(s)")

    #     if result["won"]:
    #         print("🏆 You won!")
    #         break
    #     elif result["lost"]:
    #         print("💀 You lost!")
    #         state = get_game_state(game_id)
    #         print(f"The secret was: {state['secret']}")
    #         break

if __name__ == "__main__":
    play()
