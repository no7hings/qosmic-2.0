# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core

from ...rig import core as _rig_core


class CfxAdvRig(_rig_core.AdvRig):
    def __init__(self, *args, **kwargs):
        super(CfxAdvRig, self).__init__(*args, **kwargs)

    def find_all_cloth_export_args(self):
        clothes, meshes = [], []
        root = self.get_root()
        if root:
            _ = cmds.ls(root, dag=1, type='nCloth', noIntermediate=1, long=1) or []
            for i_path in _:
                i_geometry_path = _mya_core.NCloth.find_output_geometry(i_path)
                if i_geometry_path:
                    clothes.append(i_path)
                    meshes.append(i_geometry_path)
        return clothes, meshes


class CfxAdvRigsQuery(_rig_core.AdvRigsQuery):
    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'

    RESOURCE_CLS = CfxAdvRig

    def __init__(self):
        super(CfxAdvRigsQuery, self).__init__()

