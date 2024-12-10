# coding:utf-8
import collections
import copy
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ...shot_base.gui_operates import task_tool as _shot_gnl

from ...shot_base import dcc_core as _shot_base_dcc_core

from .. import dcc_core as _task_dcc_core

from .. import dcc_scripts as _task_dcc_scripts


class MayaShotCfxClothToolOpt(_shot_gnl.MayaShotTaskToolOpt):

    def __init__(self, *args, **kwargs):
        super(MayaShotCfxClothToolOpt, self).__init__(*args, **kwargs)

    def load_cfx_rig_for(self, rig_namespace):
        reference_cache = qsm_mya_core.ReferencesCache()
        rig_scene_path = reference_cache.get_file(rig_namespace)

        if not rig_scene_path:
            return

        asset_handle = _task_dcc_core.ShotCfxClothAssetHandle(rig_namespace)

        cfx_rig_namespace = asset_handle.cfx_rig_namespace

        # ignore when reference is exists
        node = reference_cache.get(cfx_rig_namespace)
        if node is None:
            rig_scene_ptn_opt = self._task_session.generate_pattern_opt_for(
                'asset-disorder-rig_scene-maya-file'
            )
            variants = rig_scene_ptn_opt.get_variants(rig_scene_path)
            if variants:
                variants_new = copy.copy(variants)

                variants_new['step'] = 'cfx'
                variants_new['task'] = 'cfx_rig'

                cfx_rig_scene_path = self._task_session.get_latest_file_for(
                    'asset-release-maya-scene-file', **variants_new
                )
                if not rig_scene_path:
                    if not bsc_storage.StgPath.get_is_file(cfx_rig_scene_path):
                        return
                    return

                asset_handle.reference_cfx_rig_from(cfx_rig_scene_path)

                locations = qsm_mya_core.Namespace.find_roots(cfx_rig_namespace)
                for i_location in locations:
                    _task_dcc_core.ShotCfxRigGroupOrg().add_one(i_location)

        asset_handle.connect_to_rig()

    def update_cfx_rig_for(self, rig_namespace):
        asset_handle = _task_dcc_core.ShotCfxClothAssetHandle(rig_namespace)
        if asset_handle.cfx_rig_is_loaded():
            scene_path_old = asset_handle.get_cfx_rig_scene_path()
            variants = self._task_session.generate_file_variants_for(
                'asset-release-maya-scene-file', scene_path_old
            )
            if variants:
                scene_path_new = self._task_session.get_latest_file_for(
                    'asset-release-maya-scene-file', **variants
                )
                if scene_path_old != scene_path_new:
                    asset_handle.replace_cfx_rig_scene(scene_path_new)

        asset_handle.connect_to_rig()

    @classmethod
    def load_cfx_rig_scene_auto(cls, rig_namespace, cfx_rig_scene_path):
        asset_handle = _task_dcc_core.ShotCfxClothAssetHandle(rig_namespace)
        if asset_handle.cfx_rig_is_loaded():
            asset_handle.replace_cfx_rig_scene(cfx_rig_scene_path)
        else:
            cfx_rig_namespace = asset_handle.cfx_rig_namespace
            asset_handle.reference_cfx_rig_from(cfx_rig_scene_path)

            locations = qsm_mya_core.Namespace.find_roots(cfx_rig_namespace)
            for i_location in locations:
                _task_dcc_core.ShotCfxRigGroupOrg().add_one(i_location)

        asset_handle.connect_to_rig()

    def get_cfx_rig_all_version_dict(self, rig_namespace):
        reference_cache = qsm_mya_core.ReferencesCache()

        rig_scene_path = reference_cache.get_file(rig_namespace)

        if not rig_scene_path:
            return {}

        rig_scene_ptn_opt = self._task_session.generate_pattern_opt_for(
            'asset-disorder-rig_scene-maya-file'
        )
        variants = rig_scene_ptn_opt.get_variants(rig_scene_path)
        if variants:
            variants_new = copy.copy(variants)

            variants_new['step'] = 'cfx'
            variants_new['task'] = 'cfx_rig'

            cfx_rig_scene_ptn_opt = self._task_session.generate_pattern_opt_for(
                'asset-release-maya-scene-file', **variants_new
            )
            dict_ = collections.OrderedDict()
            matches = cfx_rig_scene_ptn_opt.find_matches(sort=True)
            matches = matches[-10:]
            for i in matches:
                dict_['v{}'.format(i['version'])] = i['result']
            return dict_
        return {}

    @classmethod
    def export_cloth_cache_by_rig_namespace(
        cls, rig_namespace, directory_path, frame_range, frame_step=1, frame_offset=0
    ):
        asset_handle = _task_dcc_core.ShotCfxClothAssetHandle(rig_namespace)
        cfx_rig_namespace = asset_handle.cfx_rig_namespace
        resource = _task_dcc_core.CfxRigAsset(cfx_rig_namespace)

        _task_dcc_scripts.ShotCfxClothCacheOpt(resource).do_export(
            directory_path, frame_range, frame_step, frame_offset
        )

    @classmethod
    def load_cfx_rig_auto(cls):
        _task_dcc_scripts.ShotCfxRigsOpt().load_all()
        
    @classmethod
    def apply_animation_start_frame(cls, frame):
        _shot_base_dcc_core.ShotAssetsAnimationGroupOrg().set_start_frame(frame)

    @classmethod
    def apply_animation_frame_range(cls, statr_frame, end_frame):
        _shot_base_dcc_core.ShotAssetsAnimationGroupOrg().set_frame_range(statr_frame, end_frame)
    
    @classmethod
    def get_animation_start_frame(cls):
        return _shot_base_dcc_core.ShotAssetsAnimationGroupOrg().get_start_frame()

    @classmethod
    def apply_simulation_start_frame(cls, frame):
        # apply to cfx group
        _shot_base_dcc_core.ShotAssetsCfxGroupOrg().set_start_frame(frame)
        # apply to cfx rig
        _task_dcc_scripts.ShotCfxRigsOpt().apply_all_solver_start_frame(frame)

        qsm_mya_core.Frame.set_start_frame(frame)
        qsm_mya_core.Frame.set_current(frame)

    @classmethod
    def get_simulation_start_frame(cls):
        return _shot_base_dcc_core.ShotAssetsCfxGroupOrg().get_start_frame()
