# coding:utf-8
from ... import core as _lzy_wsp_core

from ..abstracts import page_for_task_release as _abs_page_for_task_release


class PrxPageForTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = _lzy_wsp_core.TaskParse

    UNIT_CLASSES = [
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskRelease, self).__init__(*args, **kwargs)
