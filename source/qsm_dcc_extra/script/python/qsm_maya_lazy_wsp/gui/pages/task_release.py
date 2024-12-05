# coding:utf-8
from qsm_lazy_wsp.gui.abstracts import page_for_task_release as _abs_page_for_task_release

import qsm_maya_lazy_wsp.core as mya_lzy_wps_core

from ...tasks.asset_cfx_rig.gui_widgets import task_release as _unit_cfx_rig_release

from ...tasks.shot_cfx_dressing.gui_widgets import task_release as _unit_cfx_dressing


class PrxPageForTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = mya_lzy_wps_core.TaskParse

    UNIT_CLASSES = [
        # cfx rig
        _unit_cfx_rig_release.PrxToolsetForAssetCfxRigRelease,
        # cfx dressing
        _unit_cfx_dressing.PrxToolsetForAssetCfxRigRelease,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskRelease, self).__init__(*args, **kwargs)
