# coding:utf-8
import qsm_lazy_resource.gui.abstracts as _abstracts


class PrxPageForResourceManager(_abstracts.AbsPrxPageForManager):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForResourceManager, self).__init__(window, session, *args, **kwargs)
