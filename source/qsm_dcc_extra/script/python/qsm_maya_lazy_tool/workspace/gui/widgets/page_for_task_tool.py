# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_tool as _abs_page_for_task_tool

import qsm_maya_wsp_task as qsm_mya_wsp_task

from . import unit_for_asset_cfx_rig_tool as _unit_for_asset_cfx_rig_tool

from . import unit_for_shot_cfx_cloth_tool as _unit_for_shot_cfx_cloth_tool


class PrxPageForAssetTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    UNIT_CLASS_DICT = {
        # cfx rig
        _unit_for_asset_cfx_rig_tool.PrxToolsetForAssetCfxRigTool.GUI_KEY:
        _unit_for_asset_cfx_rig_tool.PrxToolsetForAssetCfxRigTool
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForAssetTaskTool, self).__init__(window, session, *args, **kwargs)


class PrxPageForShotTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    UNIT_CLASS_DICT = {
        # cfx
        _unit_for_shot_cfx_cloth_tool.PrxToolsetForShotCfxClothTool.GUI_KEY:
        _unit_for_shot_cfx_cloth_tool.PrxToolsetForShotCfxClothTool,
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForShotTaskTool, self).__init__(window, session, *args, **kwargs)
