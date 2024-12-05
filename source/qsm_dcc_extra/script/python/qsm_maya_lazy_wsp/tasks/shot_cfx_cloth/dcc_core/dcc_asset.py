# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

import qsm_maya.resource.core as qsm_mya_rsc_core


class CfxRigAsset(qsm_mya_rsc_core.Asset):

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
        meshes = qsm_mya_core.Group.find_siblings(
            location, 'mesh'
        )
        for i_shape in meshes:
            i_transform = qsm_mya_core.Shape.get_transform(i_shape)
            if qsm_mya_core.Transform.is_visible(i_transform):
                mesh_transforms.append(i_transform)

        return mesh_transforms
