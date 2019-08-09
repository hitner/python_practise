import random
import base64

"""
该表示法命名为AceBig
bin_cards 兼容bytearray 和 list
"""

_card_terminal_char = ['2','3','4','5','6','7','8','9','0','J','Q','K','A','V','W']
_card_bin_char = list(range(2,15)) + [16, 32]

_card_terminal_input_color = ['!','d','c','h','b']
_card_bin_color = [0, 0, 1, 2, 3]
_card_terminal_output_color = ['!','♦', '♣', '♥', '♠']


_color_input_to_bin_map = dict(zip(_card_terminal_input_color, _card_bin_color))
_color_char_to_bin_map = dict(zip(_card_terminal_char, _card_bin_char))
_char_bin_to_terminal_map = dict(zip(_card_bin_char, _card_terminal_char))

AceBig_2 = 2
AceBig_diamond = list(range(2, 15))
AceBig_club =  [ (x | 0b01000000) for x in AceBig_diamond]
AceBig_heart = [ (x | 0b10000000) for x in AceBig_diamond]
AceBig_spade = [ (x | 0b11000000) for x in AceBig_diamond]
AceBig_joker = [16, 32]

one_deck = AceBig_diamond + AceBig_club + AceBig_heart + AceBig_spade + AceBig_joker
two_deck = one_deck + one_deck


def _one_bin_card_from(terminal_input):
    color_value = _color_input_to_bin_map[terminal_input[0]]
    char_value = _color_char_to_bin_map[terminal_input[1]]
    return (color_value << 6) + char_value


def bin_card_from_terminal_string(terminal_inputs):
    if len(terminal_inputs)%2 or len(terminal_inputs) == 0: #为奇数或为空
        return None
    try:
        ret = bytearray()
        for i in range(0, len(terminal_inputs), 2):
            ret.append(_one_bin_card_from(terminal_inputs[i:i+2]))
        return ret
    except Exception as e:
        return None


def bin_card_to_terminal_output(bin_cards):
    ret = ''
    for i in range(0, len(bin_cards)):
        if bin_cards[i] == 16:
            ret = ret + '!V'
        elif bin_cards[i] == 32:
            ret = ret + '!W'
        else:
            ret = ret + _card_terminal_output_color[1+ (bin_cards[i]>>6)]
            ret = ret + _char_bin_to_terminal_map[bin_cards[i]&0x0F]

    return ret


def bin_card_remove_color(bin_cards):
    ret = bytearray(bin_cards)
    for i in range(0, len(bin_cards)):
        ret[i] = ret[i] & 0x3F
    return ret


def fisher_yates_shuffle(cards):
    """
    :param cards: bytearray 或者list
    :return: 没有返回，直接修改cards
    """
    ln = len(cards)
    if ln <= 2:
        return
    for i in range(0, ln - 2):
        j = random.randint(i, ln -1 )
        cards[i], cards[j] = cards[j], cards[i]


def bin_cards_to_base64(cards):
    bytes_ex = bytearray(cards)
    return base64.b64encode(bytes_ex).decode()


def bin_cards_from_base64(base64_cards):
    return base64.b64decode(base64_cards)


def bin_cards_remove_some(cards, deal):
    backup = list(cards)
    try:
        for c in deal:
            backup.remove(c)
    except ValueError as e:
        return False

    for c in deal:
        cards.remove(c)
    return True


def sort_by_doudizhu_rule(cards) -> list:
    """
    :param cards: 输入是list或bytearray
    :return: 排过序之后的全新的list
    """
    return sorted(cards, key=_sort_doudizhu_compare_value, reverse=True)


def _sort_doudizhu_compare_value(c):
    '''斗地主中使用的排序方法 主要2要比A大，所以要映射成15,且花色变为黑桃最大， 主要这里仅用于排序'''
    if c == 16 or c == 32:
        number_value = c << 6
    else:
        if (c &0x0F) == AceBig_2:
            number_value = (c >> 6) + (15 << 2) #2 要变成15
        else:
            number_value = ((c & 0x0F) << 2) + (c>>6)
    return number_value