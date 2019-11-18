from tornado.web import RequestHandler
import tornado.websocket
import http_base_handler
import json
import websocket_channel_pool
from tornado.log import gen_log

class PostHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        session = websocket_channel_pool.wi_create_channel()
        if isinstance(session, dict):
            self.write_success_dict(session)
        else:
            self.write_user_layer_error(1,session)




class OneInstanceHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST','DELETE']

    def post(self, *args, **kwargs):
        try:
            message = json.loads(self.request.body)
            websocket_name = args[0]
            if message:
                result_string = websocket_channel_pool.wi_send_message_to_channel(websocket_name, message)
                if isinstance(result_string, dict):
                    self.write_success_dict({})
                else:
                    self.write_user_layer_error(1, result_string)
            else:
               self.write_user_layer_error(1, 'should send something') 
        except json.JSONDecodeError:
            self.write_bad_request('not a json string')


    def delete(self, *args, **kwargs):
        try:
            websocket_name = args[0]
            result_string = websocket_channel_pool.wi_delete_channel(websocket_name)
            if isinstance(result_string, dict):
                self.write_success_dict({})
            else:
                self.write_user_layer_error(1, result_string)
        except json.JSONDecodeError:
            self.write_bad_request('unknown error') 


class JoinHandler(tornado.websocket.WebSocketHandler):
    async def get(self, *args, **kwargs):
        channel_name = args[0]
        if websocket_channel_pool.i_has_channel(channel_name): 
            await super(JoinHandler,self).get(*args, **kwargs)
        else:
            gen_log.warning('try to connect unexisted channel')
            self.set_status(400)
            self.finish("no such websocket channel")

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        channel_name = args[0]
        if websocket_channel_pool.i_has_channel(channel_name):
            websocket_channel_pool.i_add_client(channel_name, self)
        else:
            self.close(reason='no this channel')
            gen_log.warning('open an unexisted channel')

    def on_close(self):
        channel_name = self.open_args[0]
        if websocket_channel_pool.i_has_channel(channel_name):
            websocket_channel_pool.i_remove_client(channel_name, self)


    def on_message(self, message):
        #logging.info("got message %r", message)
        print(f'warning{message}')
