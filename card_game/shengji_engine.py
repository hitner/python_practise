"""升级引擎
    不负责洗牌、uid与index的对应、关卡的确定，同时也不负责http JSON的生成
    没有定时器
    只负责逻辑上一局的玩法过程；
- 依赖
    shengji_core_foundation
- 原理

- 备注
    把洗牌功能挪到外面去。自己不需要提供这样的功能。

"""
import enum
import card
import shengji_core_foundation

class ShengjiEngine:
    WAITING = 0
    MAKING_TRUMP = 1
    SELECTING_BOTTOM = 2 #铺底的过程
    PLAYING_CARD = 3 #出牌的过程
    SHOW_RESULT = 4 #显示最后结果

    class MakeTrump:
        TRUMP_SINGLE = 0
        TRUMP_DOUBLE = 1
        TRUMP_BLACK_JOKER = 2
        TRUMP_RED_JOKER = 3
        def __init__(self):
            self.index = -1 #叫庄的玩家序号
            self.trump_type = TRUMP_SINGLE # 分别有单牌/双牌/一对小王/一对大王
        
        def __init__(self, index, type_t):
            self.index = index
            self.trump_type = type_t

    def __init__(self):
        self.host_index = -1
        self.hand_cards = None
        self.bottom_cards = None
        self.first_index = -1 #这一轮谁最先出
        self.next_index = -1 #接下来该谁出牌了
        self.history_track = [] #历史出牌记录
        self.state = WAITING
        self.current_rank = 2 #升级关卡
        self.make_trump_track = [] #记录叫主过程
        self.trump_card = None #叫主的牌

    def reset(self):
        self.host_index = -1

    def begin_with(self, hand_cards:list, bottom_cards:list, host_index:int, ):
        """从发的手牌开始，注意这里的手牌还没有排序，必须在完成铺底之后才能排序
        :param int host_index: 固定的庄家，如果还未确定，这个值为-1
        """
        self.hand_cards = hand_cards
        self.bottom_cards = bottom_cards
        self.host_index = host_index
        self.state = MAKING_TRUMP

    def make_trump(self, play_index, cards:list):
        """抢主牌"""
        if self.state == MAKING_TRUMP:
            if len(self.make_trump_track):
                last_make_trump = self.make_trump_track[-1]
                new_make_trump = self._check_make_trump(play_index,cards)
                if new_make_trump and new_make_trump.trump_type > last_make_trump.trump_type:
                    self.make_trump_track.append(new_make_trump)
                    return True
            else:
                new_make_trump = self._check_make_trump(play_index,cards)
                if new_make_trump: 
                    self.make_trump_track.append(new_make_trump)
                    return True 
    
    def desive_host_and_trump(self):
        """决定庄家和关卡牌,同时状态进入铺底牌阶段"""
        self.state = SELECTING_BOTTOM


    
    def _check_make_trump(self, play_index, cards) -> MakeTrump:
        """根据单前关卡值判断叫主是否有效"""
        if len(cards) == 1:
            if card.get_weight(cards[0]) == self.current_rank:
                return MakeTrump(play_index, MakeTrump.TRUMP_SINGLE)
        elif len(cards) == 2:
            if cards[0] == cards[1]:
                weight = card.get_weight(cards[0])
                if weight == self.current_rank:
                    return MakeTrump(play_index, MakeTrump.TRUMP_DOUBLE)
                elif weight == card.BLACK_JOKER:
                    return MakeTrump(play_index, MakeTrump.TRUMP_BLACK_JOKER)
                elif weight == card.RED_JOKER:
                    return MakeTrump(play_index, MakeTrump.TRUMP_RED_JOKER)




