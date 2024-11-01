# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_tool as _abs_page_for_task_tool

import qsm_maya_lazy.workspace.core as qsm_mya_lzy_wsp_core

from . import unit_for_task_tool as _unit_for_task_tool


class PrxPageForTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_mya_lzy_wsp_core.TaskParse

    UNIT_CLASS_DICT = {
        _unit_for_task_tool.PrxToolsetForCfxFig.UNIT_KEY:
        _unit_for_task_tool.PrxToolsetForCfxFig
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForTaskTool, self).__init__(window, session, *args, **kwargs)
