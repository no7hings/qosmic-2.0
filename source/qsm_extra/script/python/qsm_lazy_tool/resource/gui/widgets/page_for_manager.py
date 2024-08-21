# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForResourceManager(_abstracts.AbsPrxPageForManager):
    PAGE_KEY = 'manager'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForResourceManager, self).__init__(window, session, *args, **kwargs)
