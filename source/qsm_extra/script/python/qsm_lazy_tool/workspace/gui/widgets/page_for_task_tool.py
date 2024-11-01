# coding:utf-8
from ..abstracts import page_for_task_tool as _abs_page_for_task_tool

import qsm_lazy.workspace.core as qsm_lzy_wsp_core

from . import unit_for_task_tool as _unit_for_task_tool


class PrxPageForTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_lzy_wsp_core.TaskParse

    UNIT_CLASS_DICT = {
        # general
        _unit_for_task_tool.PrxToolsetForGeneral.UNIT_KEY:
        _unit_for_task_tool.PrxToolsetForGeneral,
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForTaskTool, self).__init__(window, session, *args, **kwargs)
