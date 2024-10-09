# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForSceneryBatch(_abstracts.AbsPrxPageForSceneryBatch):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForSceneryBatch, self).__init__(window, session, *args, **kwargs)
