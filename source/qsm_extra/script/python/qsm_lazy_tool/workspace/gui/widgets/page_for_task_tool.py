# coding:utf-8
import qsm_wsp_task as qsm_dcc_wsp_task

from ..abstracts import page_for_task_tool as _abs_page_for_task_tool

from . import unit_for_task_tool as _unit_for_task_tool


class PrxPageForTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    UNIT_CLASSES = [
        _unit_for_task_tool.PrxUnitForGnlTool
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForTaskTool, self).__init__(window, session, *args, **kwargs)
