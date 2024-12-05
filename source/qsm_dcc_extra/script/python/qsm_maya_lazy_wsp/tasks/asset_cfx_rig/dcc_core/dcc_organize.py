# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core


class AbsSetBaseOpt(object):
    SET_ROOT = 'QSM_SET'

    SET_NAME = None

    @classmethod
    def create_root_set(cls):
        return qsm_mya_core.Set.create(cls.SET_ROOT)

    @classmethod
    def create_set(cls):
        set_root = cls.create_root_set()
        set_name = qsm_mya_core.Set.create(cls.SET_NAME)
        qsm_mya_core.Set.add_one(set_root, set_name)
        return set_name


# group
class AbsGroupOrg(AbsSetBaseOpt):
    LOCATION = None

    SET_NAME = 'QSM_GROUP_SET'

    def __init__(self):
        if qsm_mya_core.Node.is_exists(self.LOCATION) is False:
            qsm_mya_core.Group.create_dag(self.LOCATION)

    def add_one(self, path):
        if path.startswith('{}|'.format(self.LOCATION)):
            return path
        return qsm_mya_core.Group.add_one(self.LOCATION, path)


#   bridge
class CfxBridgeGeoGrpOrg(AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_bridge_grp|cfx_bridge_geo_grp'

    def __init__(self):
        super(CfxBridgeGeoGrpOrg, self).__init__()


class CfxBridgeControlGrpOrg(AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_bridge_grp|cfx_bridge_control_grp'

    def __init__(self):
        super(CfxBridgeControlGrpOrg, self).__init__()


#   cloth
class CfxClothGeoGrpOrg(AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_output_geo_grp|cfx_cloth_geo_grp'

    def __init__(self):
        super(CfxClothGeoGrpOrg, self).__init__()


#   cloth proxy
class CfxClothProxyGeoGrpOrg(AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_cloth_proxy_grp|cfx_cloth_proxy_geo_grp'

    def __init__(self):
        super(CfxClothProxyGeoGrpOrg, self).__init__()


class CfxNClothGrpOrg(AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_ncloth_grp'

    def __init__(self):
        super(CfxNClothGrpOrg, self).__init__()


class CfxNRigidGrpOrg(AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_nrigid_grp'

    def __init__(self):
        super(CfxNRigidGrpOrg, self).__init__()


#   collider
class CfxColliderGeoGrpOrg(AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_collider_grp|cfx_collider_geo_grp'

    def __init__(self):
        super(CfxColliderGeoGrpOrg, self).__init__()


#   appendix
class CfxAppendixGeoGrpOrg(AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_output_geo_grp|cfx_appendix_geo_grp'

    def __init__(self):
        super(CfxAppendixGeoGrpOrg, self).__init__()


#   dynamic
class CfxNucleusGrpOrg(AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_nucleus_grp'

    def __init__(self):
        super(CfxNucleusGrpOrg, self).__init__()


#   wrap
class CfxWrapGrpOrg(AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_wrap_grp'

    def __init__(self):
        super(CfxWrapGrpOrg, self).__init__()


# layer
class AbsLayerOrg(AbsSetBaseOpt):
    NAME = None
    RGB = (0, 0, 0)
    VISIBLE = 0

    SET_NAME = 'QSM_LAYER_SET'

    def __init__(self):
        if qsm_mya_core.Node.is_exists(self.NAME) is False:
            layer_name = qsm_mya_core.DisplayLayer.create(self.NAME)
            qsm_mya_core.DisplayLayer.set_rgb(self.NAME, self.RGB)
            qsm_mya_core.DisplayLayer.set_visible(self.NAME, self.VISIBLE)
            set_name = self.create_set()
            qsm_mya_core.Set.add_one(set_name, layer_name)

    def add_one(self, path):
        qsm_mya_core.DisplayLayer.add_one(self.NAME, path)


#   source
class CfxSourceGeoLyrOrg(AbsLayerOrg):
    NAME = 'CFX_SOURCE_GEO_LYR'
    RGB = (0, 0, 0)
    VISIBLE = 0

    def __init__(self):
        super(CfxSourceGeoLyrOrg, self).__init__()


#   bridge
class CfxBridgeGeoLyrOrg(AbsLayerOrg):
    NAME = 'CFX_BRIDGE_GEO_LYR'
    RGB = (1, 0, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxBridgeGeoLyrOrg, self).__init__()


class CfxBridgeControlLyrOrg(AbsLayerOrg):
    NAME = 'CFX_BRIDGE_CONTROL_LYR'
    RGB = (0, 1, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxBridgeControlLyrOrg, self).__init__()


#   cloth
class CfxClothGeoLyrOrg(AbsLayerOrg):
    NAME = 'CFX_CLOTH_GEO_LYR'
    RGB = (1, 0, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxClothGeoLyrOrg, self).__init__()


#   cloth proxy
class CfxClothProxyGeoLyrOrg(AbsLayerOrg):
    NAME = 'CFX_CLOTH_PROXY_GEO_LYR'
    RGB = (0, 1, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxClothProxyGeoLyrOrg, self).__init__()


#   collider
class CfxColliderGeoLyrOrg(AbsLayerOrg):
    NAME = 'CFX_COLLIDER_GEO_LYR'
    RGB = (0, 0, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxColliderGeoLyrOrg, self).__init__()


#   appendix
class CfxAppendixGeoLyrOrg(AbsLayerOrg):
    NAME = 'CFX_APPENDIX_GEO_LYR'
    RGB = (1, 1, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxAppendixGeoLyrOrg, self).__init__()


# material
class AbsMaterialOrg(AbsSetBaseOpt):
    NAME = None
    RGB = (0, 0, 0)

    SET_NAME = 'QSM_MATERIAL_SET'

    def __init__(self):
        if qsm_mya_core.Node.is_exists(self.NAME) is False:
            qsm_mya_core.Material.create_as_lambert(self.NAME, self.RGB)

    def assign_to(self, path):
        qsm_mya_core.Material.assign_to(
            self.NAME, path
        )


#   bridge
class CfxBridgeGeoMtlOrg(AbsMaterialOrg):
    NAME = 'CFX_BRIDGE_MTL'
    RGB = (1, 0, 0)

    def __init__(self):
        super(CfxBridgeGeoMtlOrg, self).__init__()


#   cloth
class CfxClothGeoMtlOrg(AbsMaterialOrg):
    NAME = 'CFX_CLOTH_MTL'
    RGB = (1, 0, 1)

    def __init__(self):
        super(CfxClothGeoMtlOrg, self).__init__()


#   cloth proxy
class CfxClothProxyGeoMtlOrg(AbsMaterialOrg):
    NAME = 'CFX_CLOTH_PROXY_MTL'
    RGB = (0, 1, 0)

    def __init__(self):
        super(CfxClothProxyGeoMtlOrg, self).__init__()


#   collider
class CfxColliderGeoMtlOrg(AbsMaterialOrg):
    NAME = 'CFX_COLLIDER_MTL'
    RGB = (0, 0, 1)

    def __init__(self):
        super(CfxColliderGeoMtlOrg, self).__init__()


#   appendix
class CfxAppendixGeoMtlOrg(AbsMaterialOrg):
    NAME = 'CFX_APPENDIX_MTL'
    RGB = (1, 1, 0)

    def __init__(self):
        super(CfxAppendixGeoMtlOrg, self).__init__()
