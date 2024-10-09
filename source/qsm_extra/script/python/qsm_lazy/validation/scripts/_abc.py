# coding:utf-8
import lxbasic.storage as bsc_storage

from .. import core as _core


class AbsValidationOpt(object):
    OPTION_KEY = None

    def __init__(self):
        self._options = _core.DccValidationOptions(self.OPTION_KEY)

    @property
    def options(self):
        return self._options

    def generate_process_options(self, input_options):
        options = dict()
        for i_branch in self._options.get_branches():
            i_leafs = input_options[i_branch]
            if i_leafs:
                i_leafs.sort()
                options[i_branch] = i_leafs
        return options

    def to_validation_result_args(self, validation_cache_path, mesh_count_cache_path, process_options):
        validation_result_dict = bsc_storage.StgFileOpt(validation_cache_path).set_read()
        mesh_count_data = bsc_storage.StgFileOpt(mesh_count_cache_path).set_read()
        validation_opt = self._options.update_process_options_to(process_options)
        validation_opt.update_process_options(process_options)
        mesh_count_result_dict = validation_opt.to_result_dict_for_mesh_count(mesh_count_data)
        component_mesh_count_result_dict =validation_opt.to_result_dict_for_component_mesh_count(mesh_count_data)
        return validation_opt.to_result_args(
            validation_result_dict, mesh_count_result_dict, component_mesh_count_result_dict
        )
