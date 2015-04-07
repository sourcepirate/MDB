__author__ = 'plasmashadow'

import mdb


class SampleDoc(mdb.Document):
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