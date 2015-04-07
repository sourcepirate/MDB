__author__ = 'plasmashadow'
import unittest

from mdb.Property import StringData


class StringPropertyTest(unittest.TestCase):

    def setUp(self):
        self.v = type("Sample", (object,), {'s': StringData()})()
        self.globaldata = self.v

    def TestIsOnlyString(self):
        self.v = "hello"
        self.assertEqual(self.v, "hello")

    def TestExceptionRaise(self):

        def inner():
            sample = type("Sample", (object,), {'s': StringData()})()
            sample.s = "hello"

        self.assertRaises(TypeError, inner)
