import asyncio
import tornado.ioloop
import tornado.web
from dlog import ddzLog
import RoomHandler

from tornado.options import define, options, parse_command_line

define("port", default=8880, help="port given", type=int)
define("debug", default=True, help = "in debug mode")


def main():
    ddzLog.info('doudizhu start...')
    parse_command_line()
    settings = dict(
        cookie_secret = "0fa2ds88fce9dcb225c0fpda8bd7b3kbcd46b2",
        debug = options.debug
    )
    app = tornado.web.Application([
        (r"/auth/login",RoomHandler.DdzAuthLoginHandler),
        (r"/auth/logout", RoomHandler.DdzAuthLogoutHandler),
        (r"/doudizhu/room/([0-9]+)", RoomHandler.DdzRoomHandler),
        (r"/doudizhu/room/([0-9]+)/messages", RoomHandler.DdzRoomMessagesHandler),
        (r"/doudizhu/room/([0-9]+)/players/([0-2]?)", RoomHandler.DdzRoomPlayerHandler), #support GET POST DELETER
        (r"/doudizhu/room/([0-9]+)/played-cards", RoomHandler.DdzRoomPlayedCardsHandler), #support POST only now
        (r"/doudizhu/room/([0-9]+)/master-bid", RoomHandler.DdzRoomMasterBidHandler),  # support GET POST
        (r"/doudizhu/room/([0-9]+)/ready", RoomHandler.DdzRoomReadyHandler),  # support GET POST
        #(r"/dealcard", DealCardHandler),
        #(r"/getmycards", GetMyCardsHandler),
        #(r"/randomjoinroom", RandomJoinRoomHandler),
        #(r"/leaveroom", LeaveRoomHandler),
        #(r"/pollchanges", PollChangesHandler),
        #(r"/askformaster", AskForMasterHandler),
        #(r"/restartgame", RestartGameHandler)
    ], **settings,
    )




    app.listen(options.port)

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()