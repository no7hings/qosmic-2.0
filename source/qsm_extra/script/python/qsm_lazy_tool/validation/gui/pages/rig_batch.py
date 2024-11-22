# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForChrRigBatch(_abstracts.AbsPrxPageForRigBatch):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForChrRigBatch, self).__init__(window, session, *args, **kwargs)
