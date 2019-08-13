from tornado.web import RequestHandler, MissingArgumentError
import http_base_handler
import doudizhu_server



class DdzRoomPlayersHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST','GET', 'DELETE']
    def post(self, *args, **kwargs):
        uid = self.current_user
        if not uid:
            self.write_user_layer_error(2, 'not logined')
            return
        roomId = args[0]

        join_ret = doudizhu_server.join_room(roomId, uid)
        if join_ret:
            self.write_success_dict(join_ret)
        else:
            self.write_user_layer_error(3,'join room error')

    def get(self, *args, **kwargs):
        roomId = args[0]

        players = doudizhu_server.get_room_players(roomId)
        if players:
            self.write_success_dict(players)
        else:
            self.write_user_layer_error(4,'get room players error')

    def delete(self, *args, **kwargs):
        uid = self.current_user
        if not uid:
            self.write_user_layer_error(2, 'not logined')
            return
        roomId = args[0]
        leave_ret = doudizhu_server.leave_room(roomId, uid)
        if leave_ret:
            self.write_success_dict(leave_ret)
        else:
            self.write_user_layer_error(5,'leave room  error')





class DdzRoomReadyHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST','GET', 'DELETE']

    def post(self, *args, **kwargs):
        uid = self.current_user
        if not uid:
            self.write_user_layer_error(2, 'not logined')
            return
        roomId = args[0]



class DdzRoomActHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        uid = self.current_user
        if not uid:
            self.write_user_layer_error(2, 'not logined')
            return
        roomId = args[0]
        action = self.get_query_argument('action','')
        if not action:
            self.write_para_error(['action'])
        else:
            act_ret = doudizhu_server.act_in_room(roomId, uid, action)
            if act_ret:
                self.write_success_dict(act_ret)
            else:
                self.write_user_layer_error(100,'failed to act in room ')



class DdzRoomAfkHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']
    def post(self, *args, **kwargs):
        print(args, kwargs)
        self.write_success({'mgs':'ok'})


