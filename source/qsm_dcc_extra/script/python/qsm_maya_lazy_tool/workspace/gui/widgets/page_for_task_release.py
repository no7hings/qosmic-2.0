# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_release as _abs_page_for_task_release

import qsm_maya_wsp_task as qsm_mya_wsp_task

from . import unit_for_task_release as _unit_for_task_release


class PrxPageForAssetTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    UNIT_CLASS_DICT = {
        # general
        _unit_for_task_release.PrxToolsetForCfxRigRelease.GUI_KEY:
        _unit_for_task_release.PrxToolsetForCfxRigRelease
    }

    def __init__(self, *args, **kwargs):
        super(PrxPageForAssetTaskRelease, self).__init__(*args, **kwargs)
