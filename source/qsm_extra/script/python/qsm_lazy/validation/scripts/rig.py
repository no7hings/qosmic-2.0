# coding:utf-8
import copy

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import _abc


class RigValidationOpt(_abc.AbsValidationOpt):
    OPTION_KEY = 'lazy-validation/option/rig'

    def generate_process_args(self, file_path, process_options=None):
        if process_options is None:
            process_options = self._options.generate_process_options()

        api_version = 2.0
        process_options = copy.copy(process_options)
        process_options['version'] = api_version
        option_hash = bsc_core.BscHash.to_hash_key(process_options)

        task_name = '[rig-validation][{}]'.format(
            bsc_storage.StgFileOpt(file_path).name
        )
        validation_cache_path = qsm_gnl_core.MayaCache.generate_asset_rig_validation_result_file(
            file_path, api_version=option_hash
        )
        mesh_count_cache_path = qsm_gnl_core.MayaCache.generate_asset_mesh_count_file(
            file_path, version=api_version
        )
        if (
            bsc_storage.StgFileOpt(validation_cache_path).get_is_file() is False
            or bsc_storage.StgFileOpt(mesh_count_cache_path).get_is_file() is False
        ):
            cmd_script = qsm_gnl_core.MayaCacheProcess.generate_cmd_script_by_option_dict(
                'rig_validation',
                dict(
                    file_path=file_path,
                    validation_cache_path=validation_cache_path,
                    mesh_count_cache_path=mesh_count_cache_path,
                    process_options=process_options
                )
            )
            return task_name, cmd_script, validation_cache_path, mesh_count_cache_path
        return task_name, None, validation_cache_path, mesh_count_cache_path

    def __init__(self):
        super(RigValidationOpt, self).__init__()
