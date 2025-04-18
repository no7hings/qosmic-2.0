# coding:utf-8
import qsm_general.core as qsm_gnl_core

from lnx_wotrix.gui.abstracts import subpanel_for_task_create as _subpanel_for_task_create


class PrxSubpanelForTaskCreate(_subpanel_for_task_create.AbsPrxSubpanelForTaskCreate):
    SUBPAGE_CLASSES = [
        # auto load
    ]

    if qsm_gnl_core.scheme_is_release():
        ASSET_TASKS = [
            'cfx_rig',
        ]
        SHOT_TASKS = [
            'animation',
            'cfx_cloth',
            'cfx_dressing',
        ]
    else:
        PROJECT_TASKS = [
            'gnl_testing',
        ]
        ASSET_TASKS = [
            'gnl_testing',
            'rig_testing',

            'cfx_rig',
        ]
        SEQUENCE_TASKS = [
            'gnl_testing',
        ]
        SHOT_TASKS = [
            'gnl_testing',

            'animation',
            'cfx_cloth',
            'cfx_dressing',
        ]

    TASK_MODULE_ROOT = 'lnx_maya_wotrix_tasks'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubpanelForTaskCreate, self).__init__(window, session, *args, **kwargs)
