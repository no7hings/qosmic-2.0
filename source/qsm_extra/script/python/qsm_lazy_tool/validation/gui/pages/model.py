# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForScnModel(_abstracts.AbsPrxPageForScnModel):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForScnModel, self).__init__(window, session, *args, **kwargs)
