import asyncio
import tornado.ioloop
import tornado.web
import sys
import os
import tornado.log
sys.path.append(os.path.join(os.pardir, 'server_common'))

from unique_log import common_log
import im_handler
import session_manager
import qiniu_token

from tornado.options import define, options, parse_command_line

define("port", default=9999, help="port given", type=int)
define("debug", default=True, help = "in debug mode")
define("secret")

def test():
    print('hello world')

def main():
    common_log.info('drop im module start...')
    tornado.log.app_log.info('tornado self')
    parse_command_line()
    settings = dict(
        debug = options.debug
    )
    qiniu_token.qiniu_secret = options.secret
    app = tornado.web.Application([
        (r"/dropim/getConnectionAttribute", im_handler.MasterCreateHandler),
        (r"/dropim/webSend", im_handler.MasterSendHandler),
        (r"/dropim/syncWebMessages", im_handler.MasterSyncMessageHandler),
        (r"/dropim/connect", im_handler.SlaveConnectHandler),
        (r"/dropim/syncClientMessages",im_handler.SlaveSyncMessageHandler),
        (r"/dropim/clientSend",im_handler.SlaveSendHandler),
        (r"/dropim/getQiniuToken",im_handler.QiniuTokenHandler),
    ], **settings,
    )




    app.listen(options.port)

    session_manager.start_period_check()

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()