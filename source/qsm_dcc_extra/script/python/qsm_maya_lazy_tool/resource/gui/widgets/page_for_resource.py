# coding:utf-8
import qsm_lazy_tool.resource.gui.abstracts as _abstracts


class PrxPageForResource(_abstracts.AbsPrxPageForResource):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForResource, self).__init__(window, session, *args, **kwargs)
