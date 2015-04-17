
<h1>MDB- MongoDB Models </h1>  

[![Build Status](https://travis-ci.org/RevelutionWind/MDB.svg?branch=master)](https://travis-ci.org/RevelutionWind/MDB)

<h2> Models </h2>
 Inorder to create a Model you first need to inherit Document class in Mongodb
 
 ```python
 from mdb.Connection import create_engine
 import mdb
 
 create_engine(database ="Management", host= "localhost", port=27017)
 
 ```