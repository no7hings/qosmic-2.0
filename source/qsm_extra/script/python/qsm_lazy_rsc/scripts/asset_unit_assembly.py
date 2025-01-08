# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_general.process as qsm_gnl_process

import qsm_screw.core as qsm_scr_core

from . import asset_general as _asset_general


class AssetUnitAssemblyGenerateOpt(_asset_general.AssetGeneralOpt):
    TASK_KEY = 'unit_assembly_generate'
    API_VERSION = 1.0

    def __init__(self, scr_stage_name, scr_node_path):
        super(AssetUnitAssemblyGenerateOpt, self).__init__(scr_stage_name, scr_node_path)

    def generate_args(self):
        scr_stage = qsm_scr_core.Stage(self._scr_stage_name)
        is_model = scr_stage.is_exists_node_tag(
            self._scr_node_path, '/task/model'
        )
        if is_model is True:
            file_path = scr_stage.get_node_parameter(self._scr_node_path, 'scene')
            if not file_path:
                return
    
            task_name = '[{}][{}]'.format(
                self.TASK_KEY, bsc_storage.StgFileOpt(file_path).name
            )
    
            cache_path = qsm_gnl_core.MayaCache.generate_asset_unit_assembly_file_new(file_path)
            if bsc_storage.StgFileOpt(cache_path).get_is_file() is False:
                cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script_by_option_dict(
                    self.TASK_KEY,
                    dict(
                        file_path=file_path,
                        cache_path=cache_path,
                    )
                )
                return task_name, cmd_script, cache_path
            return task_name, None, cache_path

    def register(self):
        scr_stage = qsm_scr_core.Stage(self._scr_stage_name)
        file_path = scr_stage.get_node_parameter(self._scr_node_path, 'scene')
        if not file_path:
            return

        cache_path = qsm_gnl_core.MayaCache.generate_asset_unit_assembly_file_new(file_path)

        scr_stage.create_or_update_parameters(
            self._scr_node_path, 'unit_assembly_cache', cache_path
        )
