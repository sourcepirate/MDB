import unittest
import mock
from mondb.urltools import UrlBuilder


class TestUrlBuilder(unittest.TestCase):
    """test url builder"""

    def setUp(self):
        """setting up url test builder"""
        self.host = "localhost"
        self.port = 27017
        self.db = 'test'
        self.scheme = "mongodb"

    def test_host_port_builder(self):
        builder = UrlBuilder(scheme=self.scheme,
                             host=self.host,
                             port=self.port,
                             database=self.db)
        expected_string = "mongodb://localhost:27017/test/"
        self.assertEqual(str(builder), expected_string)

    def test_user_pass_builder(self):
        builder = UrlBuilder(scheme=self.scheme,
                             host=self.host,
                             port=self.port,
                             database=self.db,
                             username="admin",
                             password="admin")
        expected_string = "mongodb://admin:admin@localhost:27017/test/"
        self.assertEqual(str(builder), expected_string)
