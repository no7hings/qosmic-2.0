# coding:utf-8
from ...resource import core as _rsc_core

from ... import core as _mya_core


class Scenery(_rsc_core.Resource):
    def __init__(self, *args, **kwargs):
        super(Scenery, self).__init__(*args, **kwargs)
    
    def find_nodes_by_scheme(self, scheme):
        if scheme == 'root':
            return _mya_core.Namespace.find_roots(
                self.namespace
            )
        elif scheme == 'geometry':
            return _mya_core.Namespace.find_all_dag_nodes(
                self.namespace, ['mesh', 'gpuCache']
            )
        elif scheme == 'none':
            return []


class SceneriesQuery(_rsc_core.ResourcesQuery):
    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Maya/Final/{asset}.ma'

    RESOURCE_CLS = Scenery

    def __init__(self):
        super(SceneriesQuery, self).__init__()