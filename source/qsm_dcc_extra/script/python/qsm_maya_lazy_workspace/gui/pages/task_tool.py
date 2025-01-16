# coding:utf-8
from qsm_lazy_workspace.gui.abstracts import page_for_task_tool as _abs_page_for_task_tool

import qsm_maya_lazy_workspace.core as mya_lzy_wps_core

from ...tasks.asset_cfx_rig.gui_widgets import task_tool as _unit_cfx_rig_tool

from ...tasks.shot_cfx_cloth.gui_widgets import task_tool as _unit_cfx_cloth_tool

from ...tasks.shot_cfx_dressing.gui_widgets import task_tool as _unit_cfx_dressing_tool


class PrxPageFortTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = mya_lzy_wps_core.TaskParse

    UNIT_CLASSES = [
        # cfx rig
        _unit_cfx_rig_tool.PrxToolsetForAssetCfxRigTool,
        # cfx cloth
        _unit_cfx_cloth_tool.PrxToolsetForShotCfxClothTool,
        # cfx dressing
        _unit_cfx_dressing_tool.PrxToolsetForShotCfxDressingTool,
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageFortTaskTool, self).__init__(window, session, *args, **kwargs)
