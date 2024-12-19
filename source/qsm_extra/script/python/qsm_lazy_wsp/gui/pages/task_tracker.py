# coding:utf-8
import qsm_general.core as qsm_gnl_core

from ... import core as _lzy_wsp_core

from ..abstracts import page_for_task_tracker as _abs_page_for_task_tracker

from ..units import project_task_tracker as _unit_project_task_tracker

from ..units import asset_task_tracker as _unit_asset_task_tracker

from ..units import sequence_task_tracker as _unit_sequence_task_tracker

from ..units import shot_task_tracker as _unit_shot_task_tracker


class PrxPageForTaskTracker(_abs_page_for_task_tracker.AbsPrxPageForTaskTracker):
    TASK_PARSE_CLS = _lzy_wsp_core.TaskParse

    if qsm_gnl_core.scheme_is_release():
        TASK_BRANCHES = [
            'asset', 'shot'
        ]
    else:
        TASK_BRANCHES = [
            'project', 'asset', 'sequence', 'shot'
        ]

    UNIT_CLASSES = [
        _unit_project_task_tracker.PrxUnitForProjectTaskTracker,
        _unit_asset_task_tracker.PrxUnitForAssetTaskTracker,
        _unit_sequence_task_tracker.PrxUnitForSequenceTaskTracker,
        _unit_shot_task_tracker.PrxUnitForShotTaskTracker,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskTracker, self).__init__(*args, **kwargs)
