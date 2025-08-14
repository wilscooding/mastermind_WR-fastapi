import requests

BASE_URL = "http://127.0.0.1:8000"

def start_game():
    res = requests.post(f"{BASE_URL}/games")
    res.raise_for_status()
    data = res.json()
    print(f"\n🎯 New game started! Game ID: {data['id']}")
    return data["id"]

def make_guess(game_id, guess):
    payload = {"guess": [int(d) for d in guess]}
    res = requests.post(f"{BASE_URL}/games/{game_id}/guesses", json=payload)
    res.raise_for_status()
    return res.json()

def get_game_state(game_id):
    res = requests.get(f"{BASE_URL}/games/{game_id}")
    res.raise_for_status()
    return res.json()

def play():
    print("=== Mastermind CLI ===")
    print("Try to guess the 4-digit secret code (digits 0–9, duplicates allowed).")
    print("Type 'exit' to quit at any time.\n")

    game_id = start_game()

    while True:
        guess = input("Enter your guess (4 digits): ").strip()
        if guess.lower() == "exit":
            print("🚪 Exiting game.")
            break

        if not guess.isdigit() or len(guess) != 4:
            print("❌ Invalid guess. Must be exactly 4 digits.")
            continue

        result = make_guess(game_id, guess)
        print(f"Feedback: {result['last_feedback']['correct_position']} correct position, "
              f"{result['last_feedback']['correct_number']} correct number(s)")

        if result["won"]:
            print("🏆 You won!")
            break
        elif result["lost"]:
            print("💀 You lost!")
            state = get_game_state(game_id)
            print(f"The secret was: {state['secret']}")
            break

if __name__ == "__main__":
    play()
