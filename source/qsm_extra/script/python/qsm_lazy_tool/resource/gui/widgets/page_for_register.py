# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForRegister(_abstracts.AbsPrxPageForRegister):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForRegister, self).__init__(window, session, *args, **kwargs)

