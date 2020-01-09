import random
import base64
import enum

"""
该表示法命名为AceBig
bin_cards 全部为bytearray！！！
"""




SUIT_SHIFT = 5
WEIGHT_BITMASK = 0x1F

NUMBER2 = 2
ACE = 14
# 15 16 为保留值
BLACK_JOKER = 17
RED_JOKER = 18

DIAMOND = list(range(NUMBER2, ACE+1))
CLUB =  [ (x | 0b0100000) for x in DIAMOND]
HEART = [ (x | 0b1000000) for x in DIAMOND]
SPADE = [ (x | 0b1100000) for x in DIAMOND]
JOKERS = [BLACK_JOKER, RED_JOKER]
ONE_DECK = bytes(DIAMOND + CLUB + HEART + SPADE + JOKERS)
DOUBLE_DECK = bytes(ONE_DECK + ONE_DECK)

_card_terminal_char = ['2','3','4','5','6','7','8','9','0','J','Q','K','A','V','W']
_card_bin_char = DIAMOND + JOKERS

_card_terminal_input_color = ['!','d','c','h','s']
_card_bin_color = [0, 0, 1, 2, 3]
_card_terminal_output_color = ['!','♦', '♣', '♥', '♠']


_color_input_to_bin_map = dict(zip(_card_terminal_input_color, _card_bin_color))
_color_char_to_bin_map = dict(zip(_card_terminal_char, _card_bin_char))
_char_bin_to_terminal_map = dict(zip(_card_bin_char, _card_terminal_char))

class Suit(enum.IntEnum):
    NON_COLOR = -1
    DIAMOND = 0
    CLUB = 1
    HEART = 2
    SPADE = 3


def get_suit(card) -> Suit:
    #注意大小王也是没有COLOR的概念，包含了
    if card & 0b10010000:
        return Suit.NON_COLOR
    else:
        return (card >> SUIT_SHIFT) & 0b011

def get_weight(c) -> int:
    return c & WEIGHT_BITMASK


def _one_bin_card_from(terminal_input):
    color_value = _color_input_to_bin_map[terminal_input[0]]
    char_value = _color_char_to_bin_map[terminal_input[1]]
    return (color_value << SUIT_SHIFT) + char_value


def bin_card_from_terminal_string(terminal_inputs):
    if len(terminal_inputs)%2 or len(terminal_inputs) == 0: #为奇数或为空
        return None
    try:
        ret = bytearray()
        for i in range(0, len(terminal_inputs), 2):
            ret.append(_one_bin_card_from(terminal_inputs[i:i+2]))
        return ret
    except Exception:
        return None


def bin_card_to_terminal_output(bin_cards):
    ret = ''
    for i in range(0, len(bin_cards)):
        if bin_cards[i] == BLACK_JOKER:
            ret = ret + '!V'
        elif bin_cards[i] == RED_JOKER:
            ret = ret + '!W'
        else:
            ret = ret + _card_terminal_output_color[1+ (bin_cards[i] >> SUIT_SHIFT)]
            ret = ret + _char_bin_to_terminal_map[bin_cards[i] & WEIGHT_BITMASK]
    return ret

def bin_card_to_terminal_input(bin_cards):
    """用于自动生成一些东西并且能够存储
    """
    ret = ''
    for i in range(0, len(bin_cards)):
        if bin_cards[i] == BLACK_JOKER:
            ret = ret + '!V'
        elif bin_cards[i] == RED_JOKER:
            ret = ret + '!W'
        else:
            ret = ret + _card_terminal_input_color[1+ (bin_cards[i] >> SUIT_SHIFT)]
            ret = ret + _char_bin_to_terminal_map[bin_cards[i] & WEIGHT_BITMASK]
    return ret

def bin_card_remove_color(bin_cards):
    """返回一个全新的bytearray"""
    ret = bytearray(bin_cards)
    for i in range(0, len(bin_cards)):
        ret[i] = ret[i] & WEIGHT_BITMASK
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
    if bin_cards_has_subcards(cards, deal):
        for c in deal:
            cards.remove(c)
        return True


def bin_cards_has_subcards(cards, deal):
    backup = list(cards)
    try:
        for c in deal:
            backup.remove(c)
    except ValueError:
        return False
    return True


def sort_by_doudizhu_rule(cards) -> bytearray:
    """
    :param cards: 输入是list或bytearray
    :return: 排过序之后的全新的bytearray
    """
    s_list = sorted(cards, key=_sort_doudizhu_compare_value, reverse=True)
    return bytearray(s_list)


def _sort_doudizhu_compare_value(c):
    '''斗地主中使用的排序方法 主要2要比A大，所以要映射成15,且花色变为黑桃最大， 主要这里仅用于排序'''
    if c in JOKERS:
        number_value = c << 2 #左移6位？干什么 总是比其它花色要大; 将花色与weight换一下位置
    else:
        if (c & WEIGHT_BITMASK) == NUMBER2:
            number_value = (c >> SUIT_SHIFT) + (15 << 2) #2 要变成15
        else:
            number_value = ((c & WEIGHT_BITMASK) << 2) + (c>>SUIT_SHIFT)
    return number_value




class SplitMachine:
    def __init__(self):
        self.state = 0 #1表示，当前有值还可以继续处理 （其实除了一开始是0后面一直是1）
        self.cards = []

    def process(self,c):
        """返回一个tuple（长度，字符）"""
        if self.state:
            if self.cards[0] == c:
                self.cards.append(c)
            else:
                ret = len(self.cards), self.cards[0]
                self.cards = [c]
                return ret
        else:
            self.state = 1
            self.cards = [c]

    def end(self):
        ret = None
        if self.state:
            ret = len(self.cards), self.cards[0]
            self.state = 0
            self.cards = []
        return ret


def split_bin_cards(cards):
    """
    把一手牌分解为一个dict，分别存储4、3、2、1的牌数
    输入的cards必须是已经排过序的了
    """
    result = {}

    def add_result(ret):
        if ret:
            if ret[0] in result:
                result[ret[0]].append(ret[1])
            else:
                result[ret[0]] = [ret[1]]

    sm = SplitMachine()
    for c in cards:
        r = sm.process(c)
        add_result(r)
    r = sm.end()
    add_result(r)

    return result

