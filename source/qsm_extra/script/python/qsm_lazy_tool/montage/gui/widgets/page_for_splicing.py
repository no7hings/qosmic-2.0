# coding:utf-8
from .. import abstracts as _abstracts

from ....generate.gui import widgets as _gnl_gui_weight


class PrxPageForSplicing(_abstracts.AbsPrxPageForSplicing):
    UNIT_CLASS_DICT = dict(
        scene_space=_gnl_gui_weight.PrxUnitForSceneSpace
    )

    def __init__(self, *args, **kwargs):
        super(PrxPageForSplicing, self).__init__(*args, **kwargs)

    def gui_refresh_stage(self, force=False):
        if force is True:
            self._motion_prx_track_widget.restore()
        self._motion_prx_track_widget.create_test()
