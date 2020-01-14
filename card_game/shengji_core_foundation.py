import card
import enum
from math import floor

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
    副2 -> 15  如果是无主，则都是16,以便小王加关卡牌形成拖拉机

    无主总是用小王来表示！


"""
class ActionResult(enum.IntEnum):
    TEMPORARY = -1 #临时
    FIRST_PLAY = 0
    FOLLOW_PLAY = 1
    DISCARD = 2 #弃牌
    FAIL_TO_BUCKET = 3
    OVERTRUMP  = 4 #毙了


class Pattern(enum.IntEnum):
    """
    单独的牌型类别,包括单牌，对子，多对子，甩牌，不考虑已有手牌和上家出牌
    单牌的权值为这个单牌，去掉花色 如果是主牌就 ｜ 0x40 (即最高变为01），大小王也是如此
    """
    UNKNOWN = -1 #未知
    DISCARD = 0 # 弃牌，没有值的出牌，比方说花色不一样,用于跟牌中
    SINGLE = 1
    PAIR = 2
    PAIR_STRAIGHT = 3
    BUCKET = 4

def is_valid_pattern(pattern: Pattern):
    return pattern != Pattern.INVALID



MAIN_NUMBER_WEIGHT = 16
SUBMAIN_NUMBER_WEIGHT = 15

class ShengjiSuit(enum.IntEnum):
    TRUMP = card.Suit.NON_COLOR
    HEART = card.Suit.HEART
    SPADE = card.Suit.SPADE
    CLUB = card.Suit.CLUB
    DIAMOND = card.Suit.DIAMOND


def _get_shengji_suit_cards(suit : ShengjiSuit, cards, trump_card)->bytearray:
    """
    返回对应升级花色的牌,还是要区分主牌，对吧
    """
    ret = []
    for c in cards:
        if _shengji_suit(c, trump_card) == suit:
            ret.append(c)
    return ret

def _shengji_suit(c, trump_card) -> ShengjiSuit:
    """根据出的牌判断是什么样的升级花色"""
    if _is_trump(c, trump_card):
        return ShengjiSuit.TRUMP
    else:
        return card.get_suit(c)


class CardDescription:
    """
    分两个级别，
    """
    def __init__(self):
        self.action = ActionResult.TEMPORARY
        self.pattern = Pattern.UNKNOWN
        self.weight = 0 #pattern 与weight配合来比较大小
        self.shengji_suit = ShengjiSuit.TRUMP #花色 主、黑桃、红桃、梅花、方块
        self.special_cards = None #甩牌失败的部分 或者全部cards，不一定会有，看特定情况

         


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
    :return: 返回一个CardDescription ;返回None表示非法出牌(花色不一致等)；
        甩牌失败的必须要合理的描述,也是返回一个CardDescription
    """
    assert len(cards), len(hands)==4

    if not _is_consistent(cards, trump_card):
        return None

    cd = CardDescription()
    cards_length = len(cards)
    if cards_length == 1:
        cd.pattern = Pattern.SINGLE
        cd.weight = _weight_of_single(cards[0], trump_card)
    elif cards_length == 2:
        if cards[0] == cards[1]:
            cd.pattern = Pattern.PAIR
            cd.weight = _weight_of_pair(cards, trump_card)
    else:
        # 偶数4个及以上
        cd = _check_pair_straight(cards, trump_card)

    if not cd or cd.pattern == Pattern.UNKNOWN:
        cd = _check_bucket(cards, hands, my_index, trump_card)
    else:
        cd.action = ActionResult.FIRST_PLAY
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
    """判断是否为主，不为主即为副"""
    return c in card.JOKERS or \
        card.get_weight(c) == card.get_weight(trump_card) or \
        card.get_suit(c) == card.get_suit(trump_card)

def _is_all_trump(cards, trump_card) -> bool:
    return bool


def _is_consistent(cards, trump_card) -> bool:
    """全是主牌或者全是同一花色的副牌
    """
    pre_suit = _shengji_suit(cards[0], trump_card)
    for c in cards:
        if pre_suit != _shengji_suit(c,trump_card):
            return False
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
                if cards[i] == cards[i + 1] and _is_continue_weight(cur_weight, pre_weight, trump_card):
                    pre_weight = cur_weight
                else:
                    return None
            cd = CardDescription()
            cd.pattern = Pattern.PAIR_STRAIGHT
            cd.weight = card_len*100+weights[0]
            return cd

def _check_bucket(cards, hands, my_index, trump_card)-> CardDescription:
    """判断是为有效甩牌
        已经验证一致性，且排出了单牌、对子、拖拉机等其它情况，只需验证是否为有效甩牌;
        第一步，将单牌都分解出来
        弟二步，
        :return: CardDescription对象,如果无效甩牌，里面描述包含甩牌失败的部分的牌
    """
    (single_cards, double_cards) = _split_single_and_pair(cards) 

    #需要对double_cards里面的拖拉机进一步拆分，以找出最小的对子/拖拉机
    split_pair_straight = []
    double_weights = _get_weight_cards(double_cards, trump_card)

    one_straight = []
    for i in range(0, len(double_cards)):
        if len(one_straight):
            if _is_continue_weight(double_weights[i-1], double_weights[i], trump_card):
                one_straight.append(double_cards[i])
            else:
                split_pair_straight.append(one_straight)
                one_straight = [double_cards[i]]
        else:
            one_straight.append(double_cards[i])

    if len(one_straight):
        split_pair_straight.append(one_straight)
    #合并，只取最后面的连对和单牌的cd （即最小的那部分）
    tmp_alread_join = []
    final_split_cd = []
    current_shengji_suit = _shengji_suit(cards[0], trump_card)
    
    def get_pair_cd(single_pair) -> CardDescription:
        long_cards = []
        for single_c in single_pair:
            long_cards.append(single_c)
            long_cards.append(single_c)

        cd = CardDescription()
        if len(single_pair) == 1:
            cd.pattern = Pattern.PAIR
            cd.weight = _weight_of_single(single_pair[0],trump_card)
            cd.special_cards = long_cards
        else:
            cd.pattern = Pattern.PAIR_STRAIGHT
            cd.weight = 200*len(single_pair) + _weight_of_single(single_pair[0], trump_card) 
            cd.special_cards = long_cards
        
        cd.shengji_suit = current_shengji_suit
        return cd
        

    if len(single_cards):
        cd = CardDescription()
        cd.pattern = Pattern.SINGLE
        cd.weight = _weight_of_single(single_cards[-1], trump_card)
        cd.shengji_suit = current_shengji_suit 
        cd.special_cards = [single_cards[-1]]
        final_split_cd.append(cd)
    
    for ps in reversed(split_pair_straight):
        if not len(ps) in tmp_alread_join:
            tmp_alread_join.append(len(ps))
            final_split_cd.append(get_pair_cd(ps))
    
    #得到当前升级花色

    #分别判断cd在其它玩家中不是最大的
    def not_the_biggest_part(cd_list, hand_cards, tr)-> list:
        """返回一个排面最小的那个list
            :param list cd_list: 甩牌的描述
            :param bytearray hand_cards: 对应花色的手牌
            :param int tr: 叫主的牌 如果是无主，最高位为1
            :return: cd_list中的部分元素，该部分元素不是最大的
        """

        def is_cd_the_biggest(cd, origin_cards, weight_cards, tr) -> bool:
            """判断单个cd在这一手牌中是否为最大的, 返回True or False
                :param CardDescription cd: 这一出牌描述
                :param list origin_cards: 其它玩家手里的原始牌
                :param list weight_cards: 原始牌对应的权重牌
                :param int tr: 关卡值和花色 
                :return: 返回True表示该cd可以甩出去，即比最大的牌还大
            """
            if len(hand_cards) == 0 :
                return True
            
            # 根据类型单个判断
            if cd.pattern == Pattern.SINGLE:
                return cd.weight >= weight_cards[0]
            elif cd.pattern == Pattern.PAIR:
                possible_cds = _get_valid_pair_follow(origin_cards, weight_cards)
                if len(possible_cds):
                    if cd.weight < possible_cds[0].weight:
                        return False
            elif cd.pattern == Pattern.PAIR_STRAIGHT:
                possible_cds = _get_valid_pair_staight_follow(floor(cd.weight/100), origin_cards,tr)
                if len(possible_cds):
                    if cd.weight < possible_cds[0].weight:
                        return False
            #默认找不到对应的类型，即是最大的 正确
            return True

        weight_cards = _get_weight_cards(hand_cards, tr)
        ret = []
        for cd in cd_list:
            if not is_cd_the_biggest(cd, hand_cards, weight_cards,tr):
                ret.append(cd)
        return ret

    all_bigger = [] #元素为cd
    for i in range(0,3):
        current_index = (my_index+i+1)%4
        target_origin_cards = _get_shengji_suit_cards(current_shengji_suit,hands[current_index],trump_card)
        all_bigger += not_the_biggest_part(final_split_cd, target_origin_cards ,trump_card)

    # 挑选出最右侧（牌面最小的牌）
    min_cd = None
    for cd_i in all_bigger:
        if min_cd:
            if (cd_i.weight % 100) < (min_cd.weight %100):
                min_cd = cd_i
        else:
            min_cd = cd_i
    
    cd = CardDescription()
    if min_cd:
        cd.action = ActionResult.FAIL_TO_BUCKET
        cd.special_cards = min_cd.special_cards
    else:
        cd.action = ActionResult.FIRST_PLAY
        cd.pattern = Pattern.BUCKET
    return cd 


def _get_valid_pair_follow(origin_cards, weight_cards):
    """获得有效的对子跟牌--->这个还可用于托管程序中,最大的cd在前面
    """
    ret = []
    #最多两个牌相等
    pre = None
    for i in range(0, len(origin_cards)):
        if pre is None:
            pre = origin_cards[i]
        else:
            if pre == origin_cards[i]:
                cd = CardDescription()
                cd.pattern = Pattern.PAIR
                cd.weight = weight_cards[i]
                pre = None
                ret.append(cd)
            else:
                pre = origin_cards[i]
    return ret


def _get_valid_pair_staight_follow(length, origin_cards, trump_card):
    """获得有效的对子跟牌--->这个还可用于托管程序中,最大的cd在前面
    :param int length: 拖拉机长度, 4433对应为4
    :param list orgin_cards: 相应花色的牌，且已经排过序了，大的在前面
    :return: cd的列表，大的在前面
    """
    ret = []
    #先找出两两相等的牌
    (singles, pairs) = _split_single_and_pair(origin_cards)
    possibles = len(pairs) - (length/2) #可能的总数
    if possibles > 0:
        weight_cards = _get_weight_cards(pairs, trump_card)
        for i in range(0, possibles):
            pre = weight_cards[i]
            is_continue = True
            for j in range(1, length/2):
                if _is_continue_weight(pre, weight_cards[i+j]):
                    pre = weight_cards[i+j]
                else:
                    is_continue = False
                    break
            if is_continue:
                cd = CardDescription()
                cd.pattern = Pattern.PAIR_STRAIGHT
                cd.weight = length*100 + weight_cards[i]
                ret.append(cd)
    return ret


def _split_single_and_pair(cards):
    """找出所有单牌和对子
    :param list cards: 原始牌且已经排序过了
    :return: (single, double)的pair，内部元素都是list
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
    
    return (single_cards, double_cards)


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
    """返回对应单牌的权重，注意权重一致并不能说明是一样的牌（都是副2的情况）"""
    return list(map(lambda c: _weight_of_single(c, trump_card), cards))


def _is_continue_weight(bigger, smaller, trump_card) -> bool:
    """判断weight值是否连续
    """
    trump_weight = card.get_weight(trump_card)
    if smaller >= trump_weight or \
        bigger <= trump_card or \
        (bigger == trump_weight+1 and smaller + 1 == trump_weight):
        return True
    else:
        return False