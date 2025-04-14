# coding:utf-8
import qsm_general.core as qsm_gnl_core

from ... import core as _lzy_wsp_core

from ..abstracts import page_for_task_overview as _abs_page_for_task_overview

from ..units.task_overview import project as _unit_project

from ..units.task_overview import asset as _unit_asset

from ..units.task_overview import episode as _unit_episode

from ..units.task_overview import sequence as _unit_sequence

from ..units.task_overview import shot as _unit_shot


class PrxPageForTaskOverview(_abs_page_for_task_overview.AbsPrxPageForTaskOverview):
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
        _unit_project.PrxUnitForProjectTaskOverview,
        _unit_asset.PrxUnitForAssetTaskOverview,
        _unit_episode.PrxUnitForEpisodeTaskOverview,
        _unit_sequence.PrxUnitForSequenceTaskOverview,
        _unit_shot.PrxUnitForShotTaskOverview,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskOverview, self).__init__(*args, **kwargs)
