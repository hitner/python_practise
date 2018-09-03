

class CardDescription:
    """一手有效出牌的描述"""
    def __init__(self, pattern=0, weight=0):
        self.pattern = pattern
        self.weight = weight


"""
牌型 一个人最多54-3 = 51  51/3=17 最多20张
101， 单排
105 - 112 顺子最多为 3-A 
"""
patterns_single = [101]
patterns_single_straight = list(range(105, 113))
patterns_pair = [202]
patterns_pair_straight = list(range(206, 221, 2))
patterns_triple = list(range(303, 321, 3))
patterns_triple_single = list(range(404, 421, 4))
patterns_triple_pair = list(range(505, 521, 5))
patterns_four_two = list(range(606, 621, 6))
patterns_four_pairs = list(range(708, 721, 8))
patterns_bomb = [2, 4]

patterns_all = patterns_bomb + \
               patterns_single + patterns_single_straight + \
               patterns_pair + patterns_pair_straight + \
               patterns_triple + patterns_triple_single + patterns_triple_pair + \
               patterns_four_two + patterns_four_pairs


def _check_grand_bomb(cards):
    if cards[0] == poker.MIN3['V'] and cards[1] == poker.MIN3['W']:
        return CardDescription(2, cards[0])


def _check_bomb(cards):
    if cards[0] == cards[1] == cards[2] == cards[3]:
        return CardDescription(4, cards[0])


def _check_single(cards):
    return CardDescription(101, cards[0])


def _check_single_straight_(cards):
    pre = cards[0]
    for i in range(1, len(cards)):
        if pre + 1 == cards[i]:
            pre = cards[i]
        else:
            return None
    return CardDescription(100 + len(cards), cards[0])


def _check_pair(cards):
    if cards[0] == cards[1]:
        return CardDescription(202, cards[0])


def _check_pair_straight(cards):
    if cards[0] == cards[1]:
        pre = cards[0]
        for i in range(2,len(cards),2):
            if cards[i] == cards[i+1] and pre+1 == cards[i]:
                pre = cards[i]
            else:
                return None
        return CardDescription(200+len(cards), cards[0])


def _check_triple(cards):
    if cards[0] == cards[1] == cards[2]:
        pre = cards[0]
        for i in range(3, len(cards), 3):
            if cards[i] == cards[i+1] == cards[i+2] and pre+1 == cards[i]:
                pre = cards[i]
            else:
                return None
        return CardDescription(300 + len(cards), cards[0])


def _check_triple_single(cards):
    pass


def _check_triple_pair(cards):
    pass


def _check_four_two(cards):
    pass


def _check_four_pairs(cards):
    """
    四个一样的牌不允许拆分，防止歧义
    """
    for i in range(0, len(cards), 2):
        if cards[i] != cards[i+1]:
            return None
    #寻找4个一样的牌的list
    fours = []
    for i in range(0, len(cards), 4):
        if cards[i] == cards[i+2]:
            fours.append(cards[i])

    if len(fours) == len(cards)/8:
        pre = fours[0]
        if i in range(1, len(fours)):
            if fours[i] == pre:
                pre = fours[i]
            else:
                return None
        return CardDescription(700+len(cards), fours[0])






_pattern_map_check = [([2], _check_grand_bomb),
                      ([4], _check_bomb),
                      (patterns_single, _check_single),
                      (patterns_single_straight, _check_single_straight_),
                      (patterns_pair, _check_pair),
                      (patterns_pair_straight, _check_pair_straight),
                      (patterns_triple, _check_triple),
                      (patterns_triple_single, _check_triple_single),
                      (patterns_triple_pair, _check_triple_pair),
                      (patterns_four_two, _check_four_two),
                      (patterns_four_pairs, _check_four_pairs)]


def _get_function_from_pattern(p):
    """由pattern得到检查函数"""
    for one_tuple in _pattern_map_check:
        if p in one_tuple[0]:
            return one_tuple[1]


"""
生成length到函数的字典
"""
_length_to_pattern_functions = {}


def _add_to_length_functions_dict(length: int, f):
    if length in _length_to_pattern_functions:
        _length_to_pattern_functions[length].append(f)
    else:
        _length_to_pattern_functions[length] = [f]


"""
引入代码时执行，初始化dict
"""
for one in _pattern_map_check:
    for pattern_ in one[0]:
        _add_to_length_functions_dict(pattern_ % 100, one[1])


def _check_all_possible(cards) -> CardDescription:
    """
    检查牌型的所有可能
    """
    if len(cards) not in _length_to_pattern_functions:
        return None
    functions = _length_to_pattern_functions[len(cards)]
    for f in functions:
        result = f(cards)
        if result:
            return result


def check_value_deal(cards, cd=None) -> CardDescription:
    """
    :param cards: 牌,必须是min3型 (从小到大排序）
    :param cd: 先前的牌型描述，None表示首次出牌
    :return:
    """
    if cd:
        f = _get_function_from_pattern(cd.pattern)
        result = f(cards)
        if result:
            pass
    else:
        result = _check_all_possible(cards)
        return result


import poker


#check_value_deal(poker.min3_from_monocolor_visual('9900JJ'))