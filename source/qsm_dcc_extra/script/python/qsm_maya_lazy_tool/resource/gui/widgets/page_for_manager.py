# coding:utf-8
import qsm_lazy_tool.resource.gui.abstracts as _abstracts


class PrxPageForManager(_abstracts.AbsPrxPageForManager):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForManager, self).__init__(window, session, *args, **kwargs)
