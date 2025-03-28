# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForResource(_abstracts.AbsPrxPageForResource):
    def __init__(self, *args, **kwargs):
        super(PrxPageForResource, self).__init__(*args, **kwargs)

    def gui_refresh_stage(self):
        pass
