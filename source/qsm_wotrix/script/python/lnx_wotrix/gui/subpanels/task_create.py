# coding:utf-8
from ..abstracts import subpanel_for_task_create as _subpanel_for_task_create


class PrxSubPanelForTaskCreate(_subpanel_for_task_create.AbsPrxSubpanelForTaskCreate):
    SUBPAGE_CLASSES = [
        # do not add cls here, find cls auto now.
    ]

    ASSET_TASKS = [
        'gnl_testing'
    ]
    SHOT_TASKS = [
        'gnl_testing'
    ]

    TASK_MODULE_ROOT = 'lnx_wotrix_tasks'

    def __init__(self, *args, **kwargs):
        super(PrxSubPanelForTaskCreate, self).__init__(*args, **kwargs)
