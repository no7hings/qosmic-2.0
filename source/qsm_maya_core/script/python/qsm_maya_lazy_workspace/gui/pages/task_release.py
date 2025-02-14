# coding:utf-8
from qsm_lazy_workspace.gui.abstracts import page_for_task_release as _abs_page_for_task_release

from ... import core as _lzy_wps_core

from ...tasks.asset_cfx_rig.gui_widgets import task_release as _unit_cfx_rig_release

from ...tasks.shot_cfx_dressing.gui_widgets import task_release as _unit_cfx_dressing


class PrxPageForTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = _lzy_wps_core.TaskParse

    UNIT_CLASSES = [
        # cfx rig
        _unit_cfx_rig_release.PrxToolsetForAssetCfxRigRelease,
        # cfx dressing
        _unit_cfx_dressing.PrxToolsetForAssetCfxRigRelease,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskRelease, self).__init__(*args, **kwargs)
