# coding:utf-8
import qsm_maya.core as qsm_mya_core

from ...sequence_base.gui_operates import task_create as _asset_gnl_task_create


class MayaSequenceGnlTestingCreateOpt(_asset_gnl_task_create.MayaSequenceTaskCreateOpt):
    STEP = 'gnl'
    TASK = 'gnl_testing'

    def __init__(self, *args, **kwargs):
        super(MayaSequenceGnlTestingCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(self, scene_src_path):
        qsm_mya_core.SceneFile.save_to(scene_src_path)
