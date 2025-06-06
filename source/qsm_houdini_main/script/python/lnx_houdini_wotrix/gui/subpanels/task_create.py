# coding:utf-8
import qsm_general.core as qsm_gnl_core

from lnx_wotrix.gui.abstracts import subpanel_for_task_create as _subpanel_for_task_create


class PrxSubpanelForTaskCreate(_subpanel_for_task_create.AbsPrxSubpanelForTaskCreate):
    SUBPAGE_CLASSES = [
    ]

    if qsm_gnl_core.scheme_is_release():
        ASSET_TASKS = [
        ]
    else:
        PROJECT_TASKS = [
            'gnl_testing',
        ]
        ASSET_TASKS = [
            'gnl_testing',
        ]
        EPISODE_TASKS = [
            'gnl_testing',
        ]
        SEQUENCE_TASKS = [
            'gnl_testing',
        ]
        SHOT_TASKS = [
            'gnl_testing',
        ]

    TASK_MODULE_ROOT = 'lnx_houdini_wotrix_tasks'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubpanelForTaskCreate, self).__init__(window, session, *args, **kwargs)
