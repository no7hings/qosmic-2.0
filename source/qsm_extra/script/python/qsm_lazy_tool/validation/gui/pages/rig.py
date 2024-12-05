# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForChrRig(_abstracts.AbsPrxPageForChrRig):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForChrRig, self).__init__(window, session, *args, **kwargs)
