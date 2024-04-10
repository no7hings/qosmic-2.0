# coding:utf-8
# resolver
from .. import abstracts as rsv_abstracts


class RsvAppDefault(rsv_abstracts.AbsRsvAppDefault):
    def __init__(self, *args, **kwargs):
        super(RsvAppDefault, self).__init__(*args, **kwargs)


class RsvAppNew(rsv_abstracts.AbsRsvAppNew):
    def __init__(self, *args, **kwargs):
        super(RsvAppNew, self).__init__(*args, **kwargs)
