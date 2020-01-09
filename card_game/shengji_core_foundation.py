import card
import enum

"""提供基础函数来判断牌型、大小关系等基础行为
- 接口
    sort_by_shengji : 按照升级规则的排序，大的在前面，通过将主牌最高位设为1来实现
    first_play : 判断出牌是否有效
    follow_play : 判断跟牌是否有效
    dig_point : 扣底得分
    RoundResult 类: 一轮出牌的结果
    * 所有要出的牌都已经过手牌检查和排序！

- 原理
    weight就是这个牌的去除花色的值，因为A为14，打几几就用15！不区分主牌的情况,如何区分正2，副2？
    正2 -> 16
    副2 -> 15  如果是无主，则都是15

    无主总是用小王来表示！


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
    UNKNOWN = -1 #未知
    NO_MEANING = 0 # 没有值的出牌，比方说花色不一样,用于跟牌中
    SINGLE = 1
    PAIR = 2
    PAIR_STRAIGHT = 3
    BUCKET = 4

def is_valid_pattern(pattern: Pattern):
    return pattern != Pattern.INVALID



MAIN_NUMBER_WEIGHT = 16
SUBMAIN_NUMBER_WEIGHT = 15

class CardDescription:
    """
    分两个级别，
    """
    def __init__(self):
        self.pattern = Pattern.NO_MEANING
        self.weight = 0 #pattern 与weight配合来比较大小
        self.actionResult = ActionResult.Unknown 


#对外接口


class RoundResult:
    """一轮出牌的结果
    max_index :谁最大
    point : 得分，如果没有得分即得分为0分
    point_cards : 具体得分的牌
    """
    def __init__(self):
        self.max_index = -1
        self.point = 0 
        self.point_cards = []


def sort_by_shengji(cards, trump_card) -> bytearray:
    def _sort_shengji_compare_value(c):
        #只用于排序，需要将花色考虑进去 花色大于weight
        weight = _weight_of_single(c, trump_card)
        weight =  weight + ((c >> card.SUIT_SHIFT) << card.SUIT_SHIFT)
        if _is_trump(c, trump_card): #主的花色又需要移除
            return (weight | 0b10000000) & 0b10011111
        else:
            return weight

    s_list = sorted(cards, key=_sort_shengji_compare_value, reverse=True)
    return bytearray(s_list)


def first_play(cards, hands: list, my_index,  trump_card) -> CardDescription:
    """
    cards: 将要出的牌
    hands: 是所有玩家的牌
    my_index: 自己的牌排在玩家中的序号
    trump_card: 主牌 如果是无主，则最高位为1
    return: 返回一个CardDescription ,返回None表示非法出牌，或其它异常
    """
    assert len(cards), len(all_players)==4

    cd = CardDescription()
    if not _is_consistent(cards, trump_card):
        cd.actionResult = ActionResult.Invalid
        return cd

    cards_length = len(cards)
    if cards_length == 1:
        cd.pattern = Pattern.SINGLE
        cd.weight = _weight_of_single(cards, trump_card)
    elif cards_length == 2:
        if cards[0] == cards[1]:
            cd.pattern = Pattern.PAIR
            cd.weight = _weight_of_pair(cards, trump_card)
    else:
        # 偶数4个及以上
        cd = _check_pair_straight(cards, trump_card)
    if not cd or cd.pattern == Pattern.UNKNOWN:
        cd = _check_bucket(cards, hands, my_index, trump_card) 
    return cd



def follow_play(cards, first_cd, hand_cards, main_card) -> CardDescription:
    """
    return: None表示出牌无效
    """
    return None


def round_over(cd_list:list, first_index: int, host_index: int) -> bool :
    """
    一轮出牌结束后的结果对比
    """
    return True


def dig_point(big_cd, back_cards) -> int:
    """big_cd :最后一轮出牌
    """


def compare_cd(cd_list: list) -> int:
    """
    cd_list: 第一个人的出牌放在前面
    比较cd_list中的cd，返回最大的那个牌的序号，
    """
    pass


def decide_point(cards_list: list, host_index: int, great_index: int):
    """
    根据出牌编号，和大牌编号得出得分与否返回一个pair.(cards, point),即得分牌和总分
    """
    pass

def _is_trump(c, trump_card) -> bool:
    return c in card.JOKERS or \
        card.get_weight(c) == card.get_weight(trump_card) or \
        card.get_suit(c) == card.get_suit(trump_card)

def _is_all_trump(cards, trump_card) -> bool:
    return bool


def _is_consistent(cards, trump_card) -> bool:
    """全是主牌或者全是副牌
    """
    return True


def _weight_of_single(c, trump_card):

    if c in card.JOKERS :
        return c
    else:
        if card.get_weight(c) == card.get_weight(trump_card):
            #判断花色是否一样
            if card.get_suit(c) == card.get_suit(trump_card) or \
                card.get_suit(trump_card) == card.Suit.NON_COLOR:
                #如果是无主，则统一变为主2
                return MAIN_NUMBER_WEIGHT
            else:
                return SUBMAIN_NUMBER_WEIGHT
        else:
                return card.get_weight(c)

def _weight_of_pair(cards, main_color):
    return _weight_of_single(cards[0], main_color)

def _check_pair_straight(cards, trump_card) -> CardDescription:
    """判断是否为拖拉机（已经确保全副或全主了）
        先确保两两相等
        载确保全副或者全主,
    """
    card_len = len(cards)
    if card_len >= 4 and not card_len % 2:
        weights = _get_weight_cards(cards, trump_card)
        if cards[0] == cards[1]:
            pre_weight = weights[0]
            for i in range(2, len(cards), 2):
                cur_weight = weights[i]
                if cards[i] == cards[i + 1] and _is_continue(cur_weight, pre_weight, trump_card):
                    pre_weight = cur_weight
                else:
                    return None
            cd = CardDescription()
            cd.pattern = Pattern.PAIR_STRAIGHT
            cd.weight = card_len*100+weights[0]
            return cd

def _check_bucket(cards, hands, my_index, trump_card)-> CardDescription:
    """判断是为有效甩牌
        已经验证一致性，且排斥了单牌、对子、拖拉机了;第一步分解，将单牌都分解出来
    """
    single_cards = []
    double_cards = []
    pre = cards[0]
    for i in range(1, len(cards)):
        if pre is None:
            pre = cards[i]
        else:
            if cards[i] == pre:
                double_cards.append(pre)
                pre = None
            else:
                single_cards.append(pre)
                pre = cards[i]

    if not pre is None:
        single_cards.append(pre)

    #需要对double_cards里面的拖拉机进一步拆分，以找出最小的对子/拖拉机

    return None




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
    elif (cards_len % 2) == 0:
        #判断是否为拖拉机
        pass
    else:
        #耍牌的情形
        pass
    return cd


def _get_weight_cards(cards, trump_card) -> list:
    return list(map(lambda c: _weight_of_single(c, trump_card), cards))


def _is_continue(bigger, smaller, trump_card) -> bool:
    trump_weight = card.get_weight(trump_card)
    if smaller >= trump_weight or \
        bigger <= trump_card or \
        (bigger == trump_weight+1 and smaller + 1 == trump_weight):
        return True
    else:
        return False