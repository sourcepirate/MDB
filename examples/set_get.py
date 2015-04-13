__author__ = 'plasmashadow'


class field(object):

    def __set__(self, instance, value):
        instance.__dict__.update({"c":value})

    def __get__(self, instance, owner):
        return instance.__dict__["c"]

class fielddict(object):

    def __set__(self, instance, value):
        instance["c"] =value

    def __get__(self, instance, owner):
        return instance["c"]

class hello(object):
    b = field()

class hellod(dict):
    b = fielddict()
h = hello()
h.b = 24
g = hellod()
g.b = 34
print g.b
print isinstance(dict(), object)
print "c" in dir(h)

# "c" won't be shown under scope
print "c" in dir(g)

print dir(g)