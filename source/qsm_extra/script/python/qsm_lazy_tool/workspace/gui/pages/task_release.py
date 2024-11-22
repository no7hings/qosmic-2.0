# coding:utf-8
import qsm_wsp_task as qsm_dcc_wsp_task

from ..abstracts import page_for_task_release as _abs_page_for_task_release

from ....workspace_task.asset_gnl.gui_units import task_rlease as _unit_gnl_release


class PrxPageForTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    UNIT_CLASSES = [
        _unit_gnl_release.PrxToolsetForGnlRelease
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskRelease, self).__init__(*args, **kwargs)
