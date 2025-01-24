# pylint: disable=C0114, C0116
import os
from dotenv import load_dotenv
import requests
import json
from game_logic import decide_action

load_dotenv()
BASE_ENDPOINT = "https://koodipahkina.monad.fi/api"
START_GAME_ENDPOINT = "https://koodipahkina.monad.fi/api/game"
APIKEY = os.getenv("APIKEY")
TIMEOUT = 5

def start_new_game():
    response = requests.post(START_GAME_ENDPOINT, headers={
                             "Authorization": f"Bearer {APIKEY}"}, timeout=TIMEOUT)
    if "application/json" in response.headers.get("Content-Type", "").lower():
        data = response.json()
        return data["gameId"], data["status"]
    else:
        raise NotImplementedError("Invalid content type received")

def execute_action(game_id: str, action: bool):
    response = requests.post(f"{BASE_ENDPOINT}/game/{game_id}/action",
                             headers={"Content-Type": "application/json",
                                      "Authorization": f"Bearer {APIKEY}"},
                             data=json.dumps({"takeCard": action}),
                             timeout=TIMEOUT)
    if "application/json" in response.headers.get("Content-Type", "").lower():
        data = response.json()
        return data["status"]
    else:
        raise NotImplementedError("Invalid content type received")


def main():
    game_id, status = start_new_game()
    while status["finished"] is False:
        action: bool = decide_action(status)
        status = execute_action(game_id, action)
    print("thanks bye")


if __name__ == "__main__":
    main()
