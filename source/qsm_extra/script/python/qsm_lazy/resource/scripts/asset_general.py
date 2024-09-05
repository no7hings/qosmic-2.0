# coding:utf-8
from ...screw import core as _scr_core


class AssetGeneral(object):
    def __init__(self, scr_stage_key, scr_node_path):
        self._scr_stage_key = scr_stage_key
        self._scr_node_path = scr_node_path

    def register_process_memory_usage_by_profile(self, process_name, profile_data):
        if 'memory_size' in profile_data:
            memory_size = profile_data['memory_size']
            self.register_process_memory_usage(process_name, memory_size)

    def register_process_memory_usage(self, process_name, size):
        scr_stage = _scr_core.Stage(self._scr_stage_key)
        scr_stage.create_or_update_parameters(
            self._scr_node_path, 'process_memory_usage.{}'.format(process_name), str(size)
        )

    def register_system_resource_usage_by_profile(self, profile_data):
        if 'memory_size' in profile_data:
            memory_size = profile_data['memory_size']
            self.register_memory_usage(memory_size)

    def register_memory_usage(self, size):
        scr_stage = _scr_core.Stage(self._scr_stage_key)

        scr_stage.create_or_update_parameters(
            self._scr_node_path, 'system_memory_usage', str(size)
        )
        # remove exists
        scr_stage.remove_assigns_below(
            self._scr_node_path, '/system_resource_usage/memory/'
        )

        tag_name = scr_stage.to_memory_size_tag(size)
        tag_path = '/system_resource_usage/memory/{}'.format(tag_name)
        scr_stage.create_tag_assign(
            self._scr_node_path, tag_path
        )


