import http_base_handler
import waiting_room_server


class RoomPlayersHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET','POST','DELETE']

    def get(self, *args, **kwargs):
        pass


    def post(self, *args, **kwargs):
        uid = self.current_user
        if not uid:
            self.write_need_login()
            return

        room_id = args[0]
        join_ret = waiting_room_server.wi_join_room(room_id, uid)
        if isinstance(join_ret, dict):
            self.write_success_dict(join_ret)
        else:
            self.write_user_layer_error(3, join_ret)

    def delete(self,*args,**kwargs):
        uid = self.current_user
        if not uid:
            self.write_need_login()
            return

        room_id = args[0]
        if len(args) > 1:
            target_uid = args[1]
        leave_ret = waiting_room_server.wi_leave_room(room_id, uid, target_uid)
        if isinstance leave_ret:
            self.write_success_dict(leave_ret)
        else:
            self.write_user_layer_error(4, "cannot leave this room")


class CreateRoomHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        uid = self.current_user
        if not uid:
            self.write_need_login()
            return

        join_ret = waiting_room_server.create_room(uid)
        if join_ret:
            self.write_success_dict(join_ret)
        else:
            self.write_user_layer_error(1, "cannot create my room")

    def delete(self,*args,**kwargs):
        uid = self.current_user
        if not uid:
            self.write_need_login()
            return

        delte_ret = waiting_room_server.delete_room(uid)
        if delte_ret:
            self.write_success_dict(delte_ret)
        else:
            self.write_user_layer_error(2, "cannot delete my room")

