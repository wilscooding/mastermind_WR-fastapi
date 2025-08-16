from urllib import response
import requests

BASE_URL = "http://127.0.0.1:8000"

MODES = {
    "easy": {"length": 3, "max_attempts": 12},
    "normal": {"length": 4, "max_attempts": 10},
    "hard": {"length": 5, "max_attempts": 8}
}


def main_menu():
    print("\n==============================")
    print("          MASTERMIND          ")
    print("==============================")
    print("1. Play Game")
    print("2. View Rules")
    print("3. Quit")
    choice = input("> ").strip()
    return choice

def display_rules():
    print("=" * 50)
    print(" RULES FOR MASTERMIND ")
    print("=" * 50)
    print("1) At the start of the game, the computer will generate a secret code:")
    print("     - Easy:   3 digits (0–6), 12 attempts")
    print("     - Normal: 4 digits (0–9), 10 attempts")
    print("     - Hard:   5 digits (0–9), 8 attempts")
    print()
    print("2) Your goal is to guess the secret code before you run out of attempts.")
    print()
    print("3) After each guess, you will receive feedback:")
    print("     ✅ Correct Position – right digit in the right spot")
    print("     🔄 Misplaced Digit – right digit but in the wrong spot")
    print()
    print("4) Hints:")
    print("     - You can request a hint after your first guess.")
    print("     - Hints reveal 1 digit of the secret code.")
    print("     - ⚠️ Each hint costs 1 attempt.")
    print()
    print("5) The game ends when:")
    print("     - You guess the full code correctly (🏆 You win!)")
    print("     - You run out of attempts (💀 You lose!)")
    print()
    print("6) You may type 'return' at any time to exit to the main menu.")
    print("=" * 50)
    print()
    input("Press Enter to return to the Main Menu...")




def choose_mode():
    print("=" * 50)
    print("Choose a mode")
    print("=" * 50)
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

def get_hint(game_id):
    response = requests.get(f"{BASE_URL}/games/{game_id}/hint")
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print("Game not found.")
        exit(1)
    else:
        data = response.json()
        if "detail" in data and "No more hints" in data["detail"]:
            print("No more hints available.")
            return None
        print("Failed to get hint.", response.text)
        return None
    
def play():
    mode = choose_mode()
    game_length = MODES[mode]["length"]
    game_id = start_game(mode)
    
    state = get_game_state(game_id)
    print(f"\nNew game started: Mode: {mode.capitalize()} | GAME ID: {game_id}")
    print(f"You have {MODES[mode]['max_attempts']} attempts to guess {game_length} digits.")
    print("Type your guess, or 'hint' to request a hint (only after your first guess)")
    print("Hints cost 1 attempt, so use them wisely!")

    while True:
        guess = input(f"Enter your guess ({game_length} digits) or 'hint': ").strip()

        if guess.lower() == "hint":
            state = get_game_state(game_id)
            if not state['history']:
                print("You need to make at least one guess before requesting a hint.")
                continue

            hint = get_hint(game_id)
            if hint:
                print(f"Hint: Position {hint['position'] + 1} is digit {hint['digit']}")
                state = get_game_state(game_id)
                print(f"Attempts left: {state['attempts_left']}")
                continue

        if not guess.isdigit() or len(guess) != game_length:
            print(f"Invalid guess. please enter {game_length} digits.")
            continue

        result = make_guess(game_id, guess)
        if "error" in result:
            print(f"Error: {result['error']}")
            continue

        if result.get("last_feedback"):
            feedback = result["last_feedback"]
            print(f"Feedback: {feedback['correct_position']} correct position(s), {feedback['correct_number']} correct number(s)")

        print(f"Attempts left: {result['attempts_left']}")

        if result.get("won"):
            print("🏆 You won!")
            break
        elif result.get("lost"):
            print("💀 You lost!")
            state = get_game_state(game_id)
            print(f"The secret was: {state['secret']}")
            break

    print("\nGame Over! What would you like to do?")
    print("1. Play Again")
    print("2. Return to Main Menu")
    choice = input("> ").strip()
    return choice

def main():
    while True:
        choice = main_menu()
        if choice == "1":
            while True:
                action = play()
                if action == "1":
                    continue
                elif action == "2":
                    break
                else:
                    print("Thanks for playing Mastermind!")
                    return
        elif choice == "2":
            display_rules()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
