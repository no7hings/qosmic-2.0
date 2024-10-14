# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_screw.core as qsm_scr_core

from . import asset_general as _asset_general


class AssetSnapShotGenerateOpt(_asset_general.AssetGeneral):
    TASK_KEY = 'snapshot_generate'
    API_VERSION = 1.0

    def __init__(self, *args, **kwargs):
        super(AssetSnapShotGenerateOpt, self).__init__(*args, **kwargs)

    def generate_args(self):
        scr_stage = qsm_scr_core.Stage(self._scr_stage_key)
        file_path = scr_stage.get_node_parameter(self._scr_node_path, 'scene')
        if not file_path:
            return

        task_name = '[{}][{}]'.format(
            self.TASK_KEY, bsc_storage.StgFileOpt(file_path).name
        )

        image_path = qsm_gnl_core.MayaCache.generate_asset_snapshot_file(file_path, version=self.API_VERSION)
        if bsc_storage.StgFileOpt(image_path).get_is_file() is False:
            # unregister first
            self.unregister()

            cmd_script = qsm_gnl_core.MayaCacheProcess.generate_cmd_script_by_option_dict(
                self.TASK_KEY,
                dict(
                    file_path=file_path,
                    image_path=image_path,
                )
            )
            return task_name, cmd_script, image_path
        return task_name, None, image_path

    def unregister(self):
        scr_stage = qsm_scr_core.Stage(self._scr_stage_key)
        # remove exists
        scr_stage.remove_assigns_below(
            self._scr_node_path, '/system_resource_usage/memory'
        )

        scr_stage.create_node_tag_assign(
            self._scr_node_path, '/system_resource_usage/memory/unspecified'
        )

    def register(self):
        scr_stage = qsm_scr_core.Stage(self._scr_stage_key)
        file_path = scr_stage.get_node_parameter(self._scr_node_path, 'scene')
        if not file_path:
            return

        image_path = qsm_gnl_core.MayaCache.generate_asset_snapshot_file(file_path, version=self.API_VERSION)

        scr_stage.upload_node_preview(
            self._scr_node_path, image_path
        )
        # register exists
        memory_size = scr_stage.get_node_parameter(
            self._scr_node_path, 'system_memory_usage'
        )
        if memory_size:
            # string from database
            memory_size = int(memory_size)
            # register process
            self.register_process_memory_usage('snapshot_generate', memory_size)
            # register tag
            # remove exists
            scr_stage.remove_assigns_below(
                self._scr_node_path, '/system_resource_usage/memory'
            )

            tag_name = _asset_general.AssetTag.to_memory_size_tag(memory_size)
            tag_path = '/system_resource_usage/memory/{}'.format(tag_name)
            scr_stage.create_node_tag_assign(
                self._scr_node_path, tag_path
            )
