from tornado.web import RequestHandler
import json
import asyncio
import http_base_handler
import session_manager

HOST = 'http://192.168.10.237:8881/dropim/connect'

class MasterCreateHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET']

    def get(self, *args, **kwargs):
        session = session_manager.create_session()
        self.write_success_dict({'session':session.token,
                                 'QRCodeUrl': HOST+'?token='+session.token})



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
        seq = self.get_query_argument('seq', '-1')
        seq = int(seq)
        if token and seq >= 0:
            session = session_manager.session_from(token)
            if session:
                msgs = session.get_msgs(seq)
                while not msgs:
                    self.wait_future = session.wait()
                    try:
                        await self.wait_future
                    except asyncio.CancelledError:
                        return
                    msgs = session.get_msgs(seq)

                self.write_success_dict(msgs)
            else:
                self.write_user_layer_error(1, 'session 失效')

        else:
            self.write_error_parameter(['session', 'seq'])


class SlaveConnectHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET']

    def get(self, *args, **kwargs):
        token = self.get_query_argument('token','')
        if token:
            session = session_manager.session_from(token)
            if session and session.state == session.WAITING_SLAVE:
                self.write_success_dict({'token': token})
            else:
                self.write_user_layer_error(1, 'session 失效')
        else:
            self.write_error_parameter(['token'])


class SlaveSyncMessageHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET']

    wait_future = None

    async def get(self, *args, **kwargs):
        token = self.get_query_argument('token', '')
        seq = self.get_query_argument('seq', '-1')
        seq = int(seq)
        if token and seq >= 0:
            session = session_manager.session_from(token)
            if session:
                msgs = session.get_msgs(seq, 1)
                while not msgs:
                    self.wait_future = session.wait(1)
                    try:
                        await self.wait_future
                    except asyncio.CancelledError:
                        return
                    msgs = session.get_msgs(seq, 1)

                self.write_success_dict(msgs)
            else:
                self.write_user_layer_error(1, 'session 失效')

        else:
            self.write_error_parameter(['token', 'seq'])


class SlaveSendHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        token = self.get_query_argument('token','')
        if token:
            try:
                msg = json.loads(self.request.body)
                if session_manager.slave_send_msg(token, msg):
                    self.write_success_dict({})
                else:
                    self.write_user_layer_error(1,'token 失效')
            except json.JSONDecodeError:
                self.write_bad_request('not a json string')
        else:
            self.write_error_parameter(['token'])
