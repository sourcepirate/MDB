__author__ = 'plasmashadow'


from mondb.Connection import create_engine
import mondb
class Company(mondb.Document):
    name = mondb.StringProperty()
class Management(mondb.Document):

    name = mondb.StringProperty(required=True)
    age = mondb.StringProperty(required=True)
    company = mondb.ReferenceProperty(Company)




create_engine(database ="opendesk", host= "localhost", port=27017)

c = Company(name = "Google")
c.save()
print c._id
# # m.save()
cs = Company.find({"name": "Google"})
print [cs._id.__str__() for cs in cs]

m = Management(name = "sathya", age= 13, company = c)
m.save()
cs = Management.find({"name":"sathya"})
# print cs[0].company
