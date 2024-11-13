# coding:utf-8
import copy

import lxbasic.storage as bsc_storage

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

import qsm_maya.tasks.cfx_cloth.core as qsm_mya_tsk_cfx_clt_core

import qsm_maya.tasks.cfx_cloth.scripts as qsm_mya_tsk_cfx_clt_scripts

from . import shot_gnl_tool as _shot_gnl


class MayaShotCfxToolOpt(_shot_gnl.MayaShotGnlToolOpt):
    @classmethod
    def test(cls):
        from .. import task_parse as _task_parse

        task_session = _task_parse.TaskParse().generate_task_session_by_resource_source_scene_src_auto()

        task_tool_opt = task_session.generate_task_tool_opt()

        task_tool_opt.update_cfx_rig_for(
            'lily_Skin'
        )

    def __init__(self, *args, **kwargs):
        super(MayaShotCfxToolOpt, self).__init__(*args, **kwargs)

    @staticmethod
    def to_cfx_rig_namespace(rig_namespace):
        return 'cfx_rig__{}'.format('__'.join(rig_namespace.split(':')))

    def load_cfx_rig_for(self, rig_namespace):

        reference_cache = qsm_mya_core.ReferencesCache()

        rig_scene_path = reference_cache.get_file(rig_namespace)

        if not rig_scene_path:
            return
        
        cfx_cloth_asset_opt = qsm_mya_tsk_cfx_clt_core.CfxClothAssetOpt(rig_namespace)

        cfx_rig_namespace = cfx_cloth_asset_opt.cfx_rig_namespace

        # ignore when reference is exists
        node = reference_cache.get(cfx_rig_namespace)
        if node is None:
            rig_scene_ptn_opt = self._task_session.generate_pattern_opt_for(
                'asset-disorder-rig_scene-maya-file'
            )
            asset_variants = rig_scene_ptn_opt.get_variants(rig_scene_path)
            if asset_variants:
                task_variants = copy.copy(asset_variants)

                task_variants['step'] = 'cfx'
                task_variants['task'] = 'cfx_rig'

                cfx_rig_scene_path = self._task_session.get_latest_file_for(
                    'asset-release-maya-scene-file', **task_variants
                )
                if not rig_scene_path:
                    if not bsc_storage.StgPath.get_is_file(cfx_rig_scene_path):
                        return
                    return

                cfx_cloth_asset_opt.load_cfx_rig_from(cfx_rig_scene_path)

                locations = qsm_mya_core.Namespace.find_roots(cfx_rig_namespace)
                for i_location in locations:
                    qsm_mya_tsk_cfx_clt_core.ShotCfxRigGroupOpt().add_one(i_location)

        cfx_cloth_asset_opt.connect_to_rig()

    def update_cfx_rig_for(self, rig_namespace):
        cfx_cloth_asset_opt = qsm_mya_tsk_cfx_clt_core.CfxClothAssetOpt(rig_namespace)
        if cfx_cloth_asset_opt.get_cfx_rig_is_loaded():
            scene_path_old = cfx_cloth_asset_opt.get_cfx_rig_scene_path()
            variants = self._task_session.generate_file_variants_for(
                'asset-release-maya-scene-file', scene_path_old
            )
            if variants:
                scene_path_new = self._task_session.get_latest_file_for(
                    'asset-release-maya-scene-file', **variants
                )
                if scene_path_old != scene_path_new:
                    cfx_cloth_asset_opt.update_cfx_rig_scene(scene_path_new)
                    cfx_cloth_asset_opt.connect_to_rig()

        cfx_cloth_asset_opt.connect_to_rig()

    @classmethod
    def export_cloth_cache_for(cls, rig_namespace, directory_path, frame_range, frame_step=1, frame_offset=0):
        cfx_cloth_asset_opt = qsm_mya_tsk_cfx_clt_core.CfxClothAssetOpt(rig_namespace)
        cfx_rig_namespace = cfx_cloth_asset_opt.cfx_rig_namespace
        resource = qsm_mya_tsk_cfx_clt_core.CfxRigAsset(cfx_rig_namespace)

        qsm_mya_tsk_cfx_clt_scripts.CfxNClothCacheOpt(resource).do_export(
            directory_path, frame_range, frame_step, frame_offset
        )
