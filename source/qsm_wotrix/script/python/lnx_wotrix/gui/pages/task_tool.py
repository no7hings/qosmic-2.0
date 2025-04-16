# coding:utf-8
from ... import core as _lzy_wsp_core

from ..abstracts import page_for_task_tool as _abs_page_for_task_tool


class PrxPageForTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = _lzy_wsp_core.TaskParse

    UNIT_CLASSES = [
        # find auto
    ]

    TASK_MODULE_ROOT = 'lnx_wotrix_tasks'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForTaskTool, self).__init__(window, session, *args, **kwargs)
