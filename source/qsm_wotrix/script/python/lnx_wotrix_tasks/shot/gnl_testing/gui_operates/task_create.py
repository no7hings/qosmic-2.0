# coding:utf-8
from ...base.gui_operates import task_create as _shot_gnl_task_create


class DccShotGnlTestingCreateOpt(_shot_gnl_task_create.DccShotTaskCreateOpt):
    STEP = 'gnl'
    TASK = 'gnl_testing'

    def __init__(self, *args, **kwargs):
        super(DccShotGnlTestingCreateOpt, self).__init__(*args, **kwargs)
