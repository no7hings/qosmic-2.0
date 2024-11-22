# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import sub_panel_for_task_create as _sub_panel_for_task_create

from ....workspace_task.asset_cfx_rig.gui_units import task_create as _unit_cfx_rig_create

from ....workspace_task.shot_cfx_cloth.gui_units import task_create as _unit_cfx_cloth_create

from ....workspace_task.shot_cfx_dressing.gui_units import task_create as _unit_cfx_dressing_create


class PrxSubPanelForTaskCreate(_sub_panel_for_task_create.AbsPrxSubPanelForTaskCreate):
    SUB_PAGE_CLASSES = [
        # cfx rig
        _unit_cfx_rig_create.PrxSubPageForAssetCfxRigCreate,
        # cfx cloth
        _unit_cfx_cloth_create.PrxSubPageForShotCfxClothCreate,
        # cfx dressing
        _unit_cfx_dressing_create.PrxSubPageForShotCfxDressingCreate
    ]

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForTaskCreate, self).__init__(window, session, *args, **kwargs)
