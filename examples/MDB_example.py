__author__ = 'plasmashadow'


from mdb.Connection import create_engine
import mdb
class MyModel(mdb.Document):

    name = mdb.Property(str, required=True)
    age = mdb.Property(int, required=True)

create_engine(database ="opendesk", host= "localhost", port=27017)