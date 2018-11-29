import asyncio
import tornado.ioloop
import tornado.web
import sys
import os
from tornado.log import gen_log, app_log
import logging
sys.path.append(os.path.join(os.pardir, 'server_common'))

import http_test_handler
import set_manager

from tornado.options import define, options, parse_command_line

define("port", default=8800, help="port given", type=int)
define("debug", default=True, help = "in debug mode")




def main():
    sys.argv.append('--log_file_prefix=./test.log')
    sys.argv.append('--log_file_num_backups=4')
    sys.argv.append('--log_file_max_size=16777216') #16M
    parse_command_line()
    gen_log.setLevel(logging.INFO)
    gen_log.info('http_test start ...')

    settings = dict(
        debug = options.debug
    )

    app = tornado.web.Application([
        (r"/testsets", http_test_handler.TestSetsHandler),
        (r"/testsets/([0-9]+)", http_test_handler.SetHandler),
        (r"/testsets/(.+)/interface/([0-9]*)", http_test_handler.SetInterfaceHandler),
    ], **settings,
    )


    app.listen(options.port)

    set_manager.init()
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()