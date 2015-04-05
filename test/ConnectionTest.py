__author__ = 'plasmashadow'

import unittest

from mdb.Connection import AbstractConnection


class TestAbstractConnection(unittest.TestCase):

    def TestUrlParse(self):
        obj = AbstractConnection(host="localhost",
                                 username="plasmashadow",
                                 password="aidenfrost"
                                 )
        self.assertIsNotNone(obj)

