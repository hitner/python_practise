from tornado.web import RequestHandler
import json
import asyncio
import http_base_handler
import channel_manager


class CreateChannelHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        if self.request.body:
            json_parameter = json.loads(self.request.body)
        else:
            json_parameter = {}
        session = channel_manager.create_channel(json_parameter)
        self.write_success_dict(session)


class SessionHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET', 'DELETE']

    def get(self, *args, **kwargs):
        channel_id = args[0]
        channel_info = channel_manager.get_channel_info(channel_id)
        if channel_info:
            self.write_success_dict(channel_info)
        else:
            self.write_user_layer_error(1, "channel失效")

    def delete(self, *args, **kwargs):
        channel_id = args[0]
        result = channel_manager.delete_channel(channel_id)
        if result:
            self.write_success_dict({})
        else:
            self.write_user_layer_error(1, "channel失效")



class MessageHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST', 'GET']

    def post(self, *args, **kwargs):
        channel_id = args[0]
        seq = self.get_query_argument('seq', '-1')
        seq = int(seq)
        try:
            msg = json.loads(self.request.body)
            if channel_manager.send_message_to_channel(channel_id, msg, seq):
                self.write_success_dict({})
            else:
                self.write_user_layer_error(1,'channel 失效')
        except json.JSONDecodeError:
            self.write_bad_request('not a json string')
#        else:
#            self.write_error_parameter(['session'])


    async def get(self, *args, **kwargs):
        self.set_no_cache()
        channel_id = args[0]
        seq = self.get_query_argument('seq', '-1')
        seq = int(seq)
        if seq >= 0:
            msgs = await channel_manager.poll_messages_from_channel(channel_id, seq)
            if msgs or isinstance(msgs, list):
                self.write_success_dict({'msgs': msgs})
            else:
                self.write_user_layer_error(1, 'channel 失效')

        else:
            self.write_error_parameter(['seq'])

    def compute_etag(self):
        return None

#
# class SlaveMsgHandler(http_base_handler.BaseHandler):
#     ALLOWED_METHODS = ['GET', 'POST']
#
#     async def get(self, *args, **kwargs):
#         self.set_no_cache()
#         token = self.get_query_argument('session', '')
#         seq = self.get_query_argument('seq', '-1')
#         seq = int(seq)
#         if token and seq >= 0:
#             session = channel_manager.session_from(token)
#             if session:
#                 msgs = session.get_msgs(seq)
#                 if not msgs:
#                     try:
#                         await session.wait()
#                     except asyncio.CancelledError:
#                         print('cancelled')
#                         msgs = []
#                 msgs = session.get_msgs(seq)
#                 if not msgs:
#                     msgs = []
#                 self.write_success_dict({'msgs' : msgs})
#             else:
#                 self.write_user_layer_error(1, 'session 失效')
#
#         else:
#             self.write_error_parameter(['session', 'seq'])
#
#     def compute_etag(self):
#         return None
#
#     def post(self, *args, **kwargs):
#         token = self.get_query_argument('token','')
#         if token:
#             try:
#                 msg = json.loads(self.request.body)
#                 if channel_manager.slave_send_msg(token, msg):
#                     self.write_success_dict({})
#                 else:
#                     self.write_user_layer_error(1,'token 失效')
#             except json.JSONDecodeError:
#                 self.write_bad_request('not a json string')
#         else:
#             self.write_error_parameter(['token'])
#
#
