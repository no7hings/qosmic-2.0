# coding:utf-8
from ...asset_base.gui_operates import task_create as _asset_gnl_task_create


class DccAssetGnlTestingCreateOpt(_asset_gnl_task_create.DccAssetTaskCreateOpt):
    STEP = 'gnl'
    TASK = 'gnl_testing'

    def __init__(self, *args, **kwargs):
        super(DccAssetGnlTestingCreateOpt, self).__init__(*args, **kwargs)
