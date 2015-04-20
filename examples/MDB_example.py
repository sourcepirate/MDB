__author__ = 'plasmashadow'


from mondb.Connection import create_engine
import mondb
class Management(mondb.Document):

    name = mondb.StringProperty(str, required=True)
    age = mondb.StringProperty(str, required=True)

create_engine(database ="opendesk", host= "localhost", port=27017)


# m.save()
m = Management(name = "sathya", age= 13)
m.save()
cs = Management.find({"name":"sathya"})
print cs.next()
