# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.resource as qsm_mya_resource

from . import dcc_handle as _dcc_handle


class CfxRigAsset(qsm_mya_resource.Asset):

    def __init__(self, *args, **kwargs):
        super(CfxRigAsset, self).__init__(*args, **kwargs)

        self._rig_namespace = ':'.join(self._namespace.split(':')[:-1])

    @property
    def rig_namespace(self):
        return self._rig_namespace

    def generate_cfx_cloth_export_args(self, include_customize_deform_geometry=True):
        handle = _dcc_handle.ShotCfxRigHandle(self._namespace)
        geometry_args = handle.generate_export_args()
        if include_customize_deform_geometry is True:
            extend_geometry_args = handle.get_extend_geometry_args()
            return geometry_args+extend_geometry_args
        else:
            return geometry_args
