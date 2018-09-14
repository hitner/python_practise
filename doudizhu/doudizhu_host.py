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
        self._cards_pool = bytearray()

        self.player_cards = {0: bytearray(), 1: bytearray(), 2: bytearray()}
        self.back_3 = bytearray()
        self.master = -1
        self.cursor = 0 #未开始 1：叫分阶段 > 2：出牌阶段
        self.current_p_index = -1
        self.pre_deals = []

        self.callback = None

    def _next_player(self):
        if self.current_p_index == 2:
            self.current_p_index = 0
        else:
            self.current_p_index = self.current_p_index + 1

    def __pre_cd(self):
        if self.pre_deals:
            lastValid = self.pre_deals[0]
            if len(self.pre_deals) > 1:
                if self.pre_deals[1]['pattern']:
                    lastValid = self.pre_deals[1]

            if lastValid['pattern']:
                return doudizhu.CardDescription(lastValid['pattern'], lastValid['weight'])
            else:
                return None
        else:
            return None

    def __add_pre(self, cards, cd: doudizhu.CardDescription):
        if len(self.pre_deals) == 2:
            del self.pre_deals[0:1]
        self.pre_deals.append({'cards':cards.hex(), 'pattern':cd.pattern, 'weight':cd.weight})

    def register_callback(self, callback):
        assert callback
        self.callback = callback

    def shuffle(self):
        """洗牌，返回一个新的dict"""
        if not self._cards_pool:
            self._cards_pool = bytearray(poker.MIN3_ALL)
        else:
            self._cards_pool += self.player_cards[0]
            self._cards_pool += self.player_cards[1]
            self._cards_pool += self.player_cards[2]
        poker.fisher_yates_shuffle(self._cards_pool)
        self.back_3 = self._cards_pool[0:3]
        self.player_cards[0] = bytearray(sorted(self._cards_pool[3:54:3]))
        self.player_cards[1] = bytearray(sorted(self._cards_pool[4:54:3]))
        self.player_cards[2] = bytearray(sorted(self._cards_pool[5:54:3]))
        self._cards_pool = []
        self.master = -1
        self.cursor = 1
        self.current_p_index = -1
        self.pre_deals = []

    def master_for(self, p_index) -> bool:
        if self.master == -1 and self.cursor == 1:
            if 0 <= p_index <= 2:
                self.master = p_index
                self.cursor = 2
                self.current_p_index = p_index
                self.player_cards[p_index] += self.back_3

                result = {
                    'cursor':self.cursor,
                    'master':p_index,
                    'back3':self.back_3.hex(),
                    'current_index':p_index,
                }
                return result


    def dealCard(self, p_index, cards: bytearray):
        """

        :param p_index:
        :param cards: min3 的byte 或者bytesarray
        :return:
        """
        result = {}
        ret = self._dealCard2(p_index, cards)
        if ret:
            self.cursor = self.cursor + 1

            result['cursor'] = self.cursor
            result['actor'] = p_index
            result['cards'] = cards.hex()
            result['next_pattern'] = ret.pattern
            result['next_weight'] = ret.weight

        return result



    def _dealCard2(self, p_index, cards):
        """
        返回 None 表示无效出牌
        返回 cd 表示下一个人i 按cd牌型出牌 (0,0)表示可以任意出牌
        """
        if p_index == self.current_p_index:
            if cards:
                if poker.check_has_deal(self.player_cards[p_index], cards):
                    ret = doudizhu.check_value_deal(poker.remove_min3_color(cards), self.__pre_cd())
                    if ret:
                        poker.remove_deal(self.player_cards[p_index], cards)
                        self._cards_pool += cards
                        self._next_player()
                        self.__add_pre(cards, ret)
                        return ret
            else:
                if not self.__pre_cd(): #起始出牌时不出是不允许的！
                    return None
                self._next_player()
                self.__add_pre(cards, doudizhu.CardDescription())

                new_pre = self.__pre_cd()
                if new_pre:
                    return new_pre
                else:
                    return doudizhu.CardDescription()

    def get_player_status(self, index):
        assert self.cursor

        ret = {}

        ret['cursor'] = self.cursor
        remains = []
        for ip in self.player_cards:
            remains.append(len(self.player_cards[ip]))
        ret['remains'] = remains
        ret['cards'] = self.player_cards[index].hex()
        ret['my_index'] = index
        if self.cursor > 1:
            ret['current_index'] = self.current_p_index
            ret['master'] = self.master

            ret['back3'] = self.back_3.hex()
            ret['pre_deals'] = self.pre_deals

        return ret

