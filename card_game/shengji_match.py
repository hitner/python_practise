import card

class CardDescription:
    def __init__(self):
        self.partern = 0
        self.weight = 0
        self.is_main = False



def first_play(all_players:list, main_color:card.Color, cards):
    """
    all_players: 是所有玩家的牌，自己的牌排在第一位
    main_color: 主花色，无主为-1,
    cards: 将要出的牌
    return: None表示出牌失败，0 表示甩牌失败 和成功 CardDescription
    """
    pass


def follow_play(first_cd, remain_cards, main_color:card.Color, cards):
    """
    return: None表示出牌无效
    """
    pass


def compare_cd(cd_list:list) -> int:
    """
    cd_list: 第一个人的出牌放在前面
    比较cd_list中的cd，返回最大的那个牌的序号，
    """
    pass

def decide_point(cards_list:list, host_index:int, great_index:int):
    """
    根据专家编号，和大牌编号得出得分与否返回一个pair.(cards, point),即得分牌和总分
    """
    pass