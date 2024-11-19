# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_tool as _abs_page_for_task_tool

import qsm_maya_wsp_task as qsm_mya_wsp_task

from . import unit_for_asset_cfx_rig_tool as _unit_for_asset_cfx_rig_tool

from . import unit_for_shot_cfx_cloth_tool as _unit_for_shot_cfx_cloth_tool

from . import unit_for_shot_cfx_dressing_tool as _unit_for_shot_cfx_dressing_tool


class PrxPageFortTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    UNIT_CLASSES = [
        # cfx rig
        _unit_for_asset_cfx_rig_tool.PrxToolsetForAssetCfxRigTool,
        # cfx cloth
        _unit_for_shot_cfx_cloth_tool.PrxToolsetForShotCfxClothTool,
        # cfx dressing
        _unit_for_shot_cfx_dressing_tool.PrxToolsetForShotCfxDressingTool,
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageFortTaskTool, self).__init__(window, session, *args, **kwargs)
