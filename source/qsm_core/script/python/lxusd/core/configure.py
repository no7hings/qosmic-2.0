# coding:utf-8
from lxusd.core.wrap import *

import lxuniverse.core as unr_core


class UsdTypes(object):
    if USD_FLAG is True:
        MAPPER = {
            unr_core.UnrType.CONSTANT_BOOLEAN: Sdf.ValueTypeNames.Bool,
            unr_core.UnrType.CONSTANT_INTEGER: Sdf.ValueTypeNames.Int,
            unr_core.UnrType.CONSTANT_FLOAT: Sdf.ValueTypeNames.Float,
            unr_core.UnrType.CONSTANT_STRING: Sdf.ValueTypeNames.String,
            #
            unr_core.UnrType.COLOR_COLOR3: Sdf.ValueTypeNames.Color3f,
            unr_core.UnrType.ARRAY_COLOR3: Sdf.ValueTypeNames.Color3fArray,
            #
            unr_core.UnrType.ARRAY_STRING: Sdf.ValueTypeNames.StringArray,
        }


class UsdNodeCategories(object):
    LYNXI = 'lynxi'


class UsdNodeTypes(object):
    Xform = 'Xform'
    Mesh = 'Mesh'
    NurbsCurves = 'NurbsCurves'
    BasisCurves = 'BasisCurves'
    #
    GeometrySubset = 'GeomSubset'


class UsdNodes(object):
    PATHSEP = '/'
