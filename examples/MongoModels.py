__author__ = 'plasmashadow'

import mdb
from mdb import create_engine

conn = create_engine(host="localhost", database="opendesk")

class SampleDoc(mdb.Document):
    __connection__ = conn
    name = mdb.StringData()
    age = mdb.IntegerData()

s = SampleDoc()
s.name = "sathya"
s.age = 34
s.save()
d = SampleDoc()
d.name = "adhi"
d.age  = 23
d.save()