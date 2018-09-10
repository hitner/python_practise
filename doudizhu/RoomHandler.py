from tornado.web import RequestHandler, MissingArgumentError
from RoomPool import room_pool
import asyncio

class BaseHandler(RequestHandler):
    def write_success(self, data):
        self.write({'rcode':0, 'data':data})

    def write_my_error(self, rcode, describe):
        self.write({'rcode':rcode, 'describe':describe})

    def write_para_error(self):
        self.write_my_error(100, "para error")

    def write_notinroom_error(self):
        self.write_my_error(110, "not in room")

    def write_nocards_error(self):
        self.write_my_error(120, "no cards")

class RandomJoinRoomHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            rid = room_pool.RandomJoinRoom(uid)
            self.write_success({'roomId':rid})
        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.write_error(500)




class GetMyCardsHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            if room_pool.isUserInRoom(uid, roomId):
                dret = room_pool.getMyCards(uid, roomId)
                if dret:
                    self.write_success(dret)
                else:
                    self.write_nocards_error()
            else:
                self.write_notinroom_error

        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.write_error(500)



class DealCardHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass



class PollChangesHandler(BaseHandler):

    async def get(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            cursor = int(self.get_argument('cursor'))

            if room_pool.isUserInRoom(uid, roomId):
                msgs = room_pool.getRoomMessages(roomId, cursor)
                while not msgs:
                    self.wait_future = room_pool.waitOnRoom(roomId)
                    try:
                        await self.wait_future
                    except asyncio.CancelledError:
                        return
                    msgs = room_pool.getRoomMessages(roomId, cursor)
                if self.request.connection.stream.closed():
                    return

                self.write_success(msgs)

            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except Exception as e:
            self.write_error(500)

    def on_connection_close(self):
        if self.wait_future:
            self.wait_future.cancel()