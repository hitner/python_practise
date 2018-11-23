import secrets
import threading
import tornado.locks
from tornado.ioloop import IOLoop


session_pool = {}

class MessageBuffer:
    def __init__(self, size=10):
        self.cond = tornado.locks.Condition()
        self.cache = []
        self.cache_size = size
        self.cursor = 0

    def get_message_since(self, cursor):
        for i in range(0, len(self.cache)):
            if self.cache[i]['seq'] > cursor:
                return self.cache[i: len(self.cache)]

    def add_message(self, msg: dict):
        self.cursor = self.cursor + 1
        msg['seq'] = self.cursor
        self.cache.append(msg)

        if len(self.cache) > self.cache_size:
            self.cache = self.cache[int(self.cache_size / 2):]

        print('notify all')
        self.cond.notify_all()


WAITING_SLAVE = 1
CONNECTED = 2
SYNC_TIME_OUT = 60
DESTROY_TIMEOUT = 300



class Session:
    def __init__(self, tk):
        self.token = tk
        self.state = WAITING_SLAVE
        self.master_send_msgs_buffer = MessageBuffer()
        self.slave_send_msgs_buffer = MessageBuffer()
        self.master_last_req_time = IOLoop.current().time()
        self.slave_last_req_time = IOLoop.current().time()

    def get_msgs(self, seq, is_slave=0):
        now_time = IOLoop.current().time()
        print(now_time)
        if not is_slave:
            self.master_last_req_time = now_time
            return self.slave_send_msgs_buffer.get_message_since(seq)
        else:
            self.slave_last_req_time = now_time
            return self.master_send_msgs_buffer.get_message_since(seq)

    def wait(self, is_slave=0):
        io_loop = IOLoop.current()
        if not is_slave:
            return self.slave_send_msgs_buffer.cond.wait(timeout=io_loop.time() + SYNC_TIME_OUT)
        else:
            return self.master_send_msgs_buffer.cond.wait(timeout=io_loop.time() + SYNC_TIME_OUT)

    def slave_in(self):
        self.state = CONNECTED
        self.slave_send_msgs_buffer.add_message({'cmd': 1})

    def is_slave_not_in(self):
        return self.state == WAITING_SLAVE

    def is_valued(self):
        now_time = IOLoop.current().time()
        if now_time - self.slave_last_req_time > DESTROY_TIMEOUT and \
            now_time - self.master_last_req_time > DESTROY_TIMEOUT :
            return False
        else:
            return True


def create_session():
    token = secrets.token_urlsafe(9)
    while token in session_pool:
        token = secrets.token_urlsafe(9)
    ses = Session(token)
    session_pool[token] = ses
    return ses


def master_send_msg(token, msg):
    if token not in session_pool:
        return None
    session = session_pool[token]
    if session:
        session.master_send_msgs_buffer.add_message(msg)
        return True


def slave_send_msg(token, msg):
    if token not in session_pool:
        return None
    session = session_pool[token]
    if session:
        session.slave_send_msgs_buffer.add_message(msg)
        return True


def session_from(token):
    if token in session_pool:
        return session_pool[token]


def period_check():
    print('now checking')
    will_delete = []
    for key, session in session_pool.items():
        if not session.is_valued():
            will_delete.append(key)

    for key in will_delete:
        print('remote session:' + key)
        del session_pool[key]


def start_period_check():
    a = tornado.ioloop.PeriodicCallback(period_check, 1000 * DESTROY_TIMEOUT, 0.1)
    a.start()
