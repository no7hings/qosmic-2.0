# coding:utf-8
import qsm_general.core as qsm_gnl_core

from qsm_lazy_workspace.gui.abstracts import subpanel_for_task_create as _subpanel_for_task_create


class PrxSubPanelForTaskCreate(_subpanel_for_task_create.AbsPrxSubpanelForTaskCreate):
    SUB_PAGE_CLASSES = [
    ]

    if qsm_gnl_core.scheme_is_release():
        pass
    else:
        pass

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForTaskCreate, self).__init__(window, session, *args, **kwargs)
