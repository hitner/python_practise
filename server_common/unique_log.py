from logging import Logger, FileHandler, StreamHandler
import logging
import sys
import os


def create_logger(name, filename):
    log = Logger(name)
    hdlr = FileHandler(filename)
    hdlr.setLevel(logging.INFO)

    f = logging.Formatter('%(asctime)s %(process)d %(levelname)s:%(message)s')
    hdlr.setFormatter(f)
    log.addHandler(hdlr)
    if __debug__:
        terminal = StreamHandler(sys.stdout)
        terminal.setLevel(logging.DEBUG)
        log.addHandler(terminal)
    return log


LOG_DIR = '/var/log/zhixing'
LOG_NAME = 'common'

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
    print('mkdir %s success'%(LOG_DIR))

common_log = create_logger('common', os.path.join(LOG_DIR, f'${LOG_NAME}.log'))
