# coding:utf-8
import qsm_general.core as qsm_gnl_core

from ... import core as _lzy_wsp_core

from ..abstracts import page_for_task_tracker as _abs_page_for_task_tracker

from ..units.task_tracker import project as _unit_project

from ..units.task_tracker import asset as _unit_asset

from ..units.task_tracker import episode as _unit_episode

from ..units.task_tracker import sequence as _unit_sequence

from ..units.task_tracker import shot as _unit_shot


class PrxPageForTaskTracker(_abs_page_for_task_tracker.AbsPrxPageForTaskTracker):
    TASK_PARSE_CLS = _lzy_wsp_core.TaskParse

    if qsm_gnl_core.scheme_is_release():
        RESOURCE_TYPES = [
            TASK_PARSE_CLS.ResourceTypes.Asset, TASK_PARSE_CLS.ResourceTypes.Shot
        ]
    else:
        RESOURCE_TYPES = [
            TASK_PARSE_CLS.ResourceTypes.Project,
            TASK_PARSE_CLS.ResourceTypes.Asset,
            TASK_PARSE_CLS.ResourceTypes.Episode,
            TASK_PARSE_CLS.ResourceTypes.Sequence,
            TASK_PARSE_CLS.ResourceTypes.Shot,
        ]

    UNIT_CLASSES = [
        _unit_project.PrxUnitForProjectTaskTracker,
        _unit_asset.PrxUnitForAssetTaskTracker,
        _unit_episode.PrxUnitForEpisodeTaskTracker,
        _unit_sequence.PrxUnitForSequenceTaskTracker,
        _unit_shot.PrxUnitForShotTaskTracker,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskTracker, self).__init__(*args, **kwargs)
