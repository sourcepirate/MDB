__author__ = 'plasmashadow'
import socket
import logging
log = None
if socket.gethostname() == 'plasmashadow-desktop':
    logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("MONDB")