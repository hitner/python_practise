import tornado.locks
from doudizhu_host import Doudizhu


class MessageBuffer:
    def __init__(self):
        self.cond = tornado.locks.Condition()
        self.cache = []
        self.cache_size = 10

    def get_message_since(self, cursor):
        for i in range(0, len(self.cache)):
            if self.cache[i]['cursor'] > cursor:
                return self.cache[i : len(self.cache)]

    def add_message(self,msg: dict):
        self.cache.append(msg)

        if len(self.cache) > self.cache_size:
            self.cache = self.cache[int(self.cache_size/2):]

        print('notify all')
        self.cond.notify_all()



"""
一个Room对应一个Game，暂无旁观席位
"""

class Room:
    GameStart = 1

    def __init__(self, rid = 0):
        self.room_id = rid
        self.create_time = 0
        self.creator_uid = 0
        self.players = []
        self.msgBuffer = MessageBuffer()
        self.gameHost : Doudizhu = Doudizhu()

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
            self.gameHost.shuffle()
            self.msgBuffer.add_message({'cursor': self.GameStart})

    def get_internal_index(self, uid):
        return self.players.index(uid)

    def deal_cards(self, uid, cards) -> bool:

        result = self.gameHost.dealCard(self.get_internal_index(uid), cards)
        #输出这次action { cursor:  cards:  pattern: weight: index:  next_pattern:0}
        if result:
            self.msgBuffer.add_message(result)

        return bool(result)


    def getRoomMessages(self, cursor):
        return self.msgBuffer.get_message_since(cursor)

    def wait(self):
        return self.msgBuffer.buffer.cond.wait()


    def getMyCards(self, uid):
        return self.gameHost.get_player_status(self.get_internal_index(uid))



class RoomPool:
    """
    提供一般化的存储方案，如支持内存、sql、redis
    """
    def __init__(self):
        self.pool = {}
        self.idInc = 1  #下一个有效的roomId

    def _nextId(self):
        a = self.idInc;
        self.idInc = a + 1
        return a

    def _createRoom(self) -> Room:
        room = Room(rid = self._nextId())
        self.pool[room.room_id] = room
        return room



    def createRoom(self, uid = 0):
        """uid不为0时，默认创建成果，该uid就加入该room"""
        pass

    def joinRoom(self, uid, roomId):
        if roomId in self.pool:
            return self.pool[roomId].addPlayer(uid)
        else:
            return False

    def leaveRoom(self, uid, roomId):
        pass

    def isRoomExist(self,roomId) -> bool:
        return roomId in self.pool

    def RandomJoinRoom(self, uid) -> int:
        """随机进房"""
        alreadyRoom = self.getUserRoom(uid)
        if alreadyRoom:
            return alreadyRoom

        targetRoom = None
        for k,v in self.pool.items():
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
        return self.pool[roomId]


    def isUserInRoom(self, uid, roomid):
        if roomid in self.pool:
            return self.pool[roomid].isContainPlayer(uid)



room_pool = RoomPool()