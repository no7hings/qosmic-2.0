# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForSplicing(_abstracts.AbsPrxPageForSplicing):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForSplicing, self).__init__(window, session, *args, **kwargs)

    def gui_refresh_stage(self, force=False):
        if force is True:
            self._motion_prx_track_view.restore()
        self._motion_prx_track_view.create_test()
