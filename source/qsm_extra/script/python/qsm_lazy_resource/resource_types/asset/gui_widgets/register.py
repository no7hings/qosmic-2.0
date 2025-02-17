# coding:utf-8
from ....gui import abstracts as _abstracts


class PrxSubpageForAssetRegister(_abstracts.AbsPrxSubpageForAssetRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForAssetRegister, self).__init__(window, session, subwindow, *args, **kwargs)
