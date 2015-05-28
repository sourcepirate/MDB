
#MDB- MongoDB Models

[![Build Status](https://travis-ci.org/RevelutionWind/MDB.svg?branch=master)](https://travis-ci.org/RevelutionWind/MDB)
[![PyPI version](https://badge.fury.io/py/mondb.svg)](http://badge.fury.io/py/mondb)
[![PyPI](https://img.shields.io/pypi/dm/mondb.svg)](https://pypi.python.org/pypi/mondb)
[![Code Health](https://landscape.io/github/RevelutionWind/MDB/master/landscape.svg?style=flat)](https://landscape.io/github/RevelutionWind/MDB/master)

##Installation
  Inorder to install
  
  ```
   pip install mondb

  ```

##Models
 Inorder to create a Model you first need to inherit Document class in Mongodb
 
 ```python
 from mdb.Connection import create_engine
 import mdb
 
 create_engine(database ="Management", host= "localhost", port=27017)
 
 class Management(mdb.Document):
     name = mdb.StringProperty()
     age = mdb.IntegerProperty()
 
 m = Management(name = "sathya", age =23)
 m.save()
 
 #inorder to query the entity
 
 cursor = Management.find({"name":"sathya"})
 for element in cursor:
    print element[0].name,element[0].age
    

 ```
 
 
##Query
 
 ```
 
  query = mdb.Query(Management)
  query.filter("name", "==", "sathya")
  lst = query.fetch()
  for l in lst:
      print l
      
 ```