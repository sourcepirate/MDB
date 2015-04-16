__author__ = 'plasmashadow'


from mdb.Connection import create_engine
import mdb
class MyModel(mdb.Document):

    name = mdb.StringProperty(str, required=True)
    age = mdb.StringProperty(int, required=True)

create_engine(database ="opendesk", host= "localhost", port=27017)


# m.save()
m = MyModel(name = "sathya", age= 13)
print m.name
c = MyModel.search({"name": "sathya"})
c[0]
