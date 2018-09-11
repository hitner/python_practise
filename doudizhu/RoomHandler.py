from tornado.web import RequestHandler, MissingArgumentError
from RoomPool import room_pool
import asyncio


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        #pass

    def write_success(self, data):
        self.write({'rcode': 0, 'data': data})

    def write_my_error(self, rcode, describe):
        self.write({'rcode': rcode, 'describe': describe})

    def write_para_error(self):
        self.write_my_error(100, "para error")

    def write_notinroom_error(self):
        self.write_my_error(110, "not in room")

    def write_nocards_error(self):
        self.write_my_error(120, "no cards")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()


class RandomJoinRoomHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            rid = room_pool.RandomJoinRoom(uid)
            self.write_success({'roomId': rid})
        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.write_error(500)

    def post(self, *args, **kwargs):
        self.get()


class GetMyCardsHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            if room_pool.isUserInRoom(uid, roomId):
                dret = room_pool.get_room(roomId).getMyCards(uid)
                if dret:
                    self.write_success(dret)
                else:
                    self.write_nocards_error()
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.write_error(500)

    def post(self, *args, **kwargs):
        self.get()


class DealCardHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            cards = self.get_argument('cards', default='')
            if room_pool.isUserInRoom(uid, roomId):
                room = room_pool.get_room(roomId)
                dret = room.deal_cards(uid, cards)
                final = {'rcode': 121, 'describe': 'not value deals'}
                if dret:
                    final = {'rcode': 0}
                self.write_success(final)
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.write_error(500)

    def post(self, *args, **kwargs):
        self.get()


class PollChangesHandler(BaseHandler):

    async def post(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            cursor = int(self.get_argument('cursor'))

            if room_pool.isUserInRoom(uid, roomId):
                room = room_pool.get_room(roomId)
                msgs = room.getRoomMessages(cursor)
                while not msgs:
                    self.wait_future = room.wait()
                    try:
                        await self.wait_future
                    except asyncio.CancelledError:
                        return
                    msgs = room.getRoomMessages(cursor)
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
