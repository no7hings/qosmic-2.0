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
            self._scr_node_path, '/mesh_count/face'
        )

        scr_stage.remove_assigns_below(
            self._scr_node_path, '/mesh_count/geometry'
        )

        scr_stage.remove_assigns_below(
            self._scr_node_path, '/mesh_count/non_cache_face_percentage'
        )

        scr_stage.create_tag_assign(
            self._scr_node_path, '/mesh_count/face/unspecified'
        )

        scr_stage.create_tag_assign(
            self._scr_node_path, '/mesh_count/geometry/unspecified'
        )

        scr_stage.create_tag_assign(
            self._scr_node_path, '/mesh_count/non_cache_face_percentage/unspecified'
        )
    
    def register(self):
        scr_stage = _scr_core.Stage(self._scr_stage_key)
        file_path = scr_stage.get_node_parameter(self._scr_node_path, 'scene')
        if not file_path:
            return

        cache_path = qsm_gnl_core.MayaCache.generate_asset_mesh_count_file(file_path, version=self.API_VERSION)
        image_path = qsm_gnl_core.MayaCache.generate_asset_snapshot_file(file_path, version=self.API_VERSION)

        data = bsc_storage.StgFileOpt(cache_path).set_read()
        
        mesh_count_data = data['mesh_count']
        mesh_count_data_opt = _asset_general.MeshCountDataOpt(mesh_count_data)

        scr_stage.create_or_update_parameters(
            self._scr_node_path, 'mesh_count', cache_path
        )
        # use triangle
        triangle_count = mesh_count_data_opt.triangle
        geometry_count = mesh_count_data_opt.geometry_all
        non_cache_face_percentage = mesh_count_data_opt.non_cache_face_percentage

        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.face',
            str(mesh_count_data_opt.face)
        )

        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.face_per_world_area',
            str(mesh_count_data_opt.face_per_world_area)
        )

        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.triangle',
            str(triangle_count)
        )
        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.triangle_per_world_area',
            str(mesh_count_data_opt.triangle_per_world_area)
        )

        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.geometry_all',
            str(geometry_count)
        )
        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.geometry_visible',
            str(mesh_count_data_opt.geometry_visible)
        )
        scr_stage.create_or_update_parameters(
            self._scr_node_path,
            'mesh_count.non_cache_face_percentage',
            non_cache_face_percentage
        )

        self.register_mesh_face_count_tag(triangle_count)
        self.register_mesh_geometry_count_tag(geometry_count)
        self.register_mesh_cache_percentage_tag(non_cache_face_percentage)

        scr_stage.upload_node_preview(
            self._scr_node_path, image_path
        )
