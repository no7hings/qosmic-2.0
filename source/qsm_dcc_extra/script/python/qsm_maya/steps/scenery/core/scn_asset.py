# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ....general import core as _gnl_core

from ....resource import core as _rsc_core

from .... import core as _mya_core


class SceneryAsset(_rsc_core.Asset):
    def __init__(self, *args, **kwargs):
        super(SceneryAsset, self).__init__(*args, **kwargs)

    def get_unit_assembly_location(self):
        _ = cmds.ls(
            '{}:{}'.format(self.namespace, _gnl_core.ResourceCacheNodes.UnitAssemblyName),
            long=1
        )
        if _:
            return _[0]

    def is_unit_assembly_exists(self):
        _ = self.get_unit_assembly_location()
        if _:
            if cmds.objExists(_) is True:
                return True
        return False
    
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


class SceneryAssetQuery(_rsc_core.AssetsQuery):
    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Maya/Final/{asset}.ma'

    RESOURCE_CLS = SceneryAsset

    def __init__(self):
        super(SceneryAssetQuery, self).__init__()

    def check_is_valid(self, *args, **kwargs):
        file_path = kwargs['file']
        return self._pth.check_is_matched(file_path)
