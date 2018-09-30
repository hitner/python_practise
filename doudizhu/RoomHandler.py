from tornado.web import RequestHandler, MissingArgumentError
from RoomPool import room_pool
import asyncio
from dlog import ddzLog

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
        self.write_my_error(120, "no cards becouse of match not started")

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


class AskForMasterHandler(BaseHandler):
    def post(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            if room_pool.isUserInRoom(uid, roomId):
                room = room_pool.get_room(roomId)
                dret = room.ask_for_master(uid)
                if dret:
                    self.write_success({})
                else:
                    self.write_my_error(122, 'already has a master')
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except BaseException as e:
            ddzLog.error(e)
            self.write_error(500)


class DealCardHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            cards = self.get_argument('cards', default='')
            if room_pool.isUserInRoom(uid, roomId):
                room = room_pool.get_room(roomId)
                dret = room.deal_cards(uid, cards)
                if dret:
                    ddzLog.info('valued deal from uid:%s, cards:%s', uid, cards)
                    self.write_success({})
                else:
                    self.write_my_error(121, 'not value deals')
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


class LeaveRoomHandler(BaseHandler):
    def post(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            if room_pool.isUserInRoom(uid, roomId):
                room = room_pool.get_room(roomId)
                room.leave_room(uid)
                ddzLog.info('player uid:%s, leave room:%s', uid, roomId)
                self.write_success({})
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.write_error(500)


class RestartGameHandler(BaseHandler):
    def post(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            if room_pool.isUserInRoom(uid, roomId):
                room = room_pool.get_room(roomId)
                ret = room.restart_game()
                ddzLog.info('player uid:%s in room:%s restart game,result:%s', uid, roomId, ret)
                if ret:
                    self.write_success({})
                else:
                    self.write_my_error(122, 'player not enough')
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.write_error(500)