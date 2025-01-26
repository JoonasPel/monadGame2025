import os
import json
import sys
import requests
from requests import Timeout, JSONDecodeError

APIKEY = os.getenv("APIKEY")
BASE_ENDPOINT = "https://koodipahkina.monad.fi/api"
TIMEOUT = 60

def start_new_game(retries):
    """
    Args:
        retries (int): Number of retries taken if game can't be started.

    Returns:
        tuple[str, dict]: gameId and current status
    """
    try:
        response = requests.post(f"{BASE_ENDPOINT}/game",
                                 headers={"Authorization": f"Bearer {APIKEY}"},
                                 timeout=TIMEOUT)
        if response.status_code == 401:
            sys.exit("Unauthorized. Check that your APIKEY in .env is valid.")
        response.raise_for_status()
        data = response.json()
        return data["gameId"], data["status"]
    except Timeout:
        retries -= 1
        if retries <= 0:
            sys.exit("Timeouted. Out of retries.")
        else:
            return start_new_game(retries)
    except JSONDecodeError as e:
        sys.exit(f"Failed to decode JSON game status.\n{e}")
    except Exception as e:
        sys.exit(f"Unexpected problem happened when starting new game.\n{e}")

def execute_action(game_id, action):
    """ Executes next game action (takeCard)

    Args:
        game_id (str): id of the current game
        action (boolean): action to be taken

    Returns:
        dict: Game status after executing action
    """
    try:
        response = requests.post(f"{BASE_ENDPOINT}/game/{game_id}/action",
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {APIKEY}"},
                                 data=json.dumps({"takeCard": action}),
                                 timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return data["status"]
    except Timeout as e:
        sys.exit(f"Timeouted when executing game action.\n{e}")
    except JSONDecodeError as e:
        sys.exit(f"Failed to decode JSON game status.\n{e}")
    except Exception as e:
        sys.exit(f"Unexpected problem happened when executing game action.\n{e}")
