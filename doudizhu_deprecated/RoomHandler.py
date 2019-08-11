from tornado.web import RequestHandler, MissingArgumentError
import http_base_handler
from RoomPool import room_pool
import asyncio
from dlog import ddzlog



class DdzRoomHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']
    def post(self, *args, **kwargs):
        print(args, kwargs)
        self.write_success({'mgs':'ok'})



class RandomJoinRoomHandler(http_base_handler.BaseHandler):
    def get(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            rid = room_pool.RandomJoinRoom(uid)
            self.write_success({'roomId': rid})
        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.send_error(500)

    def post(self, *args, **kwargs):
        self.get()


class GetMyCardsHandler(http_base_handler.BaseHandler):
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
            self.send_error(500)

    def post(self, *args, **kwargs):
        self.get()


class DdzRoomMasterBidHandler(http_base_handler.BaseHandler):
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
                    self.write_code_layer_error(440, 'already has a master')
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except BaseException as e:
            ddzlog.error(e)
            self.send_error(500)


class DdzRoomPlayedCardsHandler(http_base_handler.BaseHandler):
    def post(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(args[0])
            cards = self.get_argument('cards', default='')
            if room_pool.isUserInRoom(uid, roomId):
                room = room_pool.get_room(roomId)
                dret = room.deal_cards(uid, cards)
                if dret:
                    ddzlog.info('valued deal from uid:%s, cards:%s', uid, cards)
                    self.write_success({})
                else:
                    self.write_code_layer_error(441, 'not value deals')
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.send_error(500)



class DdzRoomMessagesHandler(http_base_handler.BaseHandler):

    async def get(self, *args, **kwargs):
        try:
            roomId = int(args[0])
            room = room_pool.get_room(roomId)
            if room:
                cursor = int(self.get_argument('cursor'))
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
                self.send_error(404)

        except MissingArgumentError:
            self.write_para_error(['cursor'])
        except BaseException as e:
            self.send_error(500)

    def on_connection_close(self):
        if self.wait_future:
            self.wait_future.cancel()


class DdzRoomPlayerHandler(http_base_handler.BaseHandler):
    def post(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            if room_pool.isUserInRoom(uid, roomId):
                room = room_pool.get_room(roomId)
                room.leave_room(uid)
                ddzlog.info('player uid:%s, leave room:%s', uid, roomId)
                self.write_success({})
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.send_error(500)

    def get(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        if len(args) < 2 :
            self.send_error(405)




class DdzRoomReadyHandler(http_base_handler.BaseHandler):
    def post(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(self.get_argument('roomId'))
            if room_pool.isUserInRoom(uid, roomId):
                room = room_pool.get_room(roomId)
                ret = room.restart_game()
                ddzlog.info('player uid:%s in room:%s restart game,result:%s', uid, roomId, ret)
                if ret:
                    self.write_success({})
                else:
                    self.write_code_layer_error(122, 'player not enough')
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.send_error(500)