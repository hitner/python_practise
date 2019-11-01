import card
import enum

"""
提供基础函数来判断牌型、大小关系等基础行为
"""
class ActionResult(enum.IntEnum):
    Unknown = -1 #未知
    Invalid = 0
    NormalPlay = 1 #正常出牌，包括跟牌
    Bucket = 2
    Abandoned = 3  #跟甩牌的，不是弃牌就是毙了
    MasterOver = 4  # 毙了
    FailToBucket = 5  # 甩牌失败

class Pattern(enum.IntEnum):
    """
    单独的牌型类别,包括单牌，对子，多对子，甩牌，不考虑已有手牌和上家出牌
    单牌的权值为这个单牌，去掉花色 如果是主牌就 ｜ 0x40 (即最高变为01），大小王也是如此
    """
    NO_MEANING = 0 # 没有值的出牌，比方说花色不一样
    SINGLE = 1
    PAIR = 2
    MULTI_PAIR = 3
    BUCKET = 4

def is_valid_pattern(pattern: Pattern):
    return pattern != Pattern.INVALID


class CardDescription:
    """
    分两个级别，
    """
    def __init__(self):
        self.pattern = Pattern.NO_MEANING
        self.weight = 0
        self.actionResult = ActionResult.Unknown


def first_play(all_players: list, main_color: card.Color, cards) -> CardDescription:
    """
    all_players: 是所有玩家的牌，自己的牌排在第一位
    main_color: 主花色，无主为-1,
    cards: 将要出的牌,
    return: 返回一个CardDescription ,返回None表示非法出牌，或其它异常
    """
    assert len(cards), len(all_players)==4
    my_hand_cards = all_players[0]
    if card.bin_cards_has_subcards(my_hand_cards, cards) :




def follow_play(first_cd, remain_cards, main_color: card.Color, cards):
    """
    return: None表示出牌无效
    """
    pass


def compare_cd(cd_list: list) -> int:
    """
    cd_list: 第一个人的出牌放在前面
    比较cd_list中的cd，返回最大的那个牌的序号，
    """
    pass


def decide_point(cards_list: list, host_index: int, great_index: int):
    """
    根据专家编号，和大牌编号得出得分与否返回一个pair.(cards, point),即得分牌和总分
    """
    pass


def _weight_of_single(cards, main_color):
    if cards[0] == card.BLACK_JOKER or cards[0] == card.RED_JOKER \
        or card.get_color(cards[0]) == main_color:
        return (cards[0] & 0x3F ) | 0x40
    else:
        return cards[0] & 0x3F

def _card_description_of_two(cards, main_color):
    cd = CardDescription()
    if cards[0] == cards[1]:
        cd.pattern = Pattern.PAIR
        cd.weight = _weight_of_single(cards, main_color)
    return cd

def _get_static_card_description(cards, main_color):
    """
    静态检查，看看是哪种类型，
    :param cards: 已确保长度大于0
    :return:
    """
    cards_len = len(cards)
    cd = CardDescription()
    if cards_len == 1:
        cd.pattern = Pattern.SINGLE
        cd.weight = _weight_of_single(cards, main_color)
    elif cards_len == 2:
        cd = _card_description_of_two(cards, main_color)

    return cd