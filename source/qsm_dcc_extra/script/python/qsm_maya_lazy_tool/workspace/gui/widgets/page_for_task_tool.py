# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_tool as _abs_page_for_task_tool

import qsm_maya.wsp_task as qsm_mya_wsp_task

from . import unit_for_task_tool as _unit_for_task_tool


class PrxPageForAssetTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    UNIT_CLASS_DICT = {
        # cfx rig
        _unit_for_task_tool.PrxToolsetForAssetCfxRigTool.UNIT_KEY:
        _unit_for_task_tool.PrxToolsetForAssetCfxRigTool
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForAssetTaskTool, self).__init__(window, session, *args, **kwargs)


class PrxPageForShotTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    UNIT_CLASS_DICT = {
        # cfx
        _unit_for_task_tool.PrxToolsetForShotCfxTool.UNIT_KEY:
        _unit_for_task_tool.PrxToolsetForShotCfxTool,
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForShotTaskTool, self).__init__(window, session, *args, **kwargs)
