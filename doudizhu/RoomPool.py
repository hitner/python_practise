import tornado.locks
from doudizhu_host import Doudizhu
from dlog import ddzLog

class MessageBuffer:
    def __init__(self):
        self.cond = tornado.locks.Condition()
        self.cache = []
        self.cache_size = 10

    def get_message_since(self, cursor):
        for i in range(0, len(self.cache)):
            if self.cache[i]['cursor'] > cursor:
                return self.cache[i: len(self.cache)]

    def add_message(self, msg: dict):
        self.cache.append(msg)

        if len(self.cache) > self.cache_size:
            self.cache = self.cache[int(self.cache_size / 2):]

        print('notify all')
        self.cond.notify_all()


"""
一个Room对应一个Game，暂无旁观席位
"""




class Room:
    EVENT_BID = 100
    EVENT_STARTED = 110
    EVENT_PLAY = 111
    EVENT_END = 112
    EVENT_LEAVE = 113 #玩家在游戏中逃跑

    def __init__(self, rid=0):
        self.room_id = rid
        self.create_time = 0
        self.creator_uid = 0
        self.players = []
        self.cursor = 0
        self.msgBuffer = MessageBuffer()
        self.gameHost: Doudizhu = Doudizhu()

    def __add_dict_message(self, eventType, msg):
        self.cursor = self.cursor + 1
        event = {'cursor':self.cursor,
                 'eventType': eventType,
                 'eventContent':msg}
        self.msgBuffer.add_message(event)

    def isFull(self):
        return len(self.players) == 3

    def addPlayer(self, uid):
        if uid not in self.players and not self.isFull():
            self.players.append(uid)
        return uid in self.players

    def isContainPlayer(self, uid):
        return uid in self.players

    def tryStart(self):
        if len(self.players) == 3:
            success = self.gameHost.shuffle()
            if success:
                self.__add_dict_message(self.EVENT_BID,{})

    def get_internal_index(self, uid):
        return self.players.index(uid)

    def ask_for_master(self, uid) -> bool:
        result = self.gameHost.master_for(self.get_internal_index(uid))
        if result:
            ddzLog.info('ask for master success')
            self.__add_dict_message(self.EVENT_STARTED, result)
        return bool(result)

    def deal_cards(self, uid, cs) -> bool:
        cards = bytes.fromhex(cs)
        result = self.gameHost.play_card(self.get_internal_index(uid), cards)
        # 输出这次action { cursor:  cards:  pattern: weight: index:  next_pattern:0}
        if result:
            self.__add_dict_message(self.EVENT_PLAY, result)
            endInfo = self.gameHost.end_info()
            if endInfo:
                self.__add_dict_message(self.EVENT_END, endInfo)

        return bool(result)

    def getRoomMessages(self, cursor):
        return self.msgBuffer.get_message_since(cursor)

    def wait(self):
        return self.msgBuffer.cond.wait()

    def getMyCards(self, uid):
        describe = self.gameHost.get_player_status(self.get_internal_index(uid))
        describe['cursor'] = self.cursor
        return describe

    def leave_room(self, uid):
        index = self.get_internal_index(uid)
        leave_msg = self.gameHost.player_leave(index)
        del self.players[index:index+1]
        if leave_msg:
            self.__add_dict_message(self.EVENT_LEAVE, leave_msg)


    def restart_game(self):
        if self.isFull():
            success = self.gameHost.shuffle()
            if success:
                self.__add_dict_message(self.EVENT_BID,{})
            return True


class RoomPool:
    """
    提供一般化的存储方案，如支持内存、sql、redis
    """

    def __init__(self):
        self.pool = {}
        self.idInc = 1  # 下一个有效的roomId

    def _nextId(self):
        a = self.idInc;
        self.idInc = a + 1
        return a

    def _createRoom(self) -> Room:
        room = Room(rid=self._nextId())
        self.pool[room.room_id] = room
        return room

    def _get_user_room(self, uid) -> int:
        """先不考虑性能优化,roomId为0是为空的意思"""
        for k, v in self.pool.items():
            if v.isContainPlayer(uid):
                return k
        return 0

    def createRoom(self, uid=0):
        """uid不为0时，默认创建成果，该uid就加入该room"""
        pass

    def joinRoom(self, uid, roomId):
        if roomId in self.pool:
            return self.pool[roomId].addPlayer(uid)
        else:
            return False


    def isRoomExist(self, roomId) -> bool:
        return roomId in self.pool

    def RandomJoinRoom(self, uid) -> int:
        """随机进房"""
        alreadyRoom = self._get_user_room(uid)
        if alreadyRoom:
            return alreadyRoom

        targetRoom = None
        for k, v in self.pool.items():
            if not v.isFull():
                targetRoom = v
                break

        if not targetRoom:
            targetRoom = self._createRoom()

        targetRoom.players.append(uid)
        targetRoom.tryStart()
        print(uid, ' join room:', targetRoom.room_id)
        return targetRoom.room_id

    def get_room(self, roomId) -> Room:
        """先不考虑性能优化,roomId为0是为空的意思"""
        if roomId in self.pool:
            return self.pool[roomId]


    def isUserInRoom(self, uid, roomid):
        if roomid in self.pool:
            return self.pool[roomid].isContainPlayer(uid)


room_pool = RoomPool()
