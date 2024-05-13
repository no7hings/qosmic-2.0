# coding:utf-8
from ...resource import core as _rsc_core

from ... import core as _mya_core


class SceneryOpt(_rsc_core.ResourceOpt):
    def __init__(self, *args, **kwargs):
        super(SceneryOpt, self).__init__(*args, **kwargs)
    
    def find_nodes_by_scheme(self, scheme):
        if scheme == 'geometry':
            return _mya_core.Namespace.find_all_dag_nodes(
                self.namespace, ['mesh', 'gpuCache']
            )
        elif scheme == 'none':
            return []


class SceneriesQuery(_rsc_core.ResourcesQuery):
    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Maya/Final/{asset}.ma'

    RESOURCE_CLS = SceneryOpt

    def __init__(self):
        super(SceneriesQuery, self).__init__()
