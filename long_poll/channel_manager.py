import secrets
import tornado.locks
from tornado.ioloop import IOLoop
from tornado.log import gen_log
import asyncio

channel_pool = {}


class MessageBuffer:
    def __init__(self, size=10):
        self.cond = tornado.locks.Condition()
        self.cache = []
        self.cache_size = size
        self.cursor = 0  # cursor的含义是下一个消息的编号

    def get_message_since(self, cursor):
        for i in range(0, len(self.cache)):
            if self.cache[i]['seq'] >= cursor:
                return self.cache[i: len(self.cache)]

    def add_message(self, msg: dict, seq):
        if seq != -1:
            if seq < self.cursor:
                return False
            else:
                self.cursor = seq

        msg['seq'] = self.cursor
        self.cursor = self.cursor + 1
        self.cache.append(msg)

        if len(self.cache) > self.cache_size:
            self.cache = self.cache[int(self.cache_size / 2):]

        self.cond.notify_all()
        return True


SYNC_TIME_OUT = 15
DESTROY_TIMEOUT = 300


class Channel:
    def __init__(self, tk, json_parameter):
        self.channel_id = tk
        self.last_poll_time = IOLoop.current().time()

        if 'cacheSize' in json_parameter:
            self.cache_size = json_parameter['cacheSize']
        else:
            self.cache_size = 10

        if 'pollTimeout' in json_parameter:
            self.poll_timeout = json_parameter['pollTimeout']
        else:
            self.poll_timeout = SYNC_TIME_OUT

        if 'autoRemove' in json_parameter:
            self.auto_remove = json_parameter['autoRemove']
        else:
            self.auto_remove = 1

        if self.auto_remove:
            if 'silenceTick' in json_parameter:
                self.destroy_timeout = json_parameter['silenceTick']
            else:
                self.destroy_timeout = DESTROY_TIMEOUT

        self.message_buffer = MessageBuffer(self.cache_size)

        self.configuration = json_parameter

    def get_describe(self):
        return {'channel': self.channel_id,
                'cacheSize': self.cache_size,
                'pollTimeout': self.poll_timeout,
                'autoRemove': self.auto_remove,
                'silenceTick': self.destroy_timeout}

    def get_messages(self, seq):
        now_time = IOLoop.current().time()
        self.last_poll_time = now_time
        return self.message_buffer.get_message_since(seq)

    def wait(self):
        io_loop = IOLoop.current()
        return self.message_buffer.cond.wait(timeout=io_loop.time() + self.poll_timeout)

    def is_valuable(self):
        now_time = IOLoop.current().time()
        if now_time - self.last_poll_time > self.destroy_timeout:
            return False
        else:
            return True


def create_channel(json_param):
    """
    创建一个推送频道
    :param json_param:
    :return: 频道配置信息
    """
    channel_id = secrets.token_urlsafe(9)
    while channel_id in channel_pool:
        channel_id = secrets.token_urlsafe(9)
    ses = Channel(channel_id, json_param)
    channel_pool[channel_id] = ses

    return ses.get_describe()


def send_message_to_channel(channel_id, msg, seq):
    if channel_id not in channel_pool:
        return None
    session = channel_pool[channel_id]
    return session.message_buffer.add_message(msg, seq)


async def poll_messages_from_channel(channel_id, seq):
    if channel_id not in channel_pool:
        return None
    session = channel_pool[channel_id]
    if session:
        msgs = session.get_messages(seq)
        if not msgs:
            try:
                await session.wait()
            except asyncio.CancelledError:
                print('cancelled')
        msgs = session.get_messages(seq)
        if not msgs:
            msgs = []
        return msgs


def get_channel_info(channel_id):
    if channel_id not in channel_pool:
        return None
    channel = channel_pool[channel_id]
    return channel.get_describe()


def delete_channel(channel_id):
    if channel_id not in channel_pool:
        return False
    else:
        channel_pool[channel_id].message_buffer.cond.notify_all()
        del channel_pool[channel_id]
        return True


def period_check():
    will_delete = []
    for key, session in channel_pool.items():
        if session.auto_remove:
            if not session.is_valuable():
                will_delete.append(key)

    for key in will_delete:
        gen_log.info('remove channel:' + key)
        del channel_pool[key]
    gen_log.info('remain channel count: %d' % len(channel_pool))


def start_period_check():
    a = tornado.ioloop.PeriodicCallback(period_check, 1000 * DESTROY_TIMEOUT, 0.1)
    a.start()
