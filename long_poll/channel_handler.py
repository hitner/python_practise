from tornado.web import RequestHandler
import json
import asyncio
import http_base_handler
import session_manager


class SessionHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        session = session_manager.create_session()
        self.write_success_dict({'session':session.token})



class MasterMsgHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST', 'GET']

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


    async def get(self, *args, **kwargs):
        self.set_no_cache()
        token = self.get_query_argument('token', '')
        seq = self.get_query_argument('seq', '-1')
        seq = int(seq)
        if token and seq >= 0:
            session = session_manager.session_from(token)
            if session:
                msgs = session.get_msgs(seq, 1)
                if not msgs:
                    try:
                        await session.wait(1)
                    except asyncio.CancelledError:
                        print('cancelled')
                        msgs = []
                msgs = session.get_msgs(seq, 1)
                if not msgs:
                    msgs = []

                self.write_success_dict({'msgs':msgs})
            else:
                self.write_user_layer_error(1, 'session 失效')

        else:
            self.write_error_parameter(['token', 'seq'])

    def compute_etag(self):
        return None


class SlaveMsgHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET', 'POST']

    async def get(self, *args, **kwargs):
        self.set_no_cache()
        token = self.get_query_argument('session', '')
        seq = self.get_query_argument('seq', '-1')
        seq = int(seq)
        if token and seq >= 0:
            session = session_manager.session_from(token)
            if session:
                msgs = session.get_msgs(seq)
                if not msgs:
                    try:
                        await session.wait()
                    except asyncio.CancelledError:
                        print('cancelled')
                        msgs = []
                msgs = session.get_msgs(seq)
                if not msgs:
                    msgs = []
                self.write_success_dict({'msgs' : msgs})
            else:
                self.write_user_layer_error(1, 'session 失效')

        else:
            self.write_error_parameter(['session', 'seq'])

    def compute_etag(self):
        return None

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


