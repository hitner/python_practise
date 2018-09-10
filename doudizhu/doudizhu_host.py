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
        self._cards_pool = list(poker.MIN3_ALL)

        self.player_cards = {0: [], 1: [], 2: []}
        self.back_3 = []
        self.master = -1
        self.cursor = 0 #未开始 1：叫分阶段 > 2：出牌阶段
        self.current_p_index = -1
        self.pre_deals = []

        self.callback = None

        self.pre_cd = None
        self.cannot_afford = 0  # yao bu qi

    def _next_player(self):
        if self.current_p_index == 2:
            self.current_p_index = 0
        else:
            self.current_p_index = self.current_p_index + 1

    def register_callback(self, callback):
        assert callback
        self.callback = callback

    def shuffle(self) -> dict:
        """洗牌，返回一个新的dict"""
        poker.fisher_yates_shuffle(self._cards_pool)
        self.back_3 = self._cards_pool[0:3]
        self.player_cards[0] = sorted(self._cards_pool[3:54:3])
        self.player_cards[1] = sorted(self._cards_pool[4:54:3])
        self.player_cards[2] = sorted(self._cards_pool[5:54:3])
        self._cards_pool = []
        self.master = -1
        self.cursor = 1
        self.current_p_index = -1
        self.pre_deals = []

    def master_for(self, p_index):
        assert self.master == -1 and self.cursor == 1
        if 0 <= p_index <= 2:
            self.current_p_index = p_index
            self.player_cards[p_index] += self.back_3
            return self.back_3


    def dealCard(self, p_index, cards):
        result = {}
        ret = self._dealCard2(p_index, cards)
        if ret:
            self.cursor = self.cursor + 1

            result['cursor'] = self.cursor
            result['actor'] = p_index
            result['cards'] = cards
            result['next_pattern'] = ret[0].pattern
            result['next_weight'] = ret[0].weight

        return result



    def _dealCard2(self, p_index, cards):
        """
        返回 None 表示无效出牌
        返回 cd ,i 表示下一个人i 按cd牌型出牌
        返回 None, i 表示下一个人i可以任意出牌了（前面一个人不要）
        返回 cd, i, 1 表示 i 赢了
        """
        if p_index == self.current_p_index:
            if cards:
                if poker.check_has_deal(self.player_cards[p_index], cards):
                    ret = doudizhu.check_value_deal(poker.remove_min3_color(cards), self.pre_cd)
                    if ret:
                        poker.remove_deal(self.player_cards[p_index], cards)
                        if len(self.player_cards[p_index]) == 0:
                            return ret, self.current_p_index, 1  # 结束
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
                    return doudizhu.CardDescription(), self.current_p_index
                else:
                    return self.pre_cd, self.current_p_index

    def get_player_status(self, index):
        ret = {}
        ret['cursor'] = self.cursor
        if self.cursor == 1:
            ret['cards'] = self.player_cards[index]
        elif self.cursor > 1:
            ret['cards'] = self.player_cards[index]
            ret['current_index'] = self.current_p_index
            ret['master'] = self.master
            remains = []
            for ip in self.player_cards:
                remains.append(len(ip))
            ret['remains'] = remains
            ret['back3'] = self.back_3
            ret['pre_deals'] = self.pre_deals

        return ret

