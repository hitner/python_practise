from tornado.web import RequestHandler
import json
import asyncio
import http_base_handler
import session_manager


class MasterCreateHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET']

    def get(self, *args, **kwargs):
        session = session_manager.create_session()
        self.write_success_dict({'session':session.token,
                                 'QRCodeUrl':'http://192.168.10.237:8881/dropim/connect'})



class MasterSendHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        token = self.get_query_argument('session','')
        if token:
            try:
                msg = json.loads(self.request.body)
                if session_manager.master_send_msg(token, msg):
                    self.write_success_dict({})
                else:
                    self.write_user_layer_error(1,'session 失效')
            except json.JSONDecodeError:
                self.write_bad_request('not a json string')
        else:
            self.write_error_parameter(['session'])




class MasterSyncMessageHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET']
    wait_future = None

    async def get(self, *args, **kwargs):
        token = self.get_query_argument('session', '')
        seq = self.get_query_argument('seq', '')
        if token and seq :
            session = session_manager.session_from(token)
            if session:
                msgs = session.master_get_msgs(seq)
                while not msgs:
                    self.wait_future = session.master_wait()
                    try:
                        await self.wait_future
                    except asyncio.CancelledError:
                        return
                    msgs = session.master_get_msgs(seq)

                self.write_success_dict(msgs, seq)
            else:
                self.write_user_layer_error(1, 'session 失效')

        else:
            self.write_error_parameter(['session', 'seq'])


class SlaveConnectHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET']

    def get(self, *args, **kwargs):
        token = self.get_query_argument('token','')
        if token:
            try:
                msg = json.loads(self.request.body)
                if session_manager.master_send_msg(token, msg):
                    self.write_success_dict({})
                else:
                    self.write_user_layer_error(1,'session 失效')
            except json.JSONDecodeError:
                self.write_bad_request('not a json string')
        else:
            self.write_error_parameter(['session'])


class SlaveSyncMessageHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        uid = self.get_argument('uid', '')
        if uid:
            token = 'THESE IS A FAKE TOKEN'
            self.set_secure_cookie(self.COOKIE_NAME, uid + ':' + token)
            self.write_success_dict({})
        else:
            self.write_error_parameter(['uid'])


class SlaveSendHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        if self.current_user:
            self.clear_all_cookies()
            self.write_success_dict({})
        else:
            self.write_code_layer_error(403, 'Error: unvalue login')