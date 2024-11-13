# coding:utf-8
import qsm_wsp_task as qsm_dcc_wsp_task

from ..abstracts import page_for_task_release as _abs_page_for_task_release

from . import unit_for_task_release as _unit_for_task_release


class PrxPageForAssetTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    UNIT_CLASS_DICT = {
        # general
        _unit_for_task_release.PrxToolsetForGnlRelease.GUI_KEY:
        _unit_for_task_release.PrxToolsetForGnlRelease
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForAssetTaskRelease, self).__init__(window, session, *args, **kwargs)


class PrxPageForShotTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    UNIT_CLASS_DICT = {
        # general
        _unit_for_task_release.PrxToolsetForGnlRelease.GUI_KEY:
        _unit_for_task_release.PrxToolsetForGnlRelease
    }

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForShotTaskRelease, self).__init__(window, session, *args, **kwargs)