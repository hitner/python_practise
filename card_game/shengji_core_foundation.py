import card
import enum
from math import floor
from itertools import combinations

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
"""


MAIN_NUMBER_WEIGHT = 16
SUBMAIN_NUMBER_WEIGHT = 15


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
    FAIL_TO_BUCKET = 5
    OVERTRUMP  = 6


class ShengjiSuit(enum.IntEnum):
    TRUMP = card.Suit.NON_COLOR
    HEART = card.Suit.HEART
    SPADE = card.Suit.SPADE
    CLUB = card.Suit.CLUB
    DIAMOND = card.Suit.DIAMOND


class CardDescription:
    def __init__(self):
        self.pattern = Pattern.UNKNOWN
        self.weight = 0 #pattern 与weight配合来比较大小
        self.shengji_suit = ShengjiSuit.TRUMP #花色 主、黑桃、红桃、梅花、方块
        self.origin_cards = None #原始的出牌，注意甩牌失败的时候，为强制出牌的部分
        self.bucket_structure = None #可选 甩牌的结构;结构长的在前面
        self.remain_same_suit = None #可选 剩余的同花色牌,用于甩牌的跟牌判断中

         


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


def sort_by_shengji(cards, trump_card) -> list:
    """生成一个新的list"""
    def _sort_shengji_compare_value(c):
        #只用于排序，需要将花色考虑进去 花色大于weight
        weight = _weight_of_single(c, trump_card)
        weight =  weight + ((c >> card.SUIT_SHIFT) << card.SUIT_SHIFT)
        if _is_trump(c, trump_card): #主的花色又需要移除
            return (weight | 0b10000000) & 0b10011111
        else:
            return weight

    s_list = sorted(cards, key=_sort_shengji_compare_value, reverse=True)
    return s_list


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

    cd = None
    cards_length = len(cards)

    if cards_length == 1:
        cd = _check_single(cards,trump_card) 
    elif cards_length == 2:
        cd = _check_pair(cards, trump_card)
    else:
        # 偶数4个及以上
        cd = _check_pair_straight(cards, trump_card)

    if not cd:
        cd = _check_bucket(cards, hands, my_index, trump_card)
    return cd



def follow_play(cards, first_cd, hand_cards, trump_card) -> CardDescription:
    """
    :param list cards:将要出的牌（已经排过序了），并且已验证过牌都有
    :param CardDescription first_cd:第一家出牌的描述
    :param list hand_cards: 自己手里的手牌
    :param int trump_card:主花色
    :return: None表示出牌无效，返回一个CardDescription表示有效出牌
    """
    #1 判断数量是否满足要求
    play_cards_len = len(cards)
    if play_cards_len != len(first_cd.origin_cards):
        return None
    
    #2 判断花色是否满足要求

    suit_hands = _get_shengji_suit_cards(first_cd.shengji_suit, hand_cards, trump_card)
    if play_cards_len <= len(suit_hands):
        #要出的牌必须全部在suit_hands中间
        if not card.contain_subcard( suit_hands, cards):
            return None
        
        suit_weight_hands = _get_weight_cards(suit_hands, trump_card)
        #判断模式是否符合要求
        if first_cd.pattern == Pattern.SINGLE:
            #单牌总是可以的
            return _check_single(cards, trump_card)
        elif first_cd.pattern == Pattern.PAIR:
            #检查suit_hands里面有没有对子
            possible_cds = _get_valid_pair_follow(suit_hands,trump_card)
            if len(possible_cds):
                #有对子，则是对子或者无效出牌
                return _check_pair(cards, trump_card) 
        elif first_cd.pattern == Pattern.PAIR_STRAIGHT:
            #检查suit_hands里面有没有拖拉机
            possible_cds = _get_valid_pair_straight_follow(len(first_cd.origin_cards), \
                suit_hands,suit_weight_hands)
            if len(possible_cds):
                return _check_pair_straight(cards, trump_card)
            else:
                #没有符合要求的拖拉机，那么必须要有对子出对子,拆分为对子列表进行刷牌处理
                split_cd_list = _split_pair_straight_to_pair_list_cd(first_cd, trump_card)
                possible_cds = _possible_follow_to_cd_list(split_cd_list,suit_hands,trump_card)
                if not _is_play_in_possible(cards,possible_cds):
                    return None
        else:
            #第一个出牌甩牌的情形，必须有对出对，有拖拉机出拖拉机
            return _check_bucket_follow(cards,first_cd, suit_hands, trump_card)
    else:
        #牌数量不足，属于要不起或者毙了的情况
        if not card.contain_subcard(cards, suit_hands):
            #suit_hands必须要在cards里面，全部出去
            return None

        # 判断是毙了还是一般的弃牌
        # 毙了的要求是first_cd为副，我全是主（一致性满足），且模式也能够对应的上
        if first_cd.shengji_suit != ShengjiSuit.TRUMP and \
            _is_all_trump(cards, trump_card):
            return _check_overtrump_follow(cards, first_cd, trump_card)
    
    #没有返回None和有效cd的情况，剩下就是弃牌了
    cd = CardDescription()
    cd.pattern = Pattern.DISCARD
    cd.origin_cards = list(cards)
    return cd




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


def possible_follow_to(cd, hands, tr):
    """注意与valid_follow的区别,这里弃牌也算是一种可能
    :param CardDescription cd: pattern可能为Single/Pair/Pair_Straight/Bucket
    :param list hands:相同花色的牌，且数量大于需要出的牌 若cd为弃牌，可能的跟牌全部是弃牌
    :return: 返回一个列表，里面是cd，pattern是SINGLE/PAIR/PAIR_STRAIGHT/DISCARD的一种
    非DISCARD大weight在前面
    """
    ret = []
    if cd.pattern == Pattern.SINGLE:
        for c in hands:
            new_cd = _check_single([c], tr)
            new_cd.remain_same_suit = card.new_after_remove(hands, new_cd.origin_cards)
            ret.append(new_cd)
    elif cd.pattern == Pattern.PAIR:
        possibles = _get_valid_pair_follow(hands, tr)
        if len(possibles):
            for one_pos in possibles:
                one_pos.remain_same_suit = card.new_after_remove(hands, one_pos.origin_cards)
            ret = possibles
        else:
            #需要降级，只需要任何两个牌就可以了，因为两两不一致，就是组合的情况
            for one_combine in combinations(hands, 2):
                new_cd = CardDescription()
                new_cd.pattern = Pattern.DISCARD
                new_cd.origin_cards = list(one_combine)
                new_cd.remain_same_suit = card.new_after_remove(hands, one_combine)
                ret.append(new_cd)
    elif cd.pattern == Pattern.PAIR_STRAIGHT:
        weight_cards = _get_weight_cards(hands,tr)
        possibles = _get_valid_pair_straight_follow(len(cd.origin_cards),hands, weight_cards)
        if len(possibles):
            for one_pos in possibles:
                new_cd.remain_same_suit = card.new_after_remove(hands, one_pos.origin_cards)
            ret = possibles
        else:
            #需要降级，只需要对子就可以了，故将该cd转化为一个PAIR_STRAIGHT列表继续本过程
            split_cd_list = _split_pair_straight_to_pair_list_cd(cd, tr) 
            ret = _possible_follow_to_cd_list(split_cd_list, hands, tr)
    else:
        #甩牌的情形
        ret = _possible_follow_to_cd_list(cd.bucket_structure, hands, tr)

    return ret
                 

def _possible_follow_to_cd_list(cd_structure, suit_hands, trump_card) -> list :
    """可能的出牌,可用于AI中
    :param list cd_structure: cd列表，长度长的在前面 拖拉机、对子、单牌的顺序,
        如果只有一个元素，则是单个的出牌；如果多个元素，即是甩牌（已验证了甩牌成功)
    :param list suit_hands: 该类花色列表，已确保数量足够
    :return: 返回一个列表,元素是一个cd：origin_card就是可出的牌，remain_same_suit就是剩余的牌
    """
    def merge_head_trails(head_cd, trail_cds):
        """ 合并而成的必定是甩牌的跟牌（弃牌），且不是毙了的情况
        :param CardDescription head_cd: 单个头部cd
        :param list trail_cds: 列表，需要拼接起来
        :return: 返回一个list，每个元素是一个CardDescription
        """
        ret = []
        for cd in trail_cds:
            new_cd = CardDescription()
            new_cd.pattern = Pattern.DISCARD
            new_cd.origin_cards = sort_by_shengji(head_cd.origin_cards + cd.origin_cards, trump_card)
            new_cd.remain_same_suit = cd.remain_same_suit
            ret.append(new_cd)

        #去除重复的项目
        return _remove_duplicate_cd(ret)

    possible_for_heads = possible_follow_to(cd_structure[0], suit_hands, trump_card)
    if len(cd_structure) > 1:
        ret = []
        for cd_in_head in possible_for_heads:
            possible_for_trails = _possible_follow_to_cd_list(cd_structure[1:], \
                 cd_in_head.remain_same_suit, trump_card)
            ret += merge_head_trails(cd_in_head, possible_for_trails)
        return _remove_duplicate_cd(ret)
    else:
        return possible_for_heads


def _remove_duplicate_cd(cd_list) -> list:
    """删除重复的cd"""
    ret2 = []
    for cd in cd_list:
        if not any([card.is_equal(one.origin_cards,cd.origin_cards) for one in ret2]):
            ret2.append(cd)
    return ret2 


def _is_play_in_possible(cards, possible_cds) -> bool:
    """判断此处出牌是否属于可能的出牌列表中
    :param list possible_cds:
    """
    assert(len(possible_cds))
    for cd in possible_cds:
        if card.is_equal(cd.origin_cards,cards):
            return True
    return False
    


def _get_shengji_suit_cards(suit : ShengjiSuit, cards, trump_card)->list:
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



def _is_trump(c, trump_card) -> bool:
    """判断是否为主，不为主即为副"""
    return c in card.JOKERS or \
        card.get_weight(c) == card.get_weight(trump_card) or \
        card.get_suit(c) == card.get_suit(trump_card)

def _is_all_trump(cards:list, trump_card) -> bool:
    for c in cards:
        if not _is_trump(c,trump_card):
            return False
    return True
        


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


def _check_single(cards, trump_card):
    """生成单牌的cd"""
    cd = CardDescription()
    cd.pattern = Pattern.SINGLE
    cd.weight = _weight_of_single(cards[0], trump_card)
    cd.shengji_suit = _shengji_suit(cards[0], trump_card)
    cd.origin_cards = list(cards)
    return cd 

def _check_pair(cards, trump_card):
    """如果不是对子就返回None"""
    if cards[0] == cards[1]:
        cd = CardDescription()
        cd.pattern = Pattern.PAIR
        cd.weight = _weight_of_pair(cards, trump_card)
        cd.shengji_suit = _shengji_suit(cards[0], trump_card)
        cd.origin_cards = list(cards)
        return cd
    else:
        return None

def _check_pair_straight(cards, trump_card) -> CardDescription:
    """判断是否为拖拉机（已经确保全副或全主了）
        先确保两两相等
        然后再确保连续
    :return:None表示不是拖拉机
    """
    card_len = len(cards)
    if card_len >= 4 and not card_len % 2:
        weights = _get_weight_cards(cards, trump_card)
        if cards[0] == cards[1]:
            pre_weight = weights[0]
            for i in range(2, len(cards), 2):
                cur_weight = weights[i]
                if cards[i] == cards[i + 1] and _is_continue_weight(pre_weight,cur_weight,trump_card):
                    pre_weight = cur_weight
                else:
                    return None
            cd = CardDescription()
            cd.pattern = Pattern.PAIR_STRAIGHT
            cd.weight = card_len*100+weights[0]
            cd.shengji_suit = _shengji_suit(cards[0], trump_card)
            cd.origin_cards = list(cards)
            return cd

def _check_bucket(cards, hands, my_index, trump_card)-> CardDescription:
    """判断是为有效甩牌,已经验证一致性，且排出了单牌、对子、拖拉机等其它情况，
    只需验证是否为有效甩牌;
        :return: CardDescription对象,如果无效甩牌，里面描述包含甩牌失败的部分的牌
    """
    #第一步：拆分出单牌和对子
    (single_cards, double_cards) = _split_single_and_pair(cards) 

    #第二步：对double_cards里面的拖拉机进一步拆分，以找出最小的对子/拖拉机
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
    #第三步：取最小的（最后面的）连对和单牌，生成对应的cd
    tmp_alread_join = []
    final_split_cd = []
    current_shengji_suit = _shengji_suit(cards[0], trump_card)

    if len(single_cards):
        cd = _check_single(single_cards[-1:], trump_card)
        final_split_cd.append(cd)
    
    for ps in reversed(split_pair_straight):
        if not len(ps) in tmp_alread_join:
            tmp_alread_join.append(len(ps))
            final_split_cd.append(_create_pair_or_pair_straight_cd(ps, trump_card))

    #第四步：拿最小的cd列表去下家中验证是否是最大的，找出不是最大的cd
    not_the_biggest_cd = [] #元素为cd
    for i in range(0,3):
        current_index = (my_index+i+1)%4
        target_origin_cards = _get_shengji_suit_cards(current_shengji_suit,hands[current_index],trump_card)
        not_the_biggest_cd += _not_the_biggest_part(final_split_cd, target_origin_cards ,trump_card)

    #第五步：挑选出最右侧的（牌面最小的牌）
    min_cd = None
    for cd_i in not_the_biggest_cd:
        if min_cd:
            if (cd_i.weight % 100) < (min_cd.weight %100):
                min_cd = cd_i
        else:
            min_cd = cd_i

    #第六步：生成目标cd
    cd = CardDescription()
    if min_cd:
        cd.pattern = Pattern.FAIL_TO_BUCKET
        cd.origin_cards = min_cd.origin_cards
    else:
        cd.pattern = Pattern.BUCKET
        cd.origin_cards = cards
        cd.shengji_suit = _shengji_suit(cards[0], trump_card)
        cd.bucket_structure = _create_bucket_structure(split_pair_straight, single_cards,trump_card)
    return cd 


def _check_overtrump_follow(cards:list, first_cd: CardDescription, trump_card:int) -> CardDescription:
    """判断是否成功毙了，如果没有成功则返回弃牌
    前提：cards全是主牌，且first_cd出的是副牌（即自己没有副牌了）
    :param list cards: 出的牌
    :param CardDescription first_cd: 第一个玩家的出牌
    :param int trump_card: 关卡牌
    :return: 始终返回一个CardDescription,若成功毙了pattern为OVERTRUMP，否则为DISCARD
    """
    cd = None
    if first_cd.pattern == Pattern.SINGLE:
        cd = _check_pair(cards, trump_card)
    elif first_cd.pattern == Pattern.PAIR:
        cd = _check_pair(cards, trump_card)
    elif first_cd.pattern == Pattern.PAIR_STRAIGHT:
        cd = _check_pair_straight(cards, trump_card)
    else:
        assert(first_cd.pattern == Pattern.BUCKET)
        #第一个取最大的，后续只要有就可以了
        finnal_weight = None
        possible_cds = possible_follow_to(first_cd.bucket_structure[0],cards,trump_card)
        if possible_cds[0].pattern != Pattern.BUCKET:
            finnal_weight = possible_cds[0].weight

        cards_remain = cards
        mode_obey = True
        for one_cd in first_cd.bucket_structure:
            if one_cd.pattern == Pattern.SINGLE:
                break
            else:
                possible_cds = possible_follow_to(one_cd,cards_remain,trump_card)
                if possible_cds[0].pattern == Pattern.BUCKET:
                    mode_obey = False
                    break

        if mode_obey:
            cd = CardDescription()
            cd.weight = finnal_weight
            cd.shengji_suit = ShengjiSuit.TRUMP
            cd.origin_cards = cards
        
    if cd:
        cd.pattern = Pattern.OVERTRUMP
    else:
        cd = CardDescription()
        cd.pattern = Pattern.DISCARD
        cd.origin_cards = cards
    return cd


def _not_the_biggest_part(cd_list, hand_cards, tr)-> list:
    """返回一个排面最小的那个list
        :param list cd_list: 甩牌的最小描述，只是取拖拉机/对子/单牌中的最小者
        :param list hand_cards: 对应花色的手牌
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
            possible_cds = _get_valid_pair_follow(origin_cards, tr)
            if len(possible_cds):
                if cd.weight < possible_cds[0].weight:
                    return False
        elif cd.pattern == Pattern.PAIR_STRAIGHT:
            possible_cds = _get_valid_pair_straight_follow(floor(cd.weight/100), origin_cards,tr)
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


