__author__ = 'plasmashadow'


from mdb.Connection import create_engine
import mdb
class Management(mdb.Document):

    name = mdb.StringProperty(str, required=True)
    age = mdb.StringProperty(str, required=True)

create_engine(database ="opendesk", host= "localhost", port=27017)


# m.save()
m = Management(name = "sathya", age= 13)
m.save()
cs = Management.find({"name":"sathya"})
print cs[0].name
