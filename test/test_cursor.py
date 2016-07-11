import unittest
from mondb.Cursor import MongoCursor


class TestCursorInterface(unittest.TestCase):

    def setUp(self):
        create_engine('test', host="localhost", port=27017)

        class User(object):
            pass

        self.cursor = MongoCursor(User,
                                  limit=100,
                                  offset=0,
                                  start_cursor=None)

    def test_cursor_next(self):

        obj = self.cursor.next()
        self.assertIsNotNone(obj)

    def test_cursor_limit(self):

        obj = self.cursor.count()
        self.assertEqual(obj, 100)
