import unittest
from mondb.Connection import Connection
from mondb import create_engine


class TestConnection(unittest.TestCase):
    """Testing connection interface"""

    def setUp(self):
        create_engine('test', host="localhost", port=27017)

    def test_connection(self):
        db = Connection.get_connection('test')
        self.assertIsNotNone(db)

    def test_ping(self):
        flag = Connection.is_alive()
        self.assertTrue(flag)
