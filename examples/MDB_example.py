__author__ = 'plasmashadow'


from mondb.Connection import create_engine
from mondb.Query import Query
import mondb
class Company(mondb.Document):
    name = mondb.StringProperty()
    age = mondb.IntegerProperty()
# class Management(mondb.Document):
#
#     name = mondb.StringProperty(required=True)
#     age = mondb.StringProperty(required=True)
#     company = mondb.ReferenceProperty(Company)




create_engine(database ="opendesk", host= "localhost", port=27017)

# c = Company(age= 13)
# c.name = "hello"
# c.save()
# c.delete()
# # m.save()
# cs = Company.search({"age": 23})
# print [cs.key() for cs in cs]
# #
# m = Management(name = "sathya", age= 13, company = c)
# m.save()
# cs = Management.find({"name":"sathya"})
# # print cs[0].company
#
q = Query(Company)
q.filter("age", ">=", 5)
cs = q.fetch(limit=2)
print cs

for c in cs:
    print c.age
    c.delete()
