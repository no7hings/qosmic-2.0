# coding:utf-8


class MeshCountDataOpt(object):
    def __init__(self, data):
        self._data = data

    @property
    def face(self):
        return self._data['all']['face']

    @property
    def face_per_world_area(self):
        return self._data['all']['face_per_world_area']

    @property
    def triangle(self):
        return self._data['all']['triangle']

    @property
    def triangle_per_world_area(self):
        return self._data['all']['triangle_per_world_area']

    @property
    def geometry_all(self):
        return self._data['all']['geometry_all']

    @property
    def geometry_visible(self):
        return self._data['all']['geometry_visible']

    @property
    def non_cache_face_percentage(self):
        if 'gpu_caches' in self._data:
            triangle_all = self._data['all']['triangle']
            cache_triangle = 0
            for k, v in self._data['gpu_caches'].items():
                cache_triangle += v['triangle']
            return float((triangle_all-cache_triangle))/float(triangle_all)*100
        return 100

    @property
    def components(self):
        return self._data.get('components', {})

    @property
    def gpu_caches(self):
        return self._data.get('gpu_caches', {})
    

class ComponentMeshCountOpt(object):
    def __init__(self, data):
        self._data = data

    @property
    def triangle(self):
        return self._data['triangle']

    @property
    def component_triangle(self):
        return self._data['triangle']
