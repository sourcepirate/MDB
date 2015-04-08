
<h1>MDB- MongoDB Models </h1>  

[![Build Status](https://travis-ci.org/RevelutionWind/MDB.svg?branch=master)](https://travis-ci.org/RevelutionWind/MDB)

For creating a new Model:

```python
conn = create_engine(host="localhost", database="opendesk")

class SampleDoc(mdb.Document):
    __connection__ = conn
    name = mdb.StringData()
    age = mdb.IntegerData()

s = SampleDoc()
s.name = "hello"
s.age = 13

```