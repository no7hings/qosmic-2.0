# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForRigBatch(_abstracts.AbsPrxPageForRigBatch):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForRigBatch, self).__init__(window, session, *args, **kwargs)
