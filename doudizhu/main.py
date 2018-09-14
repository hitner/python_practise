import asyncio
import tornado.ioloop
import tornado.web

from RoomHandler import  RandomJoinRoomHandler, DealCardHandler, PollChangesHandler,GetMyCardsHandler,AskForMasterHandler


from tornado.options import define, options, parse_command_line

define("port", default=8888, help="port given", type=int)
define("debug", default=True, help = "in debug mode")


def main():
    parse_command_line()
    app = tornado.web.Application([
        (r"/dealcard", DealCardHandler),
        (r"/getmycards", GetMyCardsHandler),
        (r"/randomjoinroom", RandomJoinRoomHandler),
        (r"/pollchanges", PollChangesHandler),
        (r"/askformaster", AskForMasterHandler),
    ], debug = options.debug,
    )

    app.listen(options.port)

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()