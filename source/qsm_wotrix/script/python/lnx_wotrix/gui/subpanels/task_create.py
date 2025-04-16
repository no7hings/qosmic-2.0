# coding:utf-8
from ..abstracts import subpanel_for_task_create as _subpanel_for_task_create

from lnx_wotrix_tasks.asset.gnl_testing.gui_widgets import task_create as _asset_gnl_testing

from lnx_wotrix_tasks.shot.gnl_testing.gui_widgets import task_create as _shot_gnl_testing


class PrxSubPanelForTaskCreate(_subpanel_for_task_create.AbsPrxSubpanelForTaskCreate):
    SUB_PAGE_CLASSES = [
        _asset_gnl_testing.PrxSubpageForAssetGnlTestingCreate,
        _shot_gnl_testing.PrxSubpageForShotGnlTestingCreate,
    ]

    ASSET_TASKS = [
        'gnl_testing'
    ]
    SHOT_TASKS = [
        'gnl_testing'
    ]

    def __init__(self, *args, **kwargs):
        super(PrxSubPanelForTaskCreate, self).__init__(*args, **kwargs)
