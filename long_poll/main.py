import asyncio
import tornado.ioloop
import tornado.web
import sys
import os
from tornado.log import gen_log, app_log
import logging
sys.path.append(os.path.join(os.pardir, 'server_common'))

import channel_handler
import session_manager
import qiniu_token

from tornado.options import define, options, parse_command_line

define("port", default=9999, help="port given", type=int)
define("debug", default=True, help = "in debug mode")
define("secret")



def main():
    parse_command_line()
    gen_log.setLevel(logging.INFO)
    gen_log.info('DROP-IM start ...,listen on port:%d' % options.port)

    settings = dict(
        debug = options.debug
    )
    qiniu_token.qiniu_secret = options.secret
    app = tornado.web.Application([
        (r"/longpoll/(.+)/master_msg", channel_handler.MasterMsgHandler),
        (r"/longpoll/(.+)/slave_msg", channel_handler.SlaveMsgHandler),
        (r"/longpoll/(.*)", channel_handler.SessionHandler),
    ], **settings,
    )




    app.listen(options.port)

    session_manager.start_period_check()

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()