# pylint: disable=C0114, C0116
PLAYER_NAME = "JoonasPel"

def get_information(status):
    my_money = None
    my_cards = None
    for player in status["players"]:
        if player.get("name") == PLAYER_NAME:
            my_money = player.get("money")
            my_cards = player.get("cards")
            break
    return my_money, my_cards, status["card"], status["money"]

def decide_action(status):
    my_money, my_card_sets, card_on_table, money_on_table = get_information(status)

    # take card if out of money :(
    if my_money == 0:
        return True

    # take card if it is in series
    for card_set in my_card_sets:
        for card in card_set:
            if card in (card_on_table - 1, card_on_table + 1):
                return True

    # if coins on table are close enough to card number, take card
    offset = max(7, 15 - my_money)
    if money_on_table >= card_on_table - offset:
        return True

    return False
