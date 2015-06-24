__author__ = 'plasmashadow'

import unittest
import mock
import mondb
from mondb.Connection import create_engine
import random


class CrudTest(unittest.TestCase):
    def setUp(self):
        create_engine(host="localhost", port=27017, database="test")
        self.age_number = random.choice(range(100))
        class User(mondb.Document):
            name = mondb.StringProperty()
            age = mondb.IntegerProperty()

        self.User = User
        self.User(name="adhi", age= self.age_number).save()

    def test_save(self):
        user = self.User()
        user.name = "sathya"
        user.age = self.age_number
        user.save()
        self.assertEqual(user.name, "sathya")

    def test_search(self):
        results = self.User.search(age=self.age_number)
        self.assertEqual(len(results), 1)


