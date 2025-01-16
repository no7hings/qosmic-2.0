# coding:utf-8
import qsm_general.core as qsm_gnl_core

from qsm_lazy_workspace.gui.abstracts import subpanel_for_task_create as _subpanel_for_task_create

# project
from ...tasks.project_gnl_testing.gui_widgets import task_create as _unit_project_gnl_testing_create

# asset
from ...tasks.asset_gnl_testing.gui_widgets import task_create as _unit_asset_gnl_testing_create

from ...tasks.asset_rig_testing.gui_widgets import task_create as _unit_asset_rig_testing_create

from ...tasks.asset_cfx_rig.gui_widgets import task_create as _unit_asset_cfx_rig_create

# sequence
from ...tasks.sequence_gnl_testing.gui_widgets import task_create as _unit_sequence_cfx_rig_create

# shot
from ...tasks.shot_gnl_testing.gui_widgets import task_create as _unit_shot_gnl_testing_create

from ...tasks.shot_animation.gui_widgets import task_create as _unit_shot_animation_create

from ...tasks.shot_cfx_cloth.gui_widgets import task_create as _unit_shot_cfx_cloth_create

from ...tasks.shot_cfx_dressing.gui_widgets import task_create as _unit_shot_cfx_dressing_create


class PrxSubPanelForTaskCreate(_subpanel_for_task_create.AbsPrxSubpanelForTaskCreate):
    SUB_PAGE_CLASSES = [
        # project
        # gnl_testing
        _unit_project_gnl_testing_create.PrxSubpageForProjectGnlTestingCreate,

        # asset
        #   gnl_testing
        _unit_asset_gnl_testing_create.PrxSubpageForAssetGnlTestingCreate,
        #   rig_testing
        _unit_asset_rig_testing_create.PrxSubpageForAssetRigTestingCreate,
        #   cfx_rig
        _unit_asset_cfx_rig_create.PrxSubpageForAssetCfxRigCreate,

        # sequence
        _unit_sequence_cfx_rig_create.PrxSubpageForSequenceGnlTestingCreate,

        # shot
        _unit_shot_gnl_testing_create.PrxSubpageForShotGnlTestingCreate,
        #   animation
        _unit_shot_animation_create.PrxSubpageForShotAnimationCreate,
        #   cfx_cloth
        _unit_shot_cfx_cloth_create.PrxSubpageForShotCfxClothCreate,
        #   cfx_dressing
        _unit_shot_cfx_dressing_create.PrxSubpageForShotCfxDressingCreate
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

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForTaskCreate, self).__init__(window, session, *args, **kwargs)
