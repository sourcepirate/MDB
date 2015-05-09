__author__ = 'plasmashadow'
import socket
import logging

class Logger(object):

    def __init__(self):
        if socket.gethostname() == 'plasmashadow-desktop':
            logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger("MONGO")

    def info(self, msg):
        self.log.debug("INFO: "+str(msg))

    def error(self, msg):
        self.log.debug("ERROR: "+str(msg))

    def debug(self, msg):
        self.log.debug("DEBUG: "+str(msg))

