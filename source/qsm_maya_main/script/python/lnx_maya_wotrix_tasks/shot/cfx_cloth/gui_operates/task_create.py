# coding:utf-8
import sys

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ...base.gui_operates import task_create as _shot_gnl_task_create

from . import task_tool as _task_tool

from ..dcc_core import dcc_organize as _dcc_cor_organize


class MayaShotCfxClothCreateOpt(_shot_gnl_task_create.MayaShotTaskCreateOpt):
    STEP = 'cfx'
    TASK = 'cfx_cloth'

    def __init__(self, *args, **kwargs):
        super(MayaShotCfxClothCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(
        self,
        scene_src_path, upstream_scene_path=None,
        auto_load_cfx_rig=False, solver_start_frame=1,
        defer_load_reference_nodes=None,
        scene_frame_range=None,
        ignore_load_scenery=False,
        auto_hide_no_use_group=False,
        auto_hide_vfx_group=False,
    ):
        if upstream_scene_path:
            if bsc_storage.StgPath.get_is_file(upstream_scene_path):
                # load source
                load_kwargs = {}
                if isinstance(defer_load_reference_nodes, list):
                    load_kwargs['load_no_references'] = True

                qsm_mya_core.SceneFile.open(upstream_scene_path, **load_kwargs)

                if defer_load_reference_nodes:
                    for i_reference_node in defer_load_reference_nodes:
                        # ignore scenery
                        if ignore_load_scenery is True:
                            i_file_path = qsm_mya_core.Reference.get_file(i_reference_node)
                            if self._task_session.is_file_match(
                                'asset-disorder-model_scene-maya-file', i_file_path
                            ):
                                sys.stderr.write(u'auto ignore scenery file: {}\n'.format(i_file_path))
                                continue

                        qsm_mya_core.Reference.load(i_reference_node, **load_kwargs)

        # create groups
        task = self._properties['task']
        self.create_groups_for(task)

        task_tool_opt = self._task_session.generate_opt_for(_task_tool.MayaShotCfxClothToolOpt)

        task_tool_opt.apply_animation_scene_src(upstream_scene_path)

        if scene_frame_range is not None:
            task_tool_opt.apply_animation_frame_range(*scene_frame_range)

        if auto_load_cfx_rig is True:
            task_tool_opt.load_all_cfx_rig()
            task_tool_opt.apply_simulation_start_frame(solver_start_frame)

        # temp method
        if auto_hide_no_use_group is True:
            if qsm_mya_core.Node.is_exists('NoUse'):
                _dcc_cor_organize.ShotCfxAutoHideLayerOrg().add_one('NoUse')

        if auto_hide_vfx_group is True:
            if qsm_mya_core.Node.is_exists('VFX_Auto'):
                _dcc_cor_organize.ShotCfxAutoHideLayerOrg().add_one('VFX_Auto')

        qsm_mya_core.SceneFile.save_to(scene_src_path)

