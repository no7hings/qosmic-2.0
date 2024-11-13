# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .... import core as _mya_core


class AbsSetBaseOpt(object):
    SET_ROOT = 'QSM_SET'

    SET_NAME = None

    @classmethod
    def create_root_set(cls):
        return _mya_core.Set.create(cls.SET_ROOT)

    @classmethod
    def create_set(cls):
        set_root = cls.create_root_set()
        set_name = _mya_core.Set.create(cls.SET_NAME)
        _mya_core.Set.add_one(set_root, set_name)
        return set_name


# group
class AbsGroupOpt(AbsSetBaseOpt):
    LOCATION = None

    SET_NAME = 'QSM_GROUP_SET'

    def __init__(self):
        if _mya_core.Node.is_exists(self.LOCATION) is False:
            _mya_core.Group.create_dag(self.LOCATION)

    def add_one(self, path):
        if path.startswith('{}|'.format(self.LOCATION)):
            return path
        return _mya_core.Group.add_one(self.LOCATION, path)


#   bridge
class CfxBridgeGeoGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx_rig|cfx_bridge_grp|cfx_bridge_geo_grp'

    def __init__(self):
        super(CfxBridgeGeoGrpOpt, self).__init__()


class CfxBridgeControlGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx_rig|cfx_bridge_grp|cfx_bridge_control_grp'

    def __init__(self):
        super(CfxBridgeControlGrpOpt, self).__init__()


#   cloth
class CfxClothGeoGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx_rig|cfx_output_geo_grp|cfx_cloth_geo_grp'

    def __init__(self):
        super(CfxClothGeoGrpOpt, self).__init__()


#   cloth proxy
class CfxClothProxyGeoGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx_rig|cfx_cloth_proxy_grp|cfx_cloth_proxy_geo_grp'

    def __init__(self):
        super(CfxClothProxyGeoGrpOpt, self).__init__()


class CfxNClothGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx_rig|cfx_ncloth_grp'

    def __init__(self):
        super(CfxNClothGrpOpt, self).__init__()


class CfxNRigidGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx_rig|cfx_nrigid_grp'

    def __init__(self):
        super(CfxNRigidGrpOpt, self).__init__()


#   collider
class CfxColliderGeoGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx_rig|cfx_collider_grp|cfx_collider_geo_grp'

    def __init__(self):
        super(CfxColliderGeoGrpOpt, self).__init__()


#   appendix
class CfxAppendixGeoGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx_rig|cfx_output_geo_grp|cfx_appendix_geo_grp'

    def __init__(self):
        super(CfxAppendixGeoGrpOpt, self).__init__()


#   dynamic
class CfxNucleusGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx_rig|cfx_nucleus_grp'

    def __init__(self):
        super(CfxNucleusGrpOpt, self).__init__()


#   wrap
class CfxWrapGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx_rig|cfx_wrap_grp'

    def __init__(self):
        super(CfxWrapGrpOpt, self).__init__()


# layer
class AbsLayerOpt(AbsSetBaseOpt):
    NAME = None
    RGB = (0, 0, 0)
    VISIBLE = 0

    SET_NAME = 'QSM_LAYER_SET'

    def __init__(self):
        if _mya_core.Node.is_exists(self.NAME) is False:
            layer_name = _mya_core.DisplayLayer.create(self.NAME)
            _mya_core.DisplayLayer.set_rgb(self.NAME, self.RGB)
            _mya_core.DisplayLayer.set_visible(self.NAME, self.VISIBLE)
            set_name = self.create_set()
            _mya_core.Set.add_one(set_name, layer_name)

    def add_one(self, path):
        _mya_core.DisplayLayer.add_one(self.NAME, path)


#   source
class CfxSourceGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_SOURCE_GEO_LYR'
    RGB = (0, 0, 0)
    VISIBLE = 0

    def __init__(self):
        super(CfxSourceGeoLyrOpt, self).__init__()


#   bridge
class CfxBridgeGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_BRIDGE_GEO_LYR'
    RGB = (1, 0, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxBridgeGeoLyrOpt, self).__init__()


class CfxBridgeControlLyrOpt(AbsLayerOpt):
    NAME = 'CFX_BRIDGE_CONTROL_LYR'
    RGB = (0, 1, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxBridgeControlLyrOpt, self).__init__()


#   cloth
class CfxClothGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_CLOTH_GEO_LYR'
    RGB = (1, 0, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxClothGeoLyrOpt, self).__init__()


#   cloth proxy
class CfxClothProxyGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_CLOTH_PROXY_GEO_LYR'
    RGB = (0, 1, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxClothProxyGeoLyrOpt, self).__init__()


#   collider
class CfxColliderGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_COLLIDER_GEO_LYR'
    RGB = (0, 0, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxColliderGeoLyrOpt, self).__init__()


#   appendix
class CfxAppendixGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_APPENDIX_GEO_LYR'
    RGB = (1, 1, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxAppendixGeoLyrOpt, self).__init__()


# material
class AbsMaterialOpt(AbsSetBaseOpt):
    NAME = None
    RGB = (0, 0, 0)

    SET_NAME = 'QSM_MATERIAL_SET'

    def __init__(self):
        if _mya_core.Node.is_exists(self.NAME) is False:
            _mya_core.Material.create_as_lambert(self.NAME, self.RGB)

    def assign_to(self, path):
        _mya_core.Material.assign_to(
            self.NAME, path
        )


#   bridge
class CfxBridgeGeoMtlOpt(AbsMaterialOpt):
    NAME = 'CFX_BRIDGE_MTL'
    RGB = (1, 0, 0)

    def __init__(self):
        super(CfxBridgeGeoMtlOpt, self).__init__()


#   cloth
class CfxClothGeoMtlOpt(AbsMaterialOpt):
    NAME = 'CFX_CLOTH_MTL'
    RGB = (1, 0, 1)

    def __init__(self):
        super(CfxClothGeoMtlOpt, self).__init__()


#   cloth proxy
class CfxClothProxyGeoMtlOpt(AbsMaterialOpt):
    NAME = 'CFX_CLOTH_PROXY_MTL'
    RGB = (0, 1, 0)

    def __init__(self):
        super(CfxClothProxyGeoMtlOpt, self).__init__()


#   collider
class CfxColliderGeoMtlOpt(AbsMaterialOpt):
    NAME = 'CFX_COLLIDER_MTL'
    RGB = (0, 0, 1)

    def __init__(self):
        super(CfxColliderGeoMtlOpt, self).__init__()


#   appendix
class CfxAppendixGeoMtlOpt(AbsMaterialOpt):
    NAME = 'CFX_APPENDIX_MTL'
    RGB = (1, 1, 0)

    def __init__(self):
        super(CfxAppendixGeoMtlOpt, self).__init__()
