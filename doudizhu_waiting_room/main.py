import tornado.ioloop
import tornado.web
import sys
import os
from tornado.log import gen_log
sys.path.append(os.path.join(os.pardir, 'server_common'))
import launch_config
from tornado.options import define, options, parse_command_line
import waiting_room_handler

SERVER_NAME = 'doudizhu_waiting_room'
define("port", default=8810, help="port given", type=int)
define("debug", default=False, help = "in debug mode")

def main():
    launch_config.config_log(SERVER_NAME)
    parse_command_line()

    gen_log.info(f'{SERVER_NAME} start ...,listen on port:%d'%options.port)


    settings = dict(
        debug = True,
        cookie_secret = launch_config.COOKIE_SECRET
    )
    app = tornado.web.Application([
        (r"/doudizhu/waiting_rooms/(.+)/players/([0-9]*)", waiting_room_handler.RoomPlayersHandler),
        (r"/doudizhu/waiting_rooms", waiting_room_handler.CreateRoomHandler),
        (r"/doudizhu/waiting_rooms/(.+)", waiting_room_handler.RoomInfoHandler),
    ], **settings,
    )

    app.listen(options.port)

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()