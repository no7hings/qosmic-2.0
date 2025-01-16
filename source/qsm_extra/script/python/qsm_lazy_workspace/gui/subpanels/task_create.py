# coding:utf-8
from ..abstracts import subpanel_for_task_create as _subpanel_for_task_create

from ...tasks.asset_gnl_testing.gui_widgets import task_create as _unit_asset_gnl_testing_create

from ...tasks.shot_gnl_testing.gui_widgets import task_create as _unit_shot_gnl_testing_create


class PrxSubPanelForTaskCreate(_subpanel_for_task_create.AbsPrxSubpanelForTaskCreate):
    SUB_PAGE_CLASSES = [
        _unit_asset_gnl_testing_create.PrxSubpageForAssetGnlTestingCreate,
        _unit_shot_gnl_testing_create.PrxSubpageForShotGnlTestingCreate,
    ]

    ASSET_TASKS = [
        'gnl_testing'
    ]
    SHOT_TASKS = [
        'gnl_testing'
    ]

    def __init__(self, *args, **kwargs):
        super(PrxSubPanelForTaskCreate, self).__init__(*args, **kwargs)
