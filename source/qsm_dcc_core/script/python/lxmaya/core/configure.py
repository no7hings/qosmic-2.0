# coding:utf-8
import enum


class MyaUtil(object):
    OBJ_PATHSEP = '|'
    PORT_PATHSEP = '.'
    NAMESPACE_PATHSEP = ':'


class MyaNodeTypes(enum.EnumMeta):
    Mesh = 'mesh'
    Curve = 'nurbsCurve'
    Transform = 'transform'
    File = 'file'
    Material = 'shadingEngine'
    #
    XgenPalette = 'xgmPalette'
    XgenDescription = 'xgmDescription'
    XgenSplineGuide = 'xgmSplineGuide'


class MyaNodeApiTypes(object):
    Transform = 'kTransform'
    TransformPlugin = 'kPluginTransformNode'
    #
    Transforms = {
        Transform,
        TransformPlugin
    }


class MyaXGen(object):
    PATH_IGNORE_DICT = {
        'RandomGenerator': {
            'pointDir': ('usePoints', 'false')
        },
        'SplinePrimitive': {
            'cacheFileName': ('useCache', 'false'),
            'regionMap': ('regionMask', ['0.0', '0'])
        },
        'ClumpingFXModule': {
            'controlMapDir': [('useControlMaps', '0'), ('controlMask', ['0.0', '0'])]
        },
        'NoiseFXModule': {
            'bakeDir': ('mode', '0')
        }
    }
