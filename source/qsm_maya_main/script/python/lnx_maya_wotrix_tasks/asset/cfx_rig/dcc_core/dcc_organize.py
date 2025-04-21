# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from qsm_maya.handles import abc_


# group
#   bridge
class CfxBridgeGeoGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_bridge_grp|cfx_bridge_geo_grp'

    def __init__(self):
        super(CfxBridgeGeoGrpOrg, self).__init__()


class CfxBridgeControlGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_bridge_grp|cfx_bridge_control_grp'

    def __init__(self):
        super(CfxBridgeControlGrpOrg, self).__init__()


#   output
class CfxOutputGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_output_geo_grp'

    def __init__(self):
        super(CfxOutputGrpOrg, self).__init__()


#   output cloth
class CfxClothGeoGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_output_geo_grp|cfx_cloth_geo_grp'

    def __init__(self):
        super(CfxClothGeoGrpOrg, self).__init__()


#   output appendix
class CfxAppendixGeoGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_output_geo_grp|cfx_appendix_geo_grp'

    def __init__(self):
        super(CfxAppendixGeoGrpOrg, self).__init__()


#   cloth proxy
class CfxClothProxyGeoGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_cloth_proxy_grp|cfx_cloth_proxy_geo_grp'

    def __init__(self):
        super(CfxClothProxyGeoGrpOrg, self).__init__()


class CfxNClothGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_ncloth_grp'

    def __init__(self):
        super(CfxNClothGrpOrg, self).__init__()


class CfxNRigidGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_nrigid_grp'

    def __init__(self):
        super(CfxNRigidGrpOrg, self).__init__()


#   collider
class CfxColliderGeoGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_collider_grp|cfx_collider_geo_grp'

    def __init__(self):
        super(CfxColliderGeoGrpOrg, self).__init__()


#   dynamic
class CfxNucleusGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_nucleus_grp'

    def __init__(self):
        super(CfxNucleusGrpOrg, self).__init__()


#   wrap
class CfxWrapGrpOrg(abc_.AbsGroupOrg):
    LOCATION = '|master|cfx_rig|cfx_wrap_grp'

    def __init__(self):
        super(CfxWrapGrpOrg, self).__init__()


# layer
#   source
class CfxSourceGeoLyrOrg(abc_.AbsLayerOrg):
    NAME = 'CFX_SOURCE_GEO_LYR'
    RGB = (0, 0, 0)
    VISIBLE = 0

    def __init__(self):
        super(CfxSourceGeoLyrOrg, self).__init__()


#   bridge
class CfxBridgeGeoLyrOrg(abc_.AbsLayerOrg):
    NAME = 'CFX_BRIDGE_GEO_LYR'
    RGB = (1, 0, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxBridgeGeoLyrOrg, self).__init__()


class CfxBridgeControlLyrOrg(abc_.AbsLayerOrg):
    NAME = 'CFX_BRIDGE_CONTROL_LYR'
    RGB = (0, 1, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxBridgeControlLyrOrg, self).__init__()


#   cloth
class CfxClothGeoLyrOrg(abc_.AbsLayerOrg):
    NAME = 'CFX_CLOTH_GEO_LYR'
    RGB = (1, 0, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxClothGeoLyrOrg, self).__init__()


#   cloth proxy
class CfxClothProxyGeoLyrOrg(abc_.AbsLayerOrg):
    NAME = 'CFX_CLOTH_PROXY_GEO_LYR'
    RGB = (0, 1, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxClothProxyGeoLyrOrg, self).__init__()


#   collider
class CfxColliderGeoLyrOrg(abc_.AbsLayerOrg):
    NAME = 'CFX_COLLIDER_GEO_LYR'
    RGB = (0, 0, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxColliderGeoLyrOrg, self).__init__()


#   appendix
class CfxAppendixGeoLyrOrg(abc_.AbsLayerOrg):
    NAME = 'CFX_APPENDIX_GEO_LYR'
    RGB = (1, 1, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxAppendixGeoLyrOrg, self).__init__()


# material
#   bridge
class CfxBridgeGeoMtlOrg(abc_.AbsMaterialOrg):
    NAME = 'CFX_BRIDGE_MTL'
    RGB = (1, 0, 0)

    def __init__(self):
        super(CfxBridgeGeoMtlOrg, self).__init__()


#   cloth
class CfxClothGeoMtlOrg(abc_.AbsMaterialOrg):
    NAME = 'CFX_CLOTH_MTL'
    RGB = (1, 0, 1)

    def __init__(self):
        super(CfxClothGeoMtlOrg, self).__init__()


#   cloth proxy
class CfxClothProxyGeoMtlOrg(abc_.AbsMaterialOrg):
    NAME = 'CFX_CLOTH_PROXY_MTL'
    RGB = (0, 1, 0)

    def __init__(self):
        super(CfxClothProxyGeoMtlOrg, self).__init__()


#   collider
class CfxColliderGeoMtlOrg(abc_.AbsMaterialOrg):
    NAME = 'CFX_COLLIDER_MTL'
    RGB = (0, 0, 1)

    def __init__(self):
        super(CfxColliderGeoMtlOrg, self).__init__()


#   appendix
class CfxAppendixGeoMtlOrg(abc_.AbsMaterialOrg):
    NAME = 'CFX_APPENDIX_MTL'
    RGB = (1, 1, 0)

    def __init__(self):
        super(CfxAppendixGeoMtlOrg, self).__init__()
