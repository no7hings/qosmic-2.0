# coding:utf-8
import qsm_maya.core as qsm_mya_core

from . import base as _base


class SurfaceNodeOpt(_base.AbsNodeOpt):
    SCHEME_BASE = '/node/surface'

    TYPE_INCLUDES = [
        'lambert',
        'blinn',
        'phong',
    ]

    DATA_KEY_INCLUDES = [
        _base.Util.DataKeys.Node,
        _base.Util.DataKeys.Sources
    ]

    SOURCE_ARGS = [
        ('color', 'ramp')
    ]

    def __init__(self, *args, **kwargs):
        super(SurfaceNodeOpt, self).__init__(*args, **kwargs)

    def to_scr_type_path(self):
        return '/nodes/shader/surface'


class SurfaceCreator(_base.AbsNodeCreator):
    """
    createAndAssignShader blinn "";
    """

    def __init__(self, *args, **kwargs):
        super(SurfaceCreator, self).__init__(*args, **kwargs)

    @qsm_mya_core.Undo.execute
    def do_create(self):
        result = qsm_mya_core.Shader.create_for(
            self._node_type, self._target_node_path, self._target_any_paths
        )
        return SurfaceNodeOpt(result)


class TextureNodeOpt(_base.AbsNodeOpt):
    SCHEME_BASE = '/node/texture'

    TYPE_INCLUDES = [
        'file',
        'cloth',
        'grid',
        'noise',
        'ramp',
        'checker',
        'bulge',
        'fractal',
        'mountain',
    ]

    DATA_KEY_INCLUDES = [
        _base.Util.DataKeys.Node,
        _base.Util.DataKeys.Sources
    ]

    SOURCE_ARGS = [
        ('uvCoord', 'place2dTexture')
    ]

    def __init__(self, *args, **kwargs):
        super(TextureNodeOpt, self).__init__(*args, **kwargs)

    def to_scr_type_path(self):
        return '/nodes/shader/texture'


class TextureCreator(_base.AbsNodeCreator):
    """
    createRenderNodeCB -as2DTexture "" ramp "";
    """

    def __init__(self, *args, **kwargs):
        super(TextureCreator, self).__init__(*args, **kwargs)
