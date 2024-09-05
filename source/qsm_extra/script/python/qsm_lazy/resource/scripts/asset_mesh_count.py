# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

from ...screw import core as _scr_core

from . import asset_general as _asset_general


class AssetMeshCountGenerateOpt(_asset_general.AssetGeneral):
    TASK_KEY = 'mesh_count_generate'
    API_VERSION = 1.0

    def __init__(self, *args, **kwargs):
        super(AssetMeshCountGenerateOpt, self).__init__(*args, **kwargs)

    def generate_args(self):
        scr_stage = _scr_core.Stage(self._scr_stage_key)
        file_path = scr_stage.get_node_parameter(self._scr_node_path, 'scene')
        if not file_path:
            return 

        task_name = '[{}][{}]'.format(
            self.TASK_KEY, bsc_storage.StgFileOpt(file_path).name
        )

        cache_path = qsm_gnl_core.MayaCache.generate_asset_mesh_count_file(file_path, version=self.API_VERSION)
        image_path = qsm_gnl_core.MayaCache.generate_asset_snapshot_file(file_path, version=self.API_VERSION)
        # check is existing
        if bsc_storage.StgFileOpt(cache_path).get_is_file() is False:
            # unregister first
            self.unregister()

            cmd_script = qsm_gnl_core.MayaCacheProcess.generate_cmd_script_by_option_dict(
                self.TASK_KEY,
                dict(
                    file_path=file_path,
                    cache_path=cache_path,
                    image_path=image_path,
                )
            )
            return task_name, cmd_script, cache_path, image_path
        return task_name, None, cache_path, image_path

    def unregister(self):
        scr_stage = _scr_core.Stage(self._scr_stage_key)
        # remove exists
        scr_stage.remove_assigns_below(
            self._scr_node_path, '/mesh_count/face/'
        )

        scr_stage.create_tag_assign(
            self._scr_node_path, '/mesh_count/face/unspecified'
        )
    
    def register(self):
        scr_stage = _scr_core.Stage(self._scr_stage_key)
        file_path = scr_stage.get_node_parameter(self._scr_node_path, 'scene')
        if not file_path:
            return

        cache_path = qsm_gnl_core.MayaCache.generate_asset_mesh_count_file(file_path, version=self.API_VERSION)
        image_path = qsm_gnl_core.MayaCache.generate_asset_snapshot_file(file_path, version=self.API_VERSION)

        data = bsc_storage.StgFileOpt(cache_path).set_read()

        scr_stage.create_or_update_parameters(
            self._scr_node_path, 'mesh_count', cache_path
        )
        # use triangle
        mesh_triangle = data['mesh_count']['all']['triangle']

        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.face',
            str(data['mesh_count']['all']['face'])
        )

        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.face_per_world_area',
            str(data['mesh_count']['all']['face_per_world_area'])
        )

        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.triangle',
            str(mesh_triangle)
        )
        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.triangle_per_world_area',
            str(data['mesh_count']['all']['triangle_per_world_area'])
        )

        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.geometry_all',
            str(data['mesh_count']['all']['geometry_all'])
        )
        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.geometry_visible',
            str(data['mesh_count']['all']['geometry_visible'])
        )

        count_tag = scr_stage.to_count_tag(mesh_triangle)
        tag_path = '/mesh_count/face/{}'.format(count_tag)
        # remove exists
        scr_stage.remove_assigns_below(
            self._scr_node_path, '/mesh_count/face/'
        )

        scr_stage.create_tag_assign(
            self._scr_node_path, tag_path
        )

        scr_stage.upload_node_preview(
            self._scr_node_path, image_path
        )
