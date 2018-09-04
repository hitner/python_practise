import random
'''
poker牌的几种表现形式

'''

# 展示层表示
'''
A 2 3 4 5 6 7 8 9 0 J Q K V W
花色

0 无花色
2 方块
4 梅花
6 红桃
8 黑桃

'''
visual_char = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'V', 'W']
color_char = ['2', '4', '6', '8']
color_symbol = ['♦', '♣', '♥', '♠']


# 通用内部层 1
'''
A 2 3 4 5 6 7 8 9 0 J Q K V W
1
0E 小王
0F 大王
0x21 - 0x2D 方块 A到K 13张牌
0x41 - 0x4D 梅花 A到K
0x61 - 0x6D
0x81 - 0x8D

0010
0100
0110
1000
'''

min1_char = range(1, 16)




'''
min3表示法
高三位表示花色2 4 6 8，无花色为0
低五位表示牌
A   2   3 4         10   J   Q  K   V   W
14 15   3 。。。     10  11  12 13  16  17
牌必须按值排列，同值无花色在前面
'''

min3_char = [14, 15] + list(range(3, 14)) + [16, 17]
min3_to_visual = dict(zip(min3_char, visual_char))
visual_to_min3 = dict(zip(visual_char, min3_char))
MIN3 = visual_to_min3
MIN3_Q = visual_to_min3['Q']
MIN3_K = visual_to_min3['K']
MIN3_A = visual_to_min3['A']
MIN3_2 = visual_to_min3['2']
MIN3_V = visual_to_min3['V']
MIN3_W = visual_to_min3['W']

MIN3_diamond = list(range((0x02 << 4) + 3, (0x02 << 4) + 16))
MIN3_club = list(range((0x04 << 4) + 3, (0x04 << 4) + 16))
MIN3_heart = list(range((0x06 << 4) + 3, (0x06 << 4) + 16))
MIN3_spade = list(range((0x08 << 4) + 3, (0x08 << 4) + 16))
MIN3_joker = [16, 17]

MIN3_ALL = MIN3_diamond + MIN3_club + MIN3_heart + MIN3_spade + MIN3_joker


def min3_from_color_visual(cards: str):
    if len(cards) % 2:
        return None
    ret = bytearray()
    for i in range(0, len(cards), 2):
        if cards[i+1] == 'V' or cards[i+1] == 'W':
            if cards[i] == '0':
                ret.append(visual_to_min3[cards[i+1]])
            else:
                return None
        elif cards[i] in color_char and cards[i+1] in visual_char:
            ret.append((int(cards[i]) << 4) + visual_to_min3[cards[i+1]])
        else:
            return None
    return ret


# 单色表示
def min3_from_monocolor_visual(cards: str):
    ret = bytearray()
    for c in cards:
        if c in visual_char:
            ret.append(visual_to_min3[c])
        else:
            return None
    return sorted(ret)


def visual_from_monocolor_min3(cards: bytes):
    ret = []
    for b in cards:
        if b in min3_char:
            ret.append(min3_to_visual[b])
        else:
            return None
    return ''.join(ret)


def visual_from_color_min3(cards: bytes):
    """
    注意这里使用的图形表示，不可逆,仅用于打印
    """
    ret = []
    for b in cards:
        color = b >> 5
        num = b & 0x1F
        if num == 16 or num == 17:
            if color == 0:
                ret.append('')
                ret.append(min3_to_visual[num])
            else:
                return None
        elif 1 <= color <= 4 and num in min3_char:
            ret.append(color_symbol[color - 1])
            ret.append(min3_to_visual[num])
        else:
            return None

    return ''.join(ret)


def remove_min3_color(cards):
    """去掉min3 牌表示法的花色"""
    ret = bytearray()
    for c in cards:
        ret.append(c & 0x1F)
    return sorted(ret)


class SplitMachine:
    def __init__(self):
        self.state = 0
        self.cards = []

    def process(self,c):
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


def split_min3(cards):
    """把一手牌分解为一个dict，分别存储4、3、2、1的牌数"""
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


def fisher_yates_shuffle(cards):
    ln = len(cards)
    if ln <= 2:
        return

    for i in range(0, ln - 2):
        j = random.randint(i, ln -1 )
        cards[i], cards[j] = cards[j], cards[i]


def check_has_deal(cards, deal):
    backup = list(cards)
    try:
        for c in deal:
            backup.remove(c)
    except ValueError as e:
        return False
    return True


def remove_deal(cards, deal):
    for c in deal:
        cards.remove(c)