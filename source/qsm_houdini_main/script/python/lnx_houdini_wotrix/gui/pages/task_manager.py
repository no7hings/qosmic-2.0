# coding:utf-8
import qsm_general.core as qsm_gnl_core

from lnx_wotrix.gui.abstracts import page_for_task_manager as _abs_page_for_task_manager

from ... import core as _lnx_wtx_core

from ..units.task_manager import project as _unit_project_task_manager

from ..units.task_manager import asset as _unit_asset_task_manager

from ..units.task_manager import episode as _unit_episode_task_manager

from ..units.task_manager import sequence as _unit_sequence_task_manager

from ..units.task_manager import shot as _unit_shot_task_manager


class PrxPageForTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = _lnx_wtx_core.TaskParse

    if qsm_gnl_core.scheme_is_release():
        RESOURCE_TYPES = [
            'asset', 'shot'
        ]
    else:
        RESOURCE_TYPES = [
            'project', 'asset', 'episode', 'sequence', 'shot'
        ]

    UNIT_CLASSES = [
        # project
        _unit_project_task_manager.GuiTaskManagerMain,
        # asset
        _unit_asset_task_manager.GuiTaskManagerMain,
        # episode, sequence, shot
        _unit_episode_task_manager.GuiTaskManagerMain,
        _unit_sequence_task_manager.GuiTaskManagerMain,
        _unit_shot_task_manager.GuiTaskManagerMain,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskManager, self).__init__(*args, **kwargs)
