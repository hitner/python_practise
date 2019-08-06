import asyncio
import tornado.ioloop
import tornado.web
import sys
import os
from tornado.log import gen_log, app_log
import logging
sys.path.append(os.path.join(os.pardir, 'server_common'))

import channel_handler
import channel_manager

from tornado.options import define, options, parse_command_line

define("port", default=8801, help="port given", type=int)
define("debug", default=True, help = "in debug mode")



def main():
    parse_command_line()
    gen_log.setLevel(logging.INFO)
    gen_log.info('long poll start ...,listen on port:%d' % options.port)

    settings = dict(
        debug = options.debug
    )
    app = tornado.web.Application([
        (r"/longpoll/(.+)/message", channel_handler.MessageHandler),
        (r"/longpoll/", channel_handler.CreateChannelHandler),
        (r"/longpoll/(.+)", channel_handler.SessionHandler),
    ], **settings,
    )




    app.listen(options.port)

    channel_manager.start_period_check()

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()