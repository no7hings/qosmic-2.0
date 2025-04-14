# coding:utf-8
import qsm_general.core as qsm_gnl_core

from ... import core as _lzy_wsp_core

from ..abstracts import page_for_task_manager as _abs_page_for_task_manager

from ..units.task_manager import project as _unit_project

from ..units.task_manager import asset as _unit_asset

from ..units.task_manager import episode as _unit_episode

from ..units.task_manager import sequence as _unit_sequence

from ..units.task_manager import shot as _unit_shot


class PrxPageForTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = _lzy_wsp_core.TaskParse

    if qsm_gnl_core.scheme_is_release():
        RESOURCE_TYPES = [
            TASK_PARSE_CLS.ResourceTypes.Asset,
            TASK_PARSE_CLS.ResourceTypes.Shot
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
        _unit_project.PrxUnitForProjectTaskManager,
        _unit_asset.PrxUnitForAssetTaskManager,
        _unit_episode.PrxUnitForEpisodeTaskManager,
        _unit_sequence.PrxUnitForSequenceTaskManager,
        _unit_shot.PrxUnitForShotTaskManager,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskManager, self).__init__(*args, **kwargs)
