# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForScnModelBatch(_abstracts.AbsPrxPageForSceneryBatch):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForScnModelBatch, self).__init__(window, session, *args, **kwargs)
