__author__ = 'plasmashadow'

import unittest
import mondb
from mondb.Connection import create_engine
import random, json


class CrudTest(unittest.TestCase):
    def setUp(self):
        create_engine(host="localhost", port=27017, database="test")

        class User(mondb.Document):
            name = mondb.StringProperty()
            age = mondb.IntegerProperty()
            time = mondb.DateTimeProperty(auto_add=True)
            lst = mondb.ListProperty()
            dct = mondb.DictProperty()
            jsn = mondb.JsonProperty()

        self.User = User


    def test_save(self):
        user = self.User()
        user.name = "sathya"
        user.age = 23
        user.lst = [1, 2, 5]
        user.dct = {'tara': 'adhi'}
        user.jsn = json.dumps({"hey": "hello"})
        user.save()
        results = self.User.find({})
        for res in results:
            print res.time, res.dct, res.lst, res.jsn
        self.assertEqual(user.name, "sathya")

    def test_search(self):
        self.age_number = random.choice(range(100))
        self.User(name="adhi", age= self.age_number).save()
        results = self.User.search(age=self.age_number)
        self.assertEqual(len(results), 1)




