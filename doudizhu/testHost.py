import doudizhu_host
import poker
import sys

def min3_cmp(c):
    return ((c & 0x1F) << 3) + (c >> 5)


def fast_p(p):
    lp = list(p)
    lp.sort(key=min3_cmp)
    return poker.visual_from_color_min3(lp)


def print_players(ppp):
    aaa = {'a':3, 'b':4, 'c':'12232'}
    aaa['foo'] = 'bar'
    return aaa




def print_all_status(dd : doudizhu_host.Doudizhu):
    print('\n\n')
    print(dd.get_player_status(0))
    print(dd.get_player_status(1))
    print(dd.get_player_status(2))

d = doudizhu_host.Doudizhu()
current_index = 0
game_win = 3

d.shuffle()

print_all_status(d)

aaa = d.master_for(current_index)
print(aaa)




while game_win == 3:
    print('')
    print_all_status(d)
    s = input("for " + str(current_index) + ":" + fast_p(d.playerHand[current_index]) + ":" +
              str(len(d.playerHand[current_index])) + ":")
    cards = poker.min3_from_color_visual(str(s))
    if cards is None:
        print("bad input")
        continue
    print(fast_p(cards))
    deal_result = d.play_card(current_index, cards)
    if deal_result:
        deal_result['try'] = 'testAAA'
        print(deal_result)
        if len(d.playerHand[current_index]) == 0:
            game_win = current_index
            print("game over, winner:", game_win)
        else:
            current_index = (current_index + 1) % 3

            if deal_result['pattern'] == 0:
                print("ok, any thing you want:")
    else:
        print("bad input")



