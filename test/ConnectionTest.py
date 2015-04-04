__author__ = 'plasmashadow'

import unittest

from mdb.Connection import AbstractConnection


class TestAbstractConnection(unittest.TestCase):

    def TestUrlParse(self):
        obj = AbstractConnection(host="localhost",
                                 username="plasmashadow",
                                 password="aidenfrost"
                                 )
        print obj._connection_url
        self.assertIsNotNone(obj)

