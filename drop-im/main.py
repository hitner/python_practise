import asyncio
import tornado.ioloop
import tornado.web
import sys
import os
sys.path.append(os.path.join(os.pardir, 'server_common'))

from unique_log import common_log
import im_handler
import session_manager

from tornado.options import define, options, parse_command_line

define("port", default=9999, help="port given", type=int)
define("debug", default=True, help = "in debug mode")

def test():
    print('hello world')

def main():
    common_log.info('drop im module start...')
    parse_command_line()
    settings = dict(
        debug = options.debug
    )
    app = tornado.web.Application([
        (r"/dropim/getConnectionAttribute", im_handler.MasterCreateHandler),
        (r"/dropim/webSend", im_handler.MasterSendHandler),
        (r"/dropim/syncWebMessages", im_handler.MasterSyncMessageHandler),
        (r"/dropim/connect", im_handler.SlaveConnectHandler),
        (r"/dropim/syncClientMessages",im_handler.SlaveSyncMessageHandler),
        (r"/dropim/clientSend",im_handler.SlaveSendHandler),
    ], **settings,
    )




    app.listen(options.port)

    session_manager.start_period_check()

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()