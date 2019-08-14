
import core_doudizhu

class Doudizhu:
    def __init__(self):
        self.players = []
        self.longpoll_channel = ''
        self.afk_list = []
        self.ready_list = []
        self.seq = 0

    def join_player(self, uid):
        if uid not in self.players:
            if len(self.players) >= 3:
                return None
            self.players.append(uid)
            self.afk_list.append(0)
            self.ready_list.append(1)
        
        return {'longpoll_channel':self.longpoll_channel,
                'seq':self.seq,
                'players':self.players,
                'ready_list':self.ready_list,
                'afk_list':self.afk_list}

