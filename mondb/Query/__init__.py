__author__ = 'plasmashadow'

from mondb.Cursor import Cursor

class Query(object):

    def __init__(self, Model):
        self.model = Model
        self._start_id = None
        self.cursor = Cursor(self.model)
        self.count = self.model.count()

    def add_filter(self, **kwargs):
        pass

    def fetch(self, offset=None, start_cursor=None):
        if not offset:
            self.model.find()