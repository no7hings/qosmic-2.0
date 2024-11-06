# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_release as _abs_page_for_task_release

import qsm_maya.wsp_task as qsm_mya_task

from . import unit_for_task_release as _unit_for_task_release


class PrxPageForTaskPublish(_abs_page_for_task_release.AbsPrxPageForTaskPublish):
    TASK_PARSE_CLS = qsm_mya_task.TaskParse

    UNIT_CLASS_DICT = {
        # general
        _unit_for_task_release.PrxToolsetForCfxRigRelease.UNIT_KEY:
        _unit_for_task_release.PrxToolsetForCfxRigRelease
    }

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskPublish, self).__init__(*args, **kwargs)
