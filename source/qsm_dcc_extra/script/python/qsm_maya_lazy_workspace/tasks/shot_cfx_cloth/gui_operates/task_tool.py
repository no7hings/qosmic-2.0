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

    def load_cfx_rig_auto(self, rig_namespace, force=False):
        reference_cache = qsm_mya_core.ReferencesCache()
        rig_scene_path = reference_cache.get_file(rig_namespace)

        if not rig_scene_path:
            return

        asset_handle = _task_dcc_core.ShotCfxClothAssetHandle(rig_namespace)

        # ignore when reference is exists
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

            asset_handle.cfx_rig_handle.load_scene_auto(cfx_rig_scene_path, force=force)

    # cfx rig
    def update_cfx_rig_for(self, rig_namespace):
        asset_handle = _task_dcc_core.ShotCfxClothAssetHandle(rig_namespace)
        cfx_rig_handle = asset_handle.cfx_rig_handle
        if cfx_rig_handle.get_is_loaded():
            keyword = 'asset-release-maya-scene-file'
            scene_path_old = cfx_rig_handle.get_scene_path()
            variants = self._task_session.generate_file_variants_for(
                keyword, scene_path_old
            )
            if variants:
                scene_path_new = self._task_session.get_latest_file_for(
                    keyword, **variants
                )
                if scene_path_old != scene_path_new:
                    cfx_rig_handle.replace_scene(scene_path_new)

        cfx_rig_handle.connect_to_rig()

    @classmethod
    def load_cfx_rig_scene_auto(cls, rig_namespace, scene_path):
        asset_handle = _task_dcc_core.ShotCfxClothAssetHandle(rig_namespace)
        cfx_rig_handle = asset_handle.cfx_rig_handle
        cfx_rig_handle.load_scene_auto(scene_path)

    def get_cfx_rig_file_variants_by_rig_namespace(self, rig_namespace):
        reference_cache = qsm_mya_core.ReferencesCache()
        rig_scene_path = reference_cache.get_file(rig_namespace)

        if not rig_scene_path:
            return {}

        task_session = self._task_session
        task_parse = task_session.task_parse

        rig_scene_ptn_opt = task_parse.generate_pattern_opt_for(
            'asset-disorder-rig_scene-maya-file'
        )

        file_variants = rig_scene_ptn_opt.get_variants(rig_scene_path)
        if file_variants:
            file_variants_new = copy.copy(file_variants)
            file_variants_new['step'] = task_parse.Steps.cfx
            file_variants_new['task'] = task_parse.Tasks.cfx_rig
            return file_variants_new

    def get_cfx_rig_variants(self, file_variants):
        if file_variants:
            rig_variants = ['default']
            task_session = self._task_session
            ptn_opt = task_session.generate_pattern_opt_for(
                'asset-release-maya-scene-var-file', **file_variants
            )
            matches = ptn_opt.find_matches()
            for i in matches:
                i_rig_variant = i['var']
                if i_rig_variant not in rig_variants:
                    rig_variants.append(i_rig_variant)
            return rig_variants
        return []

    def generate_cfx_rig_version_dict(self, rig_namespace):
        file_variants = self.get_cfx_rig_file_variants_by_rig_namespace(rig_namespace)
        if file_variants:
            cfx_rig_variants = self.get_cfx_rig_variants(file_variants)

            dict_ = collections.OrderedDict()
            for i_rig_variant in cfx_rig_variants:
                i_dict = self.generate_cfx_rig_version_dict_for(file_variants, i_rig_variant)
                dict_[i_rig_variant] = i_dict

            return dict_
        return {}

    def generate_cfx_rig_version_dict_for(self, file_variants, rig_variant):
        task_session = self._task_session
        task_parse = task_session.task_parse

        if rig_variant == 'default':
            cfx_rig_scene_ptn_opt = task_parse.generate_pattern_opt_for(
                'asset-release-maya-scene-file', **file_variants
            )
        else:
            cfx_rig_scene_ptn_opt = task_parse.generate_pattern_opt_for(
                'asset-release-maya-scene-var-file', **file_variants
            )

        dict_ = collections.OrderedDict()
        matches = cfx_rig_scene_ptn_opt.find_matches(sort=True)
        matches = matches[-10:]
        for i in matches:
            dict_['v{}'.format(i['version'])] = i['result']
        return dict_

    def generate_ani_geo_cache_version_dict(self, rig_namespace):
        task_session = self._task_session
        task_parse = task_session.task_parse

        variants_new = copy.copy(task_session.properties)
        variants_new['step'] = task_parse.Steps.animation
        variants_new['task'] = task_parse.Tasks.animation
        variants_new['namespace'] = rig_namespace.replace(':', '__')
        variants_new.pop('version')

        # use scene-src for cacheing
        asset_cache_abc_pth_opt = task_parse.generate_pattern_opt_for(
            'shot-temporary-asset-cache-abc-geometry-file', **variants_new
        )
        dict_ = collections.OrderedDict()
        matches = asset_cache_abc_pth_opt.find_matches(sort=True)
        matches = matches[-10:]
        for i in matches:
            dict_['v{}'.format(i['version'])] = i['result']
        return dict_

    @classmethod
    def load_ani_geo_cache_auto(cls, rig_namespace, cache_path):
        asset_handle = _task_dcc_core.ShotCfxClothAssetHandle(rig_namespace)
        ani_geo_cache_handle = asset_handle.ani_geo_cache_handle
        ani_geo_cache_handle.load_cache_auto(cache_path)

    @classmethod
    def load_ani_ctl_cache_auto(cls, rig_namespace, cache_path):
        asset_handle = _task_dcc_core.ShotCfxClothAssetHandle(rig_namespace)
        ani_ctl_cache_handle = asset_handle.ani_ctl_cache_handle
        ani_ctl_cache_handle.load_cache_auto(cache_path)

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
    def load_all_cfx_rig(cls):
        _task_dcc_scripts.ShotCfxRigsOpt().load_all()
        
    @classmethod
    def apply_animation_start_frame(cls, frame):
        _shot_base_dcc_core.ShotAssetsAnimationGroupOrg().set_start_frame(frame)

    @classmethod
    def apply_animation_scene_src(cls, scene_path):
        _shot_base_dcc_core.ShotAssetsAnimationGroupOrg().set_scene_src(scene_path)

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

    @classmethod
    def test(cls):
        import qsm_maya_lazy_workspace.core as c

        task_parse = c.TaskParse()
        task_session = task_parse.generate_task_session_by_resource_source_scene_src_auto()
        task_tool_opt = task_session.generate_opt_for(cls)

        task_tool_opt.generate_animation_cache_export_args()

    def generate_animation_cache_export_args(self):
        pass
