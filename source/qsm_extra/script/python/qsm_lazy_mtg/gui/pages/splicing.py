# coding:utf-8
from .. import abstracts as _abstracts


class PrxPageForSplicing(_abstracts.AbsPrxPageForSplicing):

    def __init__(self, *args, **kwargs):
        super(PrxPageForSplicing, self).__init__(*args, **kwargs)

    def gui_refresh_fnc(self, force=False):
        if force is True:
            self._motion_prx_track_widget.restore()

        self._motion_prx_track_widget.create_test()
