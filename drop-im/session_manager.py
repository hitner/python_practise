import secrets
import tornado.locks

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


class Session:
    WAITING_SLAVE = 1
    CONNECTED = 2

    def __init__(self, tk):
        self.token = tk
        self.state = self.WAITING_SLAVE
        self.master_send_msgs_buffer = MessageBuffer()
        self.slave_send_msgs_buffer = MessageBuffer()

    def get_msgs(self,seq, is_slave=0):
        if not is_slave:
            return self.slave_send_msgs_buffer.get_message_since(seq)
        else:
            return self.master_send_msgs_buffer.get_message_since(seq)

    def wait(self, is_slave=0):
        if not is_slave:
            return self.slave_send_msgs_buffer.cond.wait()
        else:
            return self.master_send_msgs_buffer.cond.wait()

    def slave_in(self):
        self.state = self.CONNECTED
        self.slave_send_msgs_buffer.add_message({'cmd': 1})


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

