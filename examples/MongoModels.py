__author__ = 'plasmashadow'

import mdb
from mdb import create_engine

conn = create_engine(host="localhost", database="opendesk")


class Meta:
    connection = conn

class DocumentConfig(mdb.Document, Meta):
    pass

class SampleDoc(DocumentConfig):
    name = mdb.StringData()
    age = mdb.IntegerData()

class Sample(mdb.Document, Meta):
    name = mdb.StringData()
    age = mdb.IntegerData()

s = SampleDoc()
s.name = "sathya"
s.age = 23
s.save()

print SampleDoc.get_by_id("55295ec885518d43b5ecc3e6")
# s.delete()
#
# d = SampleDoc()
#
# d.name = "adhi"
# d.age  = 23
# d.save()
# d.delete()

# SampleDoc._get_by_id("5529409f85518d2d6c62b6d0")

# s = Sample()
# s.name = "hg"
# s.age = 123
# s.save()
# s.delete()
