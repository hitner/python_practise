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
        self.stage = 0  # 0 未开始 1 叫地主阶段 2出牌阶段
        self.playerHand = {0: bytearray(), 1: bytearray(), 2: bytearray()}
        self.bottomCards = bytearray()
        self.master = -1
        self.playingTrack = []
        self._deadwood = bytearray()

    def _get_current_turn(self):
        assert self.stage == 2
        if self.playingTrack:
            pre = (self.playingTrack[-1]['player'] + 1 ) % 3
            return pre
        else:
            return self.master

    def __pre_cd(self):
        if self.playingTrack:
            lastValid = self.playingTrack[-1]
            if len(self.playingTrack) > 1 and not lastValid['pattern'] :
                lastValid = self.playingTrack[-2]
            if lastValid['pattern']:
                return doudizhu.CardDescription(lastValid['pattern'], lastValid['weight'])
            else:
                return None
        else:
            return None

    def __add_playing_track(self,  player:int ,cards, cd: doudizhu.CardDescription):
        self.playingTrack.append({
            'player':player,
            'cards': cards.hex(),
            'pattern': cd.pattern,
            'weight': cd.weight})

    def shuffle(self, force=False) -> bool:
        """洗牌，返回True 表示洗牌成功， False表示游戏正在进行中"""
        if not force:
            if self.stage == 1 or self.stage == 2:
                return False
        if not self._deadwood:
            self._deadwood = bytearray(poker.MIN3_ALL)
        else:
            self._deadwood += self.playerHand[0]
            self._deadwood += self.playerHand[1]
            self._deadwood += self.playerHand[2]
        poker.fisher_yates_shuffle(self._deadwood)
        self.bottomCards = self._deadwood[0:3]
        self.playerHand[0] = bytearray(sorted(self._deadwood[3:54:3],
                                              key = poker.min3_doudizhu_cmp, reverse = True))
        self.playerHand[1] = bytearray(sorted(self._deadwood[4:54:3],
                                              key = poker.min3_doudizhu_cmp, reverse = True))
        self.playerHand[2] = bytearray(sorted(self._deadwood[5:54:3],
                                              key = poker.min3_doudizhu_cmp, reverse = True))
        self._deadwood = []
        self.master = -1
        self.stage = 1
        self.playingTrack = []
        return True

    def master_for(self, p_index) -> bool:
        if self.master == -1 and self.stage == 1:
            if 0 <= p_index <= 2:
                self.master = p_index
                self.stage = 2
                all = self.playerHand[p_index] + self.bottomCards
                self.playerHand[p_index] = bytearray(sorted(all, key=poker.min3_doudizhu_cmp,
                                                            reverse=True))
                result = {
                    'master': p_index,
                    'bottomCards': self.bottomCards.hex(),
                }
                return result

    def play_card(self, p_index, cards):
        """
        cards 为空表示"不要"
        返回 None 表示无效出牌
        返回 {...} 表示此次出牌的eventContent
        """
        if p_index == self._get_current_turn():
            if cards:
                if poker.check_has_deal(self.playerHand[p_index], cards):
                    ret = doudizhu.check_value_deal(poker.remove_min3_color(cards), self.__pre_cd())
                    if ret:
                        poker.remove_deal(self.playerHand[p_index], cards)
                        self._deadwood += cards
                        self.__add_playing_track(p_index, cards, ret)
                        return self.playingTrack[-1].copy()
            else:
                if self.__pre_cd():  # 起始出牌时不出是不允许的！即只有在之前有效时才能"不出"
                    self.__add_playing_track(p_index, cards, doudizhu.CardDescription())
                    return self.playingTrack[-1].copy()

    def get_player_status(self, index):
        ret = {}
        ret['stage'] = self.stage
        if self.stage:
            remains = []
            for ip in self.playerHand:
                remains.append(len(self.playerHand[ip]))
            ret['cardsRemain'] = remains
            ret['myCards'] = self.playerHand[index].hex()
            ret['myIndex'] = index
            if self.stage >= 2:
                ret['master'] = self.master
                ret['bottomCards'] = self.bottomCards.hex()
                ret['playingTrack'] = self.playingTrack[-2:]
            elif self.stage == 3:
                ret['unplayedCards'] = [self.playerHand[0].hex(),
                                        self.playerHand[1].hex(),
                                        self.playerHand[2].hex()]
        return ret

    def end_info(self):
        if self.stage == 2:
            if self.playerHand[0] and self.playerHand[1] and self.playerHand[2] :
                return None
            else:
                self.stage = 3
                return {'unplayedCards':[self.playerHand[0].hex(),
                                         self.playerHand[1].hex(),
                                         self.playerHand[2].hex()]}


    def player_leave(self, index):
        if self.stage == 1 or self.stage == 2:
            self.stage = 0
            return {'unplayedCards' : [self.playerHand[0].hex(),
                                     self.playerHand[1].hex(),
                                     self.playerHand[2].hex()],
                    'leavePlayer' : index}