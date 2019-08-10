import core_doudizhu
import card
import sys




def print_get_player_status(dd : core_doudizhu.CoreDoudizhu):
    print('\n\n')
    print(dd.get_player_status(0))
    print(dd.get_player_status(1))
    print(dd.get_player_status(2))


def print_player_cards(dd, index):
    index_cards = card.bin_card_to_terminal_output(dd.playerHand[index])
    print(f'index:{index},cards:{index_cards}')

game = core_doudizhu.CoreDoudizhu()

game.shuffle()
print_get_player_status(game)

current_index = 1
set_landlord_ret = game.set_landlord(current_index)
print(set_landlord_ret)
print_get_player_status(game)

game_stage = game.stage


while game_stage != core_doudizhu.CoreDoudizhu.STAGE_FINISHED:

    current_index_cards = game.playerHand[current_index]
    print(f'\n\ncurrent index:{current_index},cards:{card.bin_card_to_terminal_output(current_index_cards)},length:{len(current_index_cards)}')
    if not game._previous_cd():
        print('now anything you want...')
    input_str = input('--->:')

    input_bin_cards = None
    if input_str:
        input_bin_cards = card.bin_card_from_terminal_string(input_str)
        print(f'had input cards:{card.bin_card_to_terminal_output(input_bin_cards)}')
        if input_bin_cards is None:
            print("bad input")
            continue

    deal_result = game.play_card(current_index, input_bin_cards)
    if deal_result:
        print(deal_result)

        if len(game.playerHand[current_index]) == 0:
            print("game over, winner:", current_index)
            exit()
        else:
            current_index = (current_index + 1) % 3
    else:
        print("not valuable play card")



