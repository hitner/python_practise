from tornado.web import RequestHandler, MissingArgumentError
from RoomPool import room_pool
import asyncio
from dlog import ddzLog

class BaseHandler(RequestHandler):
    COOKIE_NAME = 'session'
    def get_current_user(self):
        session :str = self.get_secure_cookie(self.COOKIE_NAME)
        if session:
            sep = session.split('-',1)
            return int(sep[0])

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        #pass

    def write_success(self, data):
        self.write({'rcode': 0, 'data': data})

    def write_user_layer_error(self, rcode, describe):
        self.write({'rocode':rcode, 'describe':describe})
        
    def write_code_layer_error(self, rcode, describe):
        self.set_status(rcode)
        self.finish(describe)

    def write_para_error(self, para):
        self.write_code_layer_error(400, 'Error: need para' + ', '.join(para))

    def write_notinroom_error(self):
        self.write_code_layer_error(430, "Error: not in room")


    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def get(self, *args, **kwargs):
        self.reply405()
        
    def post(self, *args, **kwargs):
        self.reply405()
    
    def put(self, *args, **kwargs):
        self.reply405()
    
    def delete(self, *args, **kwargs):
        self.reply405()
    
    def patch(self, *args, **kwargs):
        self.reply405()
        
    def reply405(self):
        self.set_status(405)
        allow = ', '.join(self.ALLOWED_METHODS)
        self.add_header('Allow',allow)
        self.finish('Error: method not allowed, only for ' + allow)



class DdzAuthLoginHandler(BaseHandler):
    ALLOWED_METHODS = ['POST']
    def post(self, *args, **kwargs):
        uid = self.get_argument('uid', '')
        if uid:
            token = 'THESE IS A FAKE TOKEN'
            self.set_secure_cookie(self.COOKIE_NAME, uid + ':' + token)
            self.write_success({})
        else:
            self.write_para_error(['uid'])


class DdzAuthLogoutHandler(BaseHandler):
    ALLOWED_METHODS = ['POST']
    def post(self, *args, **kwargs):
        if self.current_user:
            self.clear_all_cookies()
            self.write_success({})
        else:
            self.write_code_layer_error(403, 'Error: unvalue login')


class DdzRoomHandler(BaseHandler):
    ALLOWED_METHODS = ['POST']
    def post(self, *args, **kwargs):
        print(args, kwargs)
        self.write_success({'mgs':'ok'})



class RandomJoinRoomHandler(BaseHandler):
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
            self.send_error(500)

    def post(self, *args, **kwargs):
        self.get()


class DdzRoomMasterBidHandler(BaseHandler):
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
            ddzLog.error(e)
            self.send_error(500)


class DdzRoomPlayedCardsHandler(BaseHandler):
    def post(self, *args, **kwargs):
        try:
            uid = int(self.get_argument('uid'))
            roomId = int(args[0])
            cards = self.get_argument('cards', default='')
            if room_pool.isUserInRoom(uid, roomId):
                room = room_pool.get_room(roomId)
                dret = room.deal_cards(uid, cards)
                if dret:
                    ddzLog.info('valued deal from uid:%s, cards:%s', uid, cards)
                    self.write_success({})
                else:
                    self.write_code_layer_error(441, 'not value deals')
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.send_error(500)



class DdzRoomMessagesHandler(BaseHandler):

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


class DdzRoomPlayerHandler(BaseHandler):
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
            self.send_error(500)

    def get(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        if len(args) < 2 :
            self.send_error(405)




class DdzRoomReadyHandler(BaseHandler):
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
                    self.write_code_layer_error(122, 'player not enough')
            else:
                self.write_notinroom_error()

        except MissingArgumentError:
            self.write_para_error()
        except Exception:
            self.send_error(500)