# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ...base.gui_operates import task_create as _shot_gnl_task_create


class MayaShotCfxDressingCreateOpt(_shot_gnl_task_create.MayaShotTaskCreateOpt):
    STEP = 'cfx'
    TASK = 'cfx_dressing'

    def __init__(self, *args, **kwargs):
        super(MayaShotCfxDressingCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(self, scene_src_path, upstream_scene_path=None, defer_load_reference_nodes=None):
        if upstream_scene_path:
            if bsc_storage.StgPath.get_is_file(upstream_scene_path):
                # load source
                load_kwargs = {}
                if isinstance(defer_load_reference_nodes, list):
                    load_kwargs['load_no_references'] = True

                qsm_mya_core.SceneFile.open(upstream_scene_path, **load_kwargs)

                if defer_load_reference_nodes:
                    for i_reference_node in defer_load_reference_nodes:
                        qsm_mya_core.Reference.load(i_reference_node, **load_kwargs)

        qsm_mya_core.SceneFile.save_to(scene_src_path)
