# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForScenery(_abstracts.AbsPrxPageForScenery):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForScenery, self).__init__(window, session, *args, **kwargs)
