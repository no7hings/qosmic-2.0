# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForRegisterTool(_abstracts.AbsPrxPageForRegisterTool):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForRegisterTool, self).__init__(window, session, *args, **kwargs)

