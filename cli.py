import os
import json
import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN_FILE = os.path.expanduser("~/.mastermind_token")

token = None

# ---------------------------
# Token helpers
# ---------------------------
def save_token(token_value: str):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token_value}, f)

def load_token():
    global token
    if os.path.exists(TOKEN_FILE):
        try:
            data = json.load(open(TOKEN_FILE))
            token = data.get("token")
        except Exception:
            token = None

def get_headers():
    global token
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

# ---------------------------
# Authentication
# ---------------------------
def signup():
    print("\n--- Sign Up ---")
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")

    response = requests.post(f"{BASE_URL}/users/signup", json={
        "username": username,
        "email": email,
        "password": password
    })

    if response.status_code == 200:
        print("✅ Signup successful! Please log in.")
    else:
        print("❌ Signup failed:", response.text)

def login():
    global token
    print("\n--- Log In ---")
    email = input("Email: ")
    password = input("Password: ")

    response = requests.post(f"{BASE_URL}/users/login", json={
        "email": email,
        "password": password
    })

    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token") or data.get("token")
        if not token:
            print("Login failed: No token received", data)
            return
        save_token(token)   # ✅ persist token
        print("✅ Login successful!")

def logout():
    global token
    token = None
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    print("👋 Logged out successfully!")


# ---------------------------
# Game modes
# ---------------------------
MODES = {
    "easy": {"length": 3, "max_attempts": 12, "max_num": 6},
    "normal": {"length": 4, "max_attempts": 10, "max_num": 9},
    "hard": {"length": 5, "max_attempts": 8, "max_num": 9}
}

HINT_LIMITS = {
    "easy": None,
    "normal": 2,
    "hard": 1
}

def main_menu():
    print("\n==============================")
    print("          MASTERMIND          ")
    print("==============================")
    print("1. Play Local Game")
    print("2. Play Online Game (login required)")
    print("3. View Rules")
    print("4. Logout")
    print("5. Exit")
    return input("> ").strip()

def display_rules():
    print("=" * 50)
    print(" RULES FOR MASTERMIND ")
    print("=" * 50)
    print("1) At the start of the game, the computer generates a secret code:")
    print("   - Easy:   3 digits (0–6), 12 attempts")
    print("   - Normal: 4 digits (0–9), 10 attempts")
    print("   - Hard:   5 digits (0–9), 8 attempts")
    print()
    print("2) Your goal is to guess the code before attempts run out.")
    print("3) Feedback after each guess:")
    print("   ✅ Correct Position – right digit in the right spot")
    print("   🔄 Misplaced Digit – right digit but wrong spot")
    print()
    print("4) Hints:")
    print("   - Available after your 1st guess.")
    print("   - Cost 1 attempt each.")
    print("   - Hint limits by mode:")
    print("       • Easy   → Unlimited hints")
    print("       • Normal → Max 2 hints")
    print("       • Hard   → Max 1 hint")
    print()
    print("5) The game ends when:")
    print("   - You guess the code (🏆 win)")
    print("   - You run out of attempts (💀 lose)")
    input("\nPress Enter to return to Main Menu...")


def choose_mode():
    print("=" * 50)
    print("Choose a mode")
    print("=" * 50)
    print("1. Easy (3 digits, 12 attempts)")
    print("2. Normal (4 digits, 10 attempts)")
    print("3. Hard (5 digits, 8 attempts)")
    choice = input("> ").strip()
    return {"1": "easy", "2": "normal", "3": "hard"}.get(choice, "normal")

# ---------------------------
# Game functions
# ---------------------------
def start_game(mode, online=False):
    endpoint = "/games/online" if online else "/games/local"
    response = requests.post(f"{BASE_URL}{endpoint}", json={"mode": mode}, headers=get_headers())
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print("❌ Failed to start game:", response.text)
        exit(1)

