import os
import sys

PLAYER_NAME = os.getenv("PLAYER_NAME")

def get_information(status):
    """ Assigns needed game status information to individual variables.

    Args:
        status (dict): Current game status

    Returns:
        tuple[int, list, int, int]: game status variables used to make action decision.
    """
    for player in status["players"]:
        if player.get("name") == PLAYER_NAME:
            return player["money"], player["cards"], status["card"], status["money"]
    sys.exit(f"player name {PLAYER_NAME} not found in game status. Check .env file.")


def decide_action(status):
    """ Decides next action to take by analysing current status.

    Args:
        status (dict): Current game status

    Returns:
        boolean: next takeCard action 
    """
    my_money, my_card_sets, card_on_table, money_on_table = get_information(status)
    if my_money == 0:
        return True
    # take card if it is in series
    for card_set in my_card_sets:
        for card in card_set:
            if card in (card_on_table - 1, card_on_table + 1):
                return True
    # if money on table is close enough to card number, take card.
    offset = max(8, 15 - my_money)  # magic numbers
    if money_on_table >= card_on_table - offset:
        return True
    return False
