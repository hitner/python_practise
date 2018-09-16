from logging import Logger, FileHandler, StreamHandler
import logging
import sys

ddzLog = Logger('doudizhu')

hdlr = FileHandler('ddz.log')
hdlr.setLevel(logging.INFO)

terminal = StreamHandler(sys.stdout)
terminal.setLevel(logging.WARN)

ddzLog.addHandler(hdlr)
ddzLog.addHandler(terminal)
