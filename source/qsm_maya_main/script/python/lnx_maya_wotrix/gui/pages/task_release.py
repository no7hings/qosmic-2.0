# coding:utf-8
from lnx_wotrix.gui.abstracts import page_for_task_release as _abs_page_for_task_release

from ... import core as _lnx_wtx_core

from lnx_maya_wotrix_tasks.asset.cfx_rig.gui_widgets import task_release as _asset_cfx_rig

from lnx_maya_wotrix_tasks.shot.cfx_dressing.gui_widgets import task_release as _shot_cfx_dressing


class PrxPageForTaskRelease(_abs_page_for_task_release.AbsPrxPageForTaskRelease):
    TASK_PARSE_CLS = _lnx_wtx_core.TaskParse

    UNIT_CLASSES = [
        # find auto
    ]

    TASK_MODULE_ROOT = 'lnx_maya_wotrix_tasks'

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskRelease, self).__init__(*args, **kwargs)
