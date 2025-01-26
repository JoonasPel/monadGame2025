# pylint: disable=C0413
import os
import sys
from dotenv import load_dotenv
if not load_dotenv(".env"):
    sys.exit("No .env file found. Please create .env file, refer to .env.example")
from game_logic import decide_action
from api_client import start_new_game, execute_action


def validate_env():
    """ Checks that .env file has needed keys """
    for var in ["APIKEY", "PLAYER_NAME"]:
        if not os.getenv(var):
            sys.exit(f".env file doesn't contain {var}, refer to .env.example")

def get_input():
    """ Asks user how many games to play

    Returns:
        int: Amount of games to play
    """
    while True:
        try:
            games = int(input("How many games to play? (1-100): "))
            if not 1 <= games <= 100:
                print("Give number between 1 and 100")
                continue
            return games
        except ValueError:
            print("Give number between 1 and 100")

def main():
    validate_env()
    games = get_input()
    for i in range(0, games):
        game_id, status = start_new_game(retries=3)
        while status["finished"] is False:
            action = decide_action(status)
            status = execute_action(game_id, action)
        print(f"\r{i + 1}/{games} games played", end="")


if __name__ == "__main__":
    main()
