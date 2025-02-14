# coding:utf-8
from qsm_lazy_workspace.gui.abstracts import page_for_task_release as _abs_page_for_task_release

from ... import core as _lzy_wps_core


class PrxPageForTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = _lzy_wps_core.TaskParse

    UNIT_CLASSES = []

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskRelease, self).__init__(*args, **kwargs)
