# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_release as _abs_page_for_task_release

import qsm_maya_wsp_task as qsm_mya_wsp_task

from ....workspace_task.asset_cfx_rig.gui_units import task_release as _unit_cfx_rig_release

from ....workspace_task.shot_cfx_dressing.gui_units import task_release as _unit_cfx_dressing


class PrxPageForTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    UNIT_CLASSES = [
        # cfx rig
        _unit_cfx_rig_release.PrxToolsetForAssetCfxRigRelease,
        # cfx dressing
        _unit_cfx_dressing.PrxToolsetForAssetCfxRigRelease,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskRelease, self).__init__(*args, **kwargs)
