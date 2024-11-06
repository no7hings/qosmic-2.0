# coding:utf-8
import copy

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_general.process as qsm_gnl_process

import _abc


class SceneryValidationOpt(_abc.AbsValidationOpt):
    OPTION_KEY = 'lazy-validation/option/scenery'

    def generate_process_args(self, file_path, process_options=None):
        if process_options is None:
            process_options = self._options.generate_process_options()

        api_version = 1.0
        process_options = copy.copy(process_options)
        process_options['version'] = api_version
        option_hash = bsc_core.BscHash.to_hash_key(process_options)

        task_name = '[scenery-validation][{}]'.format(
            bsc_storage.StgFileOpt(file_path).name
        )
        validation_cache_path = qsm_gnl_core.MayaCache.generate_asset_scenery_validation_result_file(
            file_path, option_hash=option_hash
        )
        mesh_count_cache_path = qsm_gnl_core.MayaCache.generate_asset_mesh_count_file(
            file_path, version=api_version
        )
        if (
            bsc_storage.StgFileOpt(validation_cache_path).get_is_file() is False
            or bsc_storage.StgFileOpt(mesh_count_cache_path).get_is_file() is False
        ):
            cmd_script = qsm_gnl_process.MayaCacheProcess.generate_cmd_script_by_option_dict(
                'scenery_validation',
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
        super(SceneryValidationOpt, self).__init__()
