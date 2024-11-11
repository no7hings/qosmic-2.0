# coding:utf-8
import qsm_general.wsp_task as qsm_dcc_wsp_task

from ..abstracts import page_for_task_tool as _abs_page_for_task_tool

from . import unit_for_task_tool as _unit_for_task_tool


class PrxPageForAssetTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    UNIT_CLASS_DICT = {
        # general
        _unit_for_task_tool.PrxToolsetForGnlTool.UNIT_KEY:
        _unit_for_task_tool.PrxToolsetForGnlTool,
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForAssetTaskTool, self).__init__(window, session, *args, **kwargs)


class PrxPageForShotTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    UNIT_CLASS_DICT = {
        # general
        _unit_for_task_tool.PrxToolsetForGnlTool.UNIT_KEY:
        _unit_for_task_tool.PrxToolsetForGnlTool,
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForShotTaskTool, self).__init__(window, session, *args, **kwargs)
