from logging import Logger, FileHandler, StreamHandler
import logging
import sys
import os


def create_logger(name, filename):
    log = Logger(name)
    hdlr = FileHandler(filename)
    hdlr.setLevel(logging.INFO)
    terminal = StreamHandler(sys.stdout)
    terminal.setLevel(logging.WARN)
    log.addHandler(hdlr)
    log.addHandler(terminal)
    return log


LOG_DIR = '/var/log/zhixing'

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
    print('mkdir %s success'%(LOG_DIR))

common_log = create_logger('common', os.path.join(LOG_DIR, 'common.log'))
