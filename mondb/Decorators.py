__author__ = 'plasmashadow'

class notinstancemethod(object):
    """
    Used to refuse access to a classmethod if called from
    an instance.
    """

    def __init__(self, func):
        self.func = classmethod(func)

    def __get__(self, obj, objtype=None):
        if obj is not None:
            raise TypeError("Cannot call this method on an instance.")
        return self.func.__get__(obj, objtype)


def deprecated(self,func, *args, **kwargs):
    print "%s is deprecated and not safe to use for huge Collections" %(func.__name__)
    def inner(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return inner(self, *args, **kwargs)