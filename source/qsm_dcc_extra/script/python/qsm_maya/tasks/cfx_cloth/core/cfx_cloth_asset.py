# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .... import core as _mya_core

from ....resource import core as _rsc_core


class CfxRigAsset(_rsc_core.Asset):

    def __init__(self, *args, **kwargs):
        super(CfxRigAsset, self).__init__(*args, **kwargs)

        self._rig_namespace = ':'.join(self._namespace.split(':')[:-1])

    @property
    def rig_namespace(self):
        return self._rig_namespace

    def find_output_geo_location(self):
        _ = cmds.ls('{}:cfx_output_geo_grp'.format(self._namespace), long=1)
        if _:
            return _[0]

    def generate_cfx_cloth_export_args(self):
        mesh_transforms = []
        location = self.find_output_geo_location()
        meshes = _mya_core.Group.find_siblings(
            location, 'mesh'
        )
        for i_shape in meshes:
            i_transform = _mya_core.Shape.get_transform(i_shape)
            if _mya_core.Transform.is_visible(i_transform):
                mesh_transforms.append(i_transform)

        return mesh_transforms
