import asyncio
import tornado.ioloop
import tornado.web
from dlog import ddzLog


from RoomHandler import  RandomJoinRoomHandler, \
    DealCardHandler, PollChangesHandler,\
    GetMyCardsHandler,AskForMasterHandler, \
    LeaveRoomHandler, RestartGameHandler


from tornado.options import define, options, parse_command_line

define("port", default=8888, help="port given", type=int)
define("debug", default=True, help = "in debug mode")


def main():
    ddzLog.info('doudizhu start...')
    parse_command_line()
    app = tornado.web.Application([
        (r"/dealcard", DealCardHandler),
        (r"/getmycards", GetMyCardsHandler),
        (r"/randomjoinroom", RandomJoinRoomHandler),
        (r"/leaveroom", LeaveRoomHandler),
        (r"/pollchanges", PollChangesHandler),
        (r"/askformaster", AskForMasterHandler),
        (r"/restartgame", RestartGameHandler)
    ], debug = options.debug,
    )




    app.listen(options.port)

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()