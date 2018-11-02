import asyncio
import tornado.ioloop
import tornado.web
import sys
import os
sys.path.append(os.path.join(os.pardir, 'server_common'))


from dlog import ddzlog
import RoomHandler

from tornado.options import define, options, parse_command_line

define("port", default=8880, help="port given", type=int)
define("debug", default=True, help = "in debug mode")


def main():
    ddzlog.info('doudizhu start...')
    parse_command_line()
    settings = dict(
        cookie_secret = "0fa2ds88fce9dcb225c0fpda8bd7b3kbcd46b2",
        debug = options.debug
    )
    app = tornado.web.Application([
        (r"/auth/login",RoomHandler.DdzAuthLoginHandler),
        (r"/auth/logout", RoomHandler.DdzAuthLogoutHandler),
    ], **settings,
    )




    app.listen(options.port)

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()