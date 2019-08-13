import tornado.ioloop
import tornado.web
import sys
import os
sys.path.append(os.path.join(os.pardir, 'server_common'))
sys.path.append(os.path.join(os.pardir, 'card_game'))


import room_handler

from unique_log import common_log

from tornado.options import define, options, parse_command_line

define("port", default=8804, help="port given", type=int)
define("debug", default=True, help = "in debug mode")


def main():
    common_log.info('doudizhu start...')
    parse_command_line()
    settings = dict(
        cookie_secret = "0fa2ds88fce9dcb225c0fpda8bd7b3kbcd46b2",
        debug = options.debug
    )
    app = tornado.web.Application([
        (r"/doudizhu/rooms/(.*)/act", room_handler.DdzRoomActHandler),
        (r"/doudizhu/rooms/(.*)/players", room_handler.DdzRoomPlayersHandler),
        (r"/doudizhu/rooms/(.*)/afk", room_handler.DdzRoomAfkHandler),
        (r"/doudizhu/rooms/(.*)/ready", room_handler.DdzRoomReadyHandler),
       
    ], **settings,
    )
    app.listen(options.port)

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()