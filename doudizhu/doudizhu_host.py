import doudizhu
import poker

'''Match可使用的方法为
shuffle 洗牌
dealCard 返回三手牌
leadCard (id ,cards) 出牌 true有效、false 无效
escape (id ) 不出
输出事件 id，（lastLead)


getLastLead 返回id cardStruct
getTurns 返回id，指示该谁出牌了
'''


class Doudizhu:

    def __init__(self):
        self.player_cards = {0: [], 1: [], 2: []}
        self.back_3 = []
        self.cards_pool = list(poker.MIN3_ALL)
        self.current_p_index = 0
        self.pre_cd = None
        self.cannot_afford = 0 # yao bu qi

    def _next_player(self):
        if self.current_p_index == 2:
            self.current_p_index = 0
        else:
            self.current_p_index = self.current_p_index + 1

    def shuffle(self):
        poker.fisher_yates_shuffle(self.cards_pool)
        self.back_3 = self.cards_pool[0:3]
        self.player_cards[0] = sorted(self.cards_pool[3:54:3])
        self.player_cards[1] = sorted(self.cards_pool[4:54:3])
        self.player_cards[2] = sorted(self.cards_pool[5:54:3])
        return dict(self.player_cards)

    def master_for(self, p_index):
        if len(self.back_3) == 3 and 0 <= p_index <= 2:
            self.current_p_index = p_index
            self.player_cards[p_index] += self.back_3
            ret = self.back_3
            self.back_3 = []
            return ret

    def dealCard(self, p_index, cards):
        """cards 必须已经排过序了"""
        if (p_index == self.current_p_index):
            if cards:
                if poker.check_has_deal(self.player_cards[p_index], cards):
                    ret = doudizhu.check_value_deal(poker.remove_min3_color(cards), self.pre_cd)
                    if ret:
                        poker.remove_deal(self.player_cards[p_index], cards)
                        if len(self.player_cards[p_index]) == 0:
                            return ret, self.current_p_index, 1 # 结束
                        self._next_player()
                        self.pre_cd = ret
                        self.cannot_afford = 0
                        return ret, self.current_p_index
            else:
                if not self.pre_cd:
                    return None
                self._next_player()
                self.cannot_afford += 1
                if self.cannot_afford == 2:
                    self.cannot_afford = 0
                    self.pre_cd = None
                    return None, self.current_p_index
                else:
                    return self.pre_cd, self.current_p_index