# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_tool as _abs_page_for_task_tool

import qsm_maya.wsp_task as qsm_mya_task

from . import unit_for_task_tool as _unit_for_task_tool


class PrxPageForTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_mya_task.TaskParse

    UNIT_CLASS_DICT = {
        _unit_for_task_tool.PrxToolsetForCfxRigTool.UNIT_KEY:
        _unit_for_task_tool.PrxToolsetForCfxRigTool
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForTaskTool, self).__init__(window, session, *args, **kwargs)
