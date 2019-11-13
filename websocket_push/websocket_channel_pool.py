import secrets
import tornado
from tornado.log import gen_log

CHANNEL_NAME_LENGTH = 9
ERROR_CHANNEL_NOT_FOUND = 'cannot find this channel'

channel_pool = {}

class WebSocketChannel():
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.clients = []

    def get_info(self):
        return {"channel_name":self.channel_name}

    def broadcast_message(self, message):
        for client in self.clients:
            try:
                client.write_message(message)
            except tornado.websocket.WebSocketClosedError:
                gen_log.warning(f'write message to one client of channel:{self.channel_name}')
                
    def close_all_client(self):
        for client in self.clients:
            try:
                client.close()
            except Exception as e:
                gen_log.warning(f'close exception {str(e)}')



def wi_create_channel():
    """创建一个连接点，返回一个字典，描述该连接点的信息
    """
    channel_id = secrets.token_urlsafe(CHANNEL_NAME_LENGTH)
    while channel_id in channel_pool:
        channel_id = secrets.token_urlsafe(CHANNEL_NAME_LENGTH)
    ses = WebSocketChannel(channel_id)
    channel_pool[channel_id] = ses
    return ses.get_info()


def wi_send_message_to_channel(channel_name, json_message):
    """
    将一个信息推送到某个websocket点
    """
    if channel_name not in channel_pool:
        return ERROR_CHANNEL_NOT_FOUND
    session = channel_pool[channel_name]
    session.broadcast_message(json_message)
    return {}


def wi_delete_channel(channel_name):
    """
    删除一个websocket 点，原有连接全部断掉
    """
    if channel_name not in channel_pool:
        return ERROR_CHANNEL_NOT_FOUND
    else:
        channel_pool[channel_name].close_all_client()
        del channel_pool[channel_name]
        return {}

def i_has_channel(channel_name):
    return channel_name in channel_pool


def i_add_client(channel_name, client):
    assert channel_name in channel_pool
    channel = channel_pool[channel_name]
    channel.clients.append(client)

def i_remove_client(channel_name, client):
    assert channel_name in channel_pool
    channel = channel_pool[channel_name]
    channel.clients.remove(client) 
