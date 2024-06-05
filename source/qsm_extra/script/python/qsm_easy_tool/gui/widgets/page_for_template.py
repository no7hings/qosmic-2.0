# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForTemplate(_abstracts.AbsPrxPageForTemplate):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForTemplate, self).__init__(window, session, *args, **kwargs)
