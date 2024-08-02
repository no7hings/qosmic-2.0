# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForComposition(_abstracts.AbsPrxPageForComposition):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForComposition, self).__init__(window, session, *args, **kwargs)

    def gui_build_stage(self):
        self._motion_prx_track_view.create_test()
