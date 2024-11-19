# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_release as _abs_page_for_task_release

import qsm_maya_wsp_task as qsm_mya_wsp_task

from . import unit_for_asset_cfx_rig_release as _unit_for_asset_cfx_rig_release

from . import unit_for_shot_cfx_dressing_release as _unit_for_shot_cfx_dressing_release


class PrxPageForTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    UNIT_CLASSES = [
        # cfx rig
        _unit_for_asset_cfx_rig_release.PrxToolsetForAssetCfxRigRelease,
        # cfx dressing
        _unit_for_shot_cfx_dressing_release.PrxToolsetForAssetCfxRigRelease,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskRelease, self).__init__(*args, **kwargs)
