# coding:utf-8
from lnx_wotrix.gui.abstracts import page_for_task_tool as _abs_page_for_task_tool

from ... import core as _lnx_wtx_core


class PrxPageFortTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = _lnx_wtx_core.TaskParse

    UNIT_CLASSES = [
        # find auto
    ]

    TASK_MODULE_ROOT = 'lnx_maya_wotrix_tasks'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageFortTaskTool, self).__init__(window, session, *args, **kwargs)
