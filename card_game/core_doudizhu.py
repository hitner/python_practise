from enum import IntEnum
import card

class CoreDoudizhu:
    """
    提供最最简单的牌核心处理逻辑，每个player的编号是0，1，2
    主要过程是：
    1，准备阶段 init/reset
    2，洗牌、分牌给每个玩家 shuffle
    3，确定地主 set_landlord
    4，出牌 play_card
    5, 获得player视角的游戏状态 get_player_status
    """
    STAGE_INIT = 0
    STAGE_WAITING_LANDLORD = 1
    STAGE_PLAYING = 2

    LANDLORD_NONE = -1

    def __init__(self):
        self.stage = 0  # 0 未开始 1 叫地主阶段 2出牌阶段
        self.playerHand = {0: bytearray(), 1: bytearray(), 2: bytearray()}
        self.bottomCards = bytearray()
        self.landlord = self.LANDLORD_NONE
        self.playingTrack = []
        self._deadwood = bytearray()

    def reset(self):
        self.stage = 0  # 0 未开始 1 叫地主阶段 2出牌阶段
        self.playerHand = {0: bytearray(), 1: bytearray(), 2: bytearray()}
        self.bottomCards = bytearray()
        self.landlord = self.LANDLORD_NONE
        self.playingTrack = []
        if len (self._deadwood) != len(card.one_deck):
            self._deadwood = []

    def shuffle(self) -> bool:
        """洗牌，返回True 表示洗牌成功， False表示游戏正在进行中,无法洗牌"""
        if not self._deadwood:
            self._deadwood = bytearray(card.one_deck)
        # else:
        #     self._deadwood += self.playerHand[0]
        #     self._deadwood += self.playerHand[1]
        #     self._deadwood += self.playerHand[2]
        card.fisher_yates_shuffle(self._deadwood)
        self.bottomCards = bytearray(self._deadwood[0:3])

        self.playerHand[0] = card.sort_by_doudizhu_rule(self._deadwood[3:54:3])
        self.playerHand[1] = card.sort_by_doudizhu_rule(self._deadwood[4:54:3])
        self.playerHand[2] = card.sort_by_doudizhu_rule(self._deadwood[5:54:3])

        self._deadwood = []
        self.landlord = -1
        self.stage = self.STAGE_WAITING_LANDLORD
        self.playingTrack = []
        return True

    def set_landlord(self, p_index) -> bool:
        if self.landlord == self.LANDLORD_NONE and self.stage == self.STAGE_WAITING_LANDLORD:
            if 0 <= p_index <= 2:
                self.landlord = p_index
                self.stage = self.STAGE_PLAYING
                all = self.playerHand[p_index] + self.bottomCards
                self.playerHand[p_index] = bytearray(sorted(all, key=poker.min3_doudizhu_cmp,
                                                            reverse=True))
                result = {
                    'master': p_index,
                    'bottomCards': self.bottomCards.hex(),
                }
                return result
    def _get_current_turn(self):
        assert self.stage == 2
        if self.playingTrack:
            pre = (self.playingTrack[-1]['player'] + 1 ) % 3
            return pre
        else:
            return self.landlord

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
                ret['master'] = self.landlord
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