def _check_bucket_follow(cards,first_cd, suit_hands, trump_card):
    """检查甩牌的跟牌
    前提：手牌该类花色数量大于所需出牌数
    :param CardDescription first_cd
    :param list suit_hands: 该部分花色牌，数量大于cards
    :return: None无效出牌；CardDescription pattern DISCARD, 正常的弃牌
    """
    possible_follows = possible_follow_to(first_cd, suit_hands, trump_card)
    if _is_play_in_possible(cards, possible_follows):
        cd = CardDescription()
        cd.pattern = Pattern.DISCARD
        cd.origin_cards = cards
        return cd


def _get_valid_pair_follow(origin_cards, trump_card):
    """获得有效的对子跟牌--->这个还可用于托管程序中,最大的cd在前面
    :param list origin_cards: 原始牌
    :return: 返回的是一个cd list，
    """
    ret = []
    #最多两个牌相等
    pre = None
    for i in range(0, len(origin_cards)):
        if pre is None:
            pre = origin_cards[i]
        else:
            if pre == origin_cards[i]:
                pre = None
                ret.append(_check_pair(origin_cards[i-1:i+1],trump_card))
            else:
                pre = origin_cards[i]
    return ret


def _get_valid_pair_straight_follow(length, origin_cards, trump_card):
    """获得有效的对子跟牌--->这个还可用于托管程序中,最大的cd在前面，
    并且必须是拖拉机跟拖拉机；拖拉机跟对子的降级情形这里未考虑
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

def _split_pair_straight_to_pair_list_cd(pair_straight_cd: CardDescription, trump_card) -> list:
    """将一个拖拉机拆分为单个的对子cd list，以用于寻找可能的对子可能跟牌"""
    ret = []
    for i in range(0, len(pair_straight_cd.origin_cards), 2):
        cd = _check_pair(pair_straight_cd.origin_cards[i:i+2],trump_card)
        ret.append(cd)
    return ret

def _create_pair_or_pair_straight_cd(single_pair, trump_card) -> CardDescription:
    """
    :param list single_pair: 对子的单牌表示，由前面split导致的
    """
    long_cards = []
    for single_c in single_pair:
        long_cards.append(single_c)
        long_cards.append(single_c)

    
    if len(single_pair) == 1:
        cd = _check_pair(long_cards,trump_card)
    else:
        # cd = _check_pair_straight(long_cards, trump_card) 
        # 加快生成速度
        cd = CardDescription()
        cd.pattern = Pattern.PAIR_STRAIGHT
        cd.weight = 200*len(single_pair) + _weight_of_single(single_pair[0], trump_card) 
        cd.origin_cards = long_cards
        cd.shengji_suit = _shengji_suit(single_pair[0], trump_card)
    
    return cd


def _create_bucket_structure(single_pair_list:list, single_list, trump_card) -> list:
    """创建一个大拖拉机在前面的 甩牌描述，这个描述用于检查后续的跟牌是否有效
    :param list single_pair_list: 每一个元素是一个连子的list.完整的例子如[[Q],[5,4,3] [2]]
    :return: 将single_pair_list长度长的连队提到前面去，并且保证稳定性，返回一个新的list
    """
    ret = []
    single_pair_list.sort(key = lambda x: len(x))
    for one_single_pair in single_pair_list:
        cd = _create_pair_or_pair_straight_cd(one_single_pair, trump_card)
        ret.append(cd)
    
    for one_single in single_list:
        cd = _check_single([one_single], trump_card)
        ret.append(cd)
    return ret



def _get_weight_cards(cards, trump_card) -> list:
    """返回对应单牌的权重列表，注意权重一致并不能说明是一样的牌（都是副2的情况）"""
    return list(map(lambda c: _weight_of_single(c, trump_card), cards))


def _is_continue_weight(bigger, smaller, trump_card) -> bool:
    """判断weight值是否连续
    """
    trump_weight = card.get_weight(trump_card)
    if smaller >= trump_weight or bigger <= trump_weight:
        return bigger == smaller + 1
    else:
        return bigger == smaller+2