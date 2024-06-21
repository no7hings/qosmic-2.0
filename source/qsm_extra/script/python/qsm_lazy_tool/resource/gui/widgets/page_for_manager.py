# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForManager(_abstracts.AbsPrxPageForManager):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForManager, self).__init__(window, session, *args, **kwargs)
