# coding:utf-8
from ... import core as _lzy_wsp_core

from ..abstracts import page_for_task_overview as _abs_page_for_task_overview


class PrxPageForTaskOverview(_abs_page_for_task_overview.AbsPrxPageForTaskOverview):
    TASK_PARSE_CLS = _lzy_wsp_core.TaskParse

    UNIT_CLASSES = [
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskOverview, self).__init__(*args, **kwargs)
