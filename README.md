
#MDB- MongoDB Models

[![Build Status](https://travis-ci.org/RevelutionWind/MDB.svg?branch=master)](https://travis-ci.org/RevelutionWind/MDB)
[![PyPI version](https://badge.fury.io/py/mondb.svg)](http://badge.fury.io/py/mondb)
[![PyPI](https://img.shields.io/pypi/dm/mondb.svg)](https://pypi.python.org/pypi/mondb)
[![Code Health](https://landscape.io/github/RevelutionWind/MDB/master/landscape.svg?style=flat)](https://landscape.io/github/RevelutionWind/MDB/master)

##Installation
  
  You can install mondb from its official pypi repository.
  
  ```
   pip install mondb

  ```

##Models
 Inorder to create a Model you first need to inherit Document class in Mondb
 
 ```python
 from mondb.Connection import create_engine
 import mondb
 
 
 #used to establish a connection with the collection
 create_engine(database ="Management", host= "localhost", port=27017)
 
 
 class User(mdb.Document):
     name = mondb.StringProperty()
     age = mondb.IntegerProperty()
 
 m = User(name = "sathya", age =23)
 m.save()
 ```
 
##Searching and Updating

 In most of the case where the user needs to search and update models.
 Mondb comes with methods such as <b>search()</b> and <b>find()</b> for finding
 a document from the collection.
 
 
 ```python
 
 #search returns a matching records as pymongo cursor.
 cursor = User.search(name="sathya")
 
 # Note:
 #    cursor is not a list but can be indexed. use list(cursor) if you want to use
 #    it as a list
 
 for record in cursor:
     print record
 
 ```
 
##Query
 
 Mondb also comes with a Query object where you can Query with some 
 criteria.
 
 ```python
 
 query = mondb.Query(User)
 
 query.filter("age", ">=", 20)
 
 lst = query.fetch()
 
 for l in lst:
     print l
 
 ```
 
 Methods such as <b>filter()</b> and <b> fetch()</b> will be handy for getting results from
 the query.
 
 
##Deleting

 Mondb models can be deleted with the help of <b> delete() </b> method.
 
 ```python
 
 user = User.search(age=23)[0]
 user.delete()
 
 ```
 
 
##License

<h4>MIT</h4>
 
 
 