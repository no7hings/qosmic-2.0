# coding:utf-8
import qsm_screw.core as qsm_scr_core


class AssetTag(object):
    @classmethod
    def to_face_count_tag(cls, count):
        k = 1000
        m = k**2
        b = k**3
        if count < 10*k:
            return 'less_than_10k'
        elif 10*k <= count < 50*k:
            return '10k_to_50k'
        elif 50*k <= count < 100*k:
            return '50k_to_100k'
        elif 100*k <= count < 500*k:
            return '100k_to_500k'
        elif 500*k <= count < k**2:
            return '500k_to_1m'
        elif m <= count < m*5:
            return '1m_to_5m'
        elif m*5 <= count < m*10:
            return '5m_to_10m'
        elif m*10 <= count < m*50:
            return '10m_to_50m'
        elif m*50 <= count < m*100:
            return '50m_to_100m'
        elif m*100 <= count < m*500:
            return '100m_to_500m'
        elif m*500 <= count < b:
            return '500m_to_1b'
        elif b <= count:
            return 'more_than_1b'
    
    @classmethod
    def to_geometry_count_tag(cls, count):
        k = 1000
        if count < 500:
            return 'less_than_500'
        elif 500 <= count < k*1:
            return '500_to_1k'
        elif k*1 <= count < k*5:
            return '1k_to_5k'
        elif k*5 <= count < k*10:
            return '5k_to_10k'
        elif k*10 <= count < k*15:
            return '10k_to_15k'
        elif k*15 <= count < k*20:
            return '15k_to_20k'
        elif k*25 <= count < k*30:
            return '25k_to_30k'
        elif k*30 <= count:
            return 'more_than_30k'

    @classmethod
    def to_cache_percentage_tag(cls, percentage):
        p = 100
        if percentage <= 0:
            return '0p'
        elif 0 < percentage < p*.25:
            return '0p_25p'
        elif p*.25 <= percentage < p*.5:
            return '25p_50p'
        elif p*.5 <= percentage < p*.75:
            return '50p_75p'
        elif p*.75 <= percentage < p*1:
            return '75p_100p'
        elif p*1 <= percentage:
            return '100p'

    @classmethod
    def to_memory_size_tag(cls, size):
        kb = 1024
        mb = 1024**2
        gb = 1024**3
        if size < mb*500:
            return 'less_than_500mb'
        elif mb*500 <= size < gb*1:
            return '500mb_to_1gb'
        elif gb*1 <= size < gb*5:
            return '1gb_to_5gb'
        elif gb*5 <= size < gb*10:
            return '5gb_to_10gb'
        elif gb*10 <= size < gb*15:
            return '10gb_to_15gb'
        elif gb*15 <= size < gb*20:
            return '15gb_to_20gb'
        elif gb*20 <= size < gb*25:
            return '20gb_to_25gb'
        elif gb*25 <= size < gb*30:
            return '25gb_to_30gb'
        elif gb*30 <= size:
            return 'more_than_30gb'


class AssetGeneralOpt(object):
    def __init__(self, scr_stage_name, scr_node_path):
        self._scr_stage_name = scr_stage_name
        self._scr_node_path = scr_node_path

    def register_process_memory_usage_by_profile(self, process_name, profile_data):
        if 'memory_size' in profile_data:
            memory_size = profile_data['memory_size']
            self.register_process_memory_usage(process_name, memory_size)

    def register_process_memory_usage(self, process_name, size):
        scr_stage = qsm_scr_core.Stage(self._scr_stage_name)
        scr_stage.create_or_update_parameters(
            self._scr_node_path, 'process_memory_usage.{}'.format(process_name), str(size)
        )

    def register_system_resource_usage_by_profile(self, profile_data):
        if 'memory_size' in profile_data:
            memory_size = profile_data['memory_size']
            self.register_memory_usage(memory_size)

    def register_mesh_face_count_tag(self, mesh_triangle):
        scr_stage = qsm_scr_core.Stage(self._scr_stage_name)
        # remove exists
        scr_stage.remove_assigns_below(
            self._scr_node_path, '/mesh_count/face'
        )
        
        count_tag = AssetTag.to_face_count_tag(mesh_triangle)
        tag_path = '/mesh_count/face/{}'.format(count_tag)

        scr_stage.create_node_tag_assign(
            self._scr_node_path, tag_path
        )

    def register_mesh_geometry_count_tag(self, geometry_count):
        scr_stage = qsm_scr_core.Stage(self._scr_stage_name)
        # remove exists
        scr_stage.remove_assigns_below(
            self._scr_node_path, '/mesh_count/geometry'
        )
        
        count_tag = AssetTag.to_geometry_count_tag(geometry_count)
        tag_path = '/mesh_count/geometry/{}'.format(count_tag)

        scr_stage.create_node_tag_assign(
            self._scr_node_path, tag_path
        )
    
    def register_mesh_cache_percentage_tag(self, percentage):
        scr_stage = qsm_scr_core.Stage(self._scr_stage_name)
        # remove exists
        scr_stage.remove_assigns_below(
            self._scr_node_path, '/mesh_count/non_cache_face_percentage'
        )
        
        tag = AssetTag.to_cache_percentage_tag(percentage)
        tag_path = '/mesh_count/non_cache_face_percentage/{}'.format(tag)

        scr_stage.create_node_tag_assign(
            self._scr_node_path, tag_path
        )

    def register_memory_usage(self, size):
        scr_stage = qsm_scr_core.Stage(self._scr_stage_name)

        scr_stage.create_or_update_parameters(
            self._scr_node_path, 'system_memory_usage', str(size)
        )
        # remove exists
        scr_stage.remove_assigns_below(
            self._scr_node_path, '/system_resource_usage/memory'
        )

        tag_name = AssetTag.to_memory_size_tag(size)
        tag_path = '/system_resource_usage/memory/{}'.format(tag_name)
        scr_stage.create_node_tag_assign(
            self._scr_node_path, tag_path
        )
