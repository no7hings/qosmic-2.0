# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForLoadTool(_abstracts.AbsPrxPageForLoad):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForLoadTool, self).__init__(window, session, *args, **kwargs)

