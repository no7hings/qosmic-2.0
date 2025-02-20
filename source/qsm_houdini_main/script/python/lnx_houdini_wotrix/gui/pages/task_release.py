# coding:utf-8
from lnx_wotrix.gui.abstracts import page_for_task_release as _abs_page_for_task_release

from ... import core as _lnx_wtx_core


class PrxPageForTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = _lnx_wtx_core.TaskParse

    UNIT_CLASSES = [
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskRelease, self).__init__(*args, **kwargs)
