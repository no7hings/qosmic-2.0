# coding:utf-8
import qsm_general.core as qsm_gnl_core

from lnx_wotrix.gui.abstracts import subpanel_for_task_create as _subpanel_for_task_create


class PrxSubPanelForTaskCreate(_subpanel_for_task_create.AbsPrxSubpanelForTaskCreate):
    SUBPAGE_CLASSES = [
    ]

    if qsm_gnl_core.scheme_is_release():
        pass
    else:
        pass

    TASK_MODULE_ROOT = 'lnx_katana_wotrix_tasks'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForTaskCreate, self).__init__(window, session, *args, **kwargs)
