# coding:utf-8
from qsm_lazy_workspace.gui.abstracts import page_for_task_tool as _abs_page_for_task_tool

from ... import core as _lzy_wps_core


class PrxPageFortTaskTool(_abs_page_for_task_tool.AbsPrxPageForTaskTool):
    TASK_PARSE_CLS = _lzy_wps_core.TaskParse

    UNIT_CLASSES = [
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageFortTaskTool, self).__init__(window, session, *args, **kwargs)
