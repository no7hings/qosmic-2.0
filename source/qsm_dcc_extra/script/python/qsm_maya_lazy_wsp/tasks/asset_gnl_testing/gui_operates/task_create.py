# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ...asset_base.gui_operates import task_create as _asset_gnl_task_create


class MayaAssetGnlTestingCreateOpt(_asset_gnl_task_create.MayaAssetTaskCreateOpt):
    STEP = 'gnl'
    TASK = 'gnl_testing'

    def __init__(self, *args, **kwargs):
        super(MayaAssetGnlTestingCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src(self, scene_src_path):
        qsm_mya_core.SceneFile.save_to(scene_src_path)