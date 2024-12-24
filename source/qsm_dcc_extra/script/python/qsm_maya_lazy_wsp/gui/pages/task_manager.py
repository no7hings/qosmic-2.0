# coding:utf-8
import qsm_general.core as qsm_gnl_core

import qsm_maya_lazy_wsp.core as mya_lzy_wps_core

from qsm_lazy_wsp.gui.abstracts import page_for_task_manager as _abs_page_for_task_manager

from ..units import project_task_manager as _unit_project_task_manager

from ..units import asset_task_manager as _unit_asset_task_manager

from ..units import sequence_task_manager as _unit_sequence_task_manager

from ..units import shot_task_manager as _unit_shot_task_manager


class PrxPageForTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = mya_lzy_wps_core.TaskParse

    if qsm_gnl_core.scheme_is_release():
        RESOURCE_TYPES = [
            'asset', 'shot'
        ]
    else:
        RESOURCE_TYPES = [
            'project', 'asset', 'sequence', 'shot'
        ]

    UNIT_CLASSES = [
        _unit_project_task_manager.PrxUnitForProjectTaskManager,
        _unit_asset_task_manager.PrxUnitForAssetTaskManager,
        _unit_sequence_task_manager.PrxUnitForSequenceTaskManager,
        _unit_shot_task_manager.PrxUnitForShotTaskManager,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskManager, self).__init__(*args, **kwargs)
