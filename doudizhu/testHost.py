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
    print('0:', poker.visual_from_color_min3(ppp[0]))
    print('1:', poker.visual_from_color_min3(ppp[1]))
    print('2:', poker.visual_from_color_min3(ppp[2]))


d = doudizhu_host.Doudizhu()
current_index = 0
game_win = 3

players = d.shuffle()

print_players(players)

back3 = d.master_for(current_index)
print(fast_p(back3))

print_players(players)

while game_win == 3:
    print('')
    s = input("for " + str(current_index) + ":" + fast_p(players[current_index]) + ":" +
              str(len(players[current_index])) + ":")
    cards = poker.min3_from_color_visual(str(s))
    if cards is None:
        print("bad input")
        continue
    print(fast_p(cards))
    deal_result = d.dealCard(current_index, cards)
    if deal_result:
        current_index = deal_result[1]
        if deal_result[0]:
            print("ok:", deal_result[0].pattern, ',', deal_result[0].weight)
            if len(deal_result) == 3:
                game_win = current_index
                print("game over, winner:" , game_win)
        else:
            print("ok, any thing you want:")
    else:
        print("bad input")