def make_guess(game_id, guess, online=False):
    response = requests.post(
        f"{BASE_URL}/games/{game_id}/guesses",
        json={"guess": [int(d) for d in guess]},
        headers=get_headers() if online else {}
    )
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print("Game not found."); exit(1)
    else:
        print("Failed to make guess.", response.text); exit(1)

def get_game_state(game_id, online=False):
    response = requests.get(f"{BASE_URL}/games/{game_id}", headers=get_headers() if online else {})
    response.raise_for_status()
    return response.json()

def get_hint(game_id, online=False):
    response = requests.get(f"{BASE_URL}/games/{game_id}/hint", headers=get_headers() if online else {})
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Failed to get hint:", response.text)
        return None

def play(online=False):
    while True:
        mode = choose_mode()
        game_length = MODES[mode]["length"]
        game_id = start_game(mode, online)

        state = get_game_state(game_id, online)
        print(f"\nNew {'Online' if online else 'Local'} Game Started! Mode: {mode.capitalize()} | GAME ID: {game_id}")
        print(f"You have {MODES[mode]['max_attempts']} attempts to guess {game_length} digits.")
        print("Type your guess, or 'hint' (after first guess).")

        hint_used = 0
        hint_limit = HINT_LIMITS[mode]

        while True:
            guess = input(f"Enter {game_length}-digit guess or 'hint': ").strip()

            if guess.lower() == "hint":
                if hint_limit is not None and hint_used >= hint_limit:
                    print("No more hints available for this mode")
                    continue

                hint = get_hint(game_id, online)
                if hint:
                    hint_used += 1
                    print(f"Hint: Position {hint['position']+1} = {hint['digit']}")
                    state = get_game_state(game_id, online)
                    print(f"Attempts left: {state['attempts_left']}")
                    continue

            if not guess.isdigit() or len(guess) != game_length:
                print(f"Invalid guess. Must be {game_length} digits.")
                continue
            max_digit = MODES[mode]["max_num"]
            if any(int(number) < 0 or int(number) > max_digit for number in guess):
                print(f"Digits must be between 0 and {max_digit}.")
                continue

            result = make_guess(game_id, guess, online)
            feedback = result["last_feedback"]
            print(f"Feedback: {feedback['correct_position']} correct pos, {feedback['correct_number']} correct num")
            print(f"Attempts left: {result['attempts_left']}")

            if result["won"]:
                print("🏆 You won!")
                if "score" in result and result["score"] is not None:
                    print(f"Your score: {result['score']} (saved to leaderboard)")
                break
            elif result["lost"]:
                print("💀 You lost!")
                state = get_game_state(game_id, online)
                print(f"The secret was: {state['secret']}")
                break

        choice = input("\n1. Play Again\n2. return to Main Menu\n> ").strip()
        if choice != "1":
            break

def online_auth_menu():
    if token:
        test = requests.get(f"{BASE_URL}/users/me", headers=get_headers())
        if test.status_code == 200:
            print("🔑 You are already logged in.")
            return True
        else:
            logout()
    while True:
        print("\n---Online Game---")
        print("1. Log In")
        print("2. Sign Up")
        print("3. Back to Main Menu")
        choice = input("> ").strip()
        if choice == "1":
            login()
            if token:
                return True
        elif choice == "2":
            signup()
            login()
            if token:
                return True
        elif choice == "3":
            return False
        else:
            print("Invalid choice.")

# ---------------------------
# Main Loop
# ---------------------------
def main():
    global token
    load_token()  # ✅ load saved token
    while True:
        choice = main_menu()
        if choice == "1":
            play(online=False)
        elif choice == "2":
            if token:

                test = requests.get(f"{BASE_URL}/users/me", headers=get_headers())
                if test.status_code != 200:
                    print("⚠️ Saved login expired, please log in again.")
                    logout()
                    if not online_auth_menu():
                        continue
            else:
                if not online_auth_menu():
                    continue    

            play(online=True)
        elif choice == "3":
            display_rules()
        elif choice == "4":
            logout()
        elif choice == "5":
            print("Goodbye!"); break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()


