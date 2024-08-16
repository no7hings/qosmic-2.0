# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForRigValidation(_abstracts.AbsPrxPageForRigValidation):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForRigValidation, self).__init__(window, session, *args, **kwargs)
