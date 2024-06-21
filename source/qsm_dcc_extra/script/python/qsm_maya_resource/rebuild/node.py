# coding:utf-8
import collections

import sys

import qsm_maya.core as qsm_mya_core


__all__ = [
    'Generator'
]


class Generator(object):

    SHAPE_EXTEND_TYPES = [
        'nurbsCurve',
        'nurbsSurface',
        'mesh',
    ]

    def __init__(self, path):
        self._node_path = path
        self._node_opt_list = qsm_mya_core.BscNodeOpt(path)

    @classmethod
    def get_node_properties(cls, path, includes=None):
        if path is None:
            raise RuntimeError()

        if qsm_mya_core.Node.is_exists(path) is False:
            raise RuntimeError()

        node_opt = qsm_mya_core.BscNodeOpt(path)
        if isinstance(includes, (tuple, list)):
            _ = includes
        else:
            _ = node_opt.get_all_port_paths()
        return node_opt.get_node_properties(includes=_)

    @classmethod
    def apply_node_properties(cls, path, data, *args, **kwargs):
        if path is None:
            raise RuntimeError()

        if qsm_mya_core.Node.is_exists(path) is False:
            raise RuntimeError()

        node_opt = qsm_mya_core.BscNodeOpt(path)
        node_opt.apply_node_properties(
            data, *args, **kwargs
        )

    @classmethod
    def generate_one(cls, node_path, search_scheme='default'):
        # transform
        if qsm_mya_core.Transform.check_is_transform(node_path) is True:
            if search_scheme == 'default':
                # constrain
                transform_path = qsm_mya_core.DagNode.to_path(node_path)
                opt = cls._generate_for_transform(transform_path)
                if opt:
                    return opt

            shape_path = qsm_mya_core.Transform.get_shape(node_path)
            shape_type = qsm_mya_core.Node.get_type(shape_path)
            return cls._generate_for_shape(shape_type, shape_path, search_scheme)
        # shape
        elif qsm_mya_core.Shape.check_is_shape(node_path) is True:
            shape_path = qsm_mya_core.DagNode.to_path(node_path)
            shape_type = qsm_mya_core.Node.get_type(node_path)
            return cls._generate_for_shape(shape_type, shape_path, search_scheme)
        # other
        else:
            node_path = qsm_mya_core.DagNode.to_path(node_path)
            node_type = qsm_mya_core.Node.get_type(node_path)
            return cls._generate_for_node(node_type, node_path)

    @classmethod
    def generate_all(cls, paths, scheme, search_scheme='default'):
        list_ = []
        for i_path in paths:
            i_opt = cls.generate_one(i_path, search_scheme)
            if i_opt:
                if i_opt.get_scheme() == scheme:
                    list_.append(i_opt)
        return list_

    @classmethod
    def _generate_for_transform(cls, transform_path):
        node_type = 'motionPath'
        _ = qsm_mya_core.NodeAttribute.get_source_node(
            transform_path, 'specifiedManipLocation', node_type
        )
        if _:
            node_path = _
            return AnyNodeOpt(node_path)
        return None

    @classmethod
    def _generate_for_node(cls, node_type, node_path):
        if node_type in SurfaceNodeOpt.TYPE_INCLUDES:
            return SurfaceNodeOpt(node_path)
        elif node_type in TextureNodeOpt.TYPE_INCLUDES:
            return TextureNodeOpt(node_path)
        elif node_type in XformNodeOpt.TYPE_INCLUDES:
            return XformNodeOpt(node_path)
        elif node_type in AnyNodeOpt.TYPE_INCLUDES:
            return AnyNodeOpt(node_path)

    @classmethod
    def _generate_for_shape(cls, shape_type, shape_path, search_scheme):
        if shape_type in NonLinearShapeOpt.TYPE_INCLUDES:
            return NonLinearShapeOpt(shape_path)
        elif shape_type in NucleusShapeOpt.TYPE_INCLUDES:
            return NucleusShapeOpt(shape_path)
        elif shape_type in cls.SHAPE_EXTEND_TYPES:
            return cls._generate_for_shape_extend(shape_type, shape_path, search_scheme)
        return None

    @classmethod
    def _generate_for_shape_extend(cls, shape_type, shape_path, search_scheme):
        if shape_type == 'mesh':
            # deform
            if search_scheme == 'default':
                # source
                _ = qsm_mya_core.NodeAttribute.get_source_node(
                    shape_path, 'inMesh'
                )
                if _:
                    node_path = _
                    node_type = qsm_mya_core.Node.get_type(node_path)
                    if node_type == 'nonLinear':
                        handle_shape_path = qsm_mya_core.NodeAttribute.get_source_node(
                            node_path, 'deformerData'
                        )
                        if handle_shape_path:
                            return NonLinearShapeOpt(handle_shape_path)
                    elif node_type == 'nCloth':
                        return NucleusShapeOpt(node_path)
                # target
                _ = qsm_mya_core.NodeAttribute.get_target_nodes(
                    shape_path, 'worldMesh'
                )
                if _:
                    node_path = _[0]
                    node_type = qsm_mya_core.Node.get_type(node_path)
                    if node_type == 'nRigid':
                        return NucleusShapeOpt(node_path)
            # shader
            elif search_scheme == 'shader':
                materials = qsm_mya_core.MeshOpt(shape_path).get_material_paths()
                if materials:
                    surface_shader = qsm_mya_core.Material.get_surface_shader(materials[0])
                    if surface_shader:
                        return SurfaceNodeOpt(surface_shader)

    @classmethod
    def generate_as_creator(cls, node_path, any_paths, scheme):
        if qsm_mya_core.Transform.check_is_transform(node_path) is True:
            shape_path = qsm_mya_core.Transform.get_shape(node_path)
            shape_type = qsm_mya_core.Node.get_type(shape_path)
            return cls._generate_creator_for_shape(shape_path, shape_type, any_paths, scheme)
        elif qsm_mya_core.Shape.check_is_shape(node_path) is True:
            shape_path = qsm_mya_core.DagNode.to_path(node_path)
            shape_type = qsm_mya_core.Node.get_type(node_path)
            return cls._generate_creator_for_shape(shape_path, shape_type, any_paths, scheme)
        else:
            pass

    @classmethod
    def generate_creators(cls, path_map, scheme):
        list_ = []
        for i_path, i_any_paths in path_map.items():
            i_creator = cls.generate_as_creator(i_path, i_any_paths, scheme)
            if i_creator:
                list_.append(i_creator)
        return list_

    @classmethod
    def _generate_creator_for_shape(cls, shape_path, shape_type, any_paths, scheme):
        if scheme.startswith(
            NonLinearShapeOpt.SCHEME_BASE
        ):
            if shape_type in {
                # 'nurbsCurve',
                # 'nurbsSurface',
                'mesh',
            }:
                return NonlinearCreator(shape_path, any_paths, scheme)
        elif scheme.startswith(
            SurfaceNodeOpt.SCHEME_BASE
        ):
            if shape_type in {
                'mesh',
            }:
                #
                return SurfaceCreator(shape_path, any_paths, scheme)


class _AbsNodeOpt(object):
    class DataKeys:
        Node = 'node'
        Transform = 'transform'
        Sources = 'sources'
        Targets = 'targets'

    SCHEME_BASE = '/node'

    SCR_TYPE_PATH_MAPPER = dict(
        # deform
        deformBend='/deformers/non_linear/bend',
        deformFlare='/deformers/non_linear/flare',
        deformSine='/deformers/non_linear/sine',
        deformSquash='/deformers/non_linear/squash',
        deformTwist='/deformers/non_linear/twist',
        deformWave='/deformers/non_linear/wave',
        # xform
        nucleus='/effects/nucleus/nucleus',
        airField='/effects/fields/air_field',
        dragField='/effects/fields/drag_field',
        gravityField='/effects/fields/gravity_field',
        newtonField='/effects/fields/newton_field',
        radialField='/effects/fields/radial_field',
        turbulenceField='/effects/fields/turbulence_field',
        uniformField='/effects/fields/uniform_field',
        vortexField='/effects/fields/vortex_field',
        # nucleus
        hairSystem='/effects/nucleus/n_hair',
        nCloth='/effects/nucleus/n_cloth',
        nRigid='/effects/nucleus/n_rigid',
        nParticle='/effects/nucleus/n_particle',
        # motion
        motionPath='/animation/constrains/motion_path',
    )

    DATA_KEY_INCLUDES = [
        DataKeys.Node
    ]

    TARGET_ARGS = [
    ]

    SOURCE_ARGS = [
    ]

    def __init__(self, node_path):
        self._node_path = node_path
        self._node_type = qsm_mya_core.Node.get_type(self._node_path)

        self._get_fnc_mapper = {
            self.DataKeys.Node: self.get_for_node,
            self.DataKeys.Transform: self.get_for_transform,
            self.DataKeys.Sources: self.get_for_sources,
            self.DataKeys.Targets: self.get_for_targets
        }
        self._apply_fnc_mapper = {
            self.DataKeys.Node: self.apply_for_node,
            self.DataKeys.Transform: self.apply_for_transform,
            self.DataKeys.Sources: self.apply_for_sources,
            self.DataKeys.Targets: self.apply_for_targets
        }

        sys.stdout.write('current is "{}:{}", scheme is "{}"\n'.format(
            self._node_type, self._node_path,
            self.get_scheme())
        )

    def get_scheme(self):
        return '{}/{}'.format(self.SCHEME_BASE, self._node_type)

    def get_for_transform(self):
        _ = qsm_mya_core.Shape.get_transform(self._node_path)
        if _:
            path = _
            return Generator.get_node_properties(path)

    def apply_for_transform(self, data, *args, **kwargs):
        _ = qsm_mya_core.Shape.get_transform(self._node_path)
        if _:
            path = _
            return Generator.apply_node_properties(path, data, *args, **kwargs)

    def get_for_sources(self):
        dict_ = {}
        for i in self.SOURCE_ARGS:
            i_atr_name, i_node_type = i
            i_key = '{}:{}'.format(*i)
            _ = qsm_mya_core.NodeAttribute.get_source_node(
                self._node_path, i_atr_name, i_node_type
            )
            if _:
                i_path = _
                dict_[i_key] = Generator.get_node_properties(i_path)
        return dict_

    def apply_for_sources(self, data, *args, **kwargs):
        for i_k, i_data in data.items():
            i_atr_name, i_node_type = i_k.split(':')
            _ = qsm_mya_core.NodeAttribute.get_source_node(
                self._node_path, i_atr_name, i_node_type
            )
            if _:
                i_path = _
                Generator.apply_node_properties(i_path, i_data, *args, **kwargs)

    def get_for_targets(self):
        dict_ = {}
        for i in self.TARGET_ARGS:
            i_atr_name, i_node_type = i
            i_key = '{}:{}'.format(*i)
            _ = qsm_mya_core.NodeAttribute.get_target_nodes(
                self._node_path, i_atr_name, i_node_type
            )
            if _:
                i_path = _[0]
                dict_[i_key] = Generator.get_node_properties(i_path)
        return dict_

    def apply_for_targets(self, data, *args, **kwargs):
        for i_k, i_data in data.items():
            i_atr_name, i_node_type = i_k.split(':')
            _ = qsm_mya_core.NodeAttribute.get_target_nodes(
                self._node_path, i_atr_name, i_node_type
            )
            if _:
                i_path = _[0]
                Generator.apply_node_properties(i_path, i_data, *args, **kwargs)

    def to_scr_type_path(self):
        if self._node_type in self.SCR_TYPE_PATH_MAPPER:
            return self.SCR_TYPE_PATH_MAPPER[self._node_type]
        return ''

    def get_for_node(self):
        path = self._node_path
        return Generator.get_node_properties(path)

    def apply_for_node(self, data, *args, **kwargs):
        Generator.apply_node_properties(self._node_path, data, *args, **kwargs)

    def get_data(self):
        data = collections.OrderedDict()
        for i_key in self.DATA_KEY_INCLUDES:
            i_fnc = self._get_fnc_mapper[i_key]
            i_data = i_fnc()
            if i_data:
                data[i_key] = i_fnc()
        return dict(
            scheme=self.get_scheme(),
            data=data
        )

    @qsm_mya_core.Undo.execute
    def apply_data(self, rebuild_data, frame_offset=0, force=True, excludes=None, key_includes=None):
        scheme = rebuild_data.get('scheme')
        if scheme == self.get_scheme():
            data = rebuild_data.get('data')
            if isinstance(key_includes, (tuple, list)):
                keys = key_includes
            else:
                keys = self.DATA_KEY_INCLUDES
            for i_key in keys:
                if i_key in data:
                    i_data = data[i_key]
                    i_fnc = self._apply_fnc_mapper[i_key]
                    i_fnc(i_data, frame_offset=frame_offset, force=force, excludes=excludes)


class _AbsNodeCreator(object):
    def __init__(self, node_path, any_paths, scheme):
        self._node_path = node_path
        self._any_paths = any_paths
        self._scheme = scheme
        self._node_type = self._scheme.split('/')[-1]

    @qsm_mya_core.Undo.execute
    def do_create(self):
        pass


class AnyNodeOpt(_AbsNodeOpt):
    TYPE_INCLUDES = [
        'motionPath'
    ]
    
    def __init__(self, *args, **kwargs):
        super(AnyNodeOpt, self).__init__(*args, **kwargs)


class SurfaceNodeOpt(_AbsNodeOpt):
    SCHEME_BASE = '/surface'

    TYPE_INCLUDES = [
        'lambert',
        'blinn',
        'phong',
    ]

    DATA_KEY_INCLUDES = [
        _AbsNodeOpt.DataKeys.Node,
        _AbsNodeOpt.DataKeys.Sources
    ]

    SOURCE_ARGS = [
        ('color', 'ramp')
    ]

    def __init__(self, *args, **kwargs):
        super(SurfaceNodeOpt, self).__init__(*args, **kwargs)

    def to_scr_type_path(self):
        return '/look/shader/surface'


class SurfaceCreator(_AbsNodeCreator):
    """
    createAndAssignShader blinn "";
    """
    def __init__(self, *args, **kwargs):
        super(SurfaceCreator, self).__init__(*args, **kwargs)

    @qsm_mya_core.Undo.execute
    def do_create(self):
        result = qsm_mya_core.Shader.create_for(
            self._node_type, self._node_path, self._any_paths
        )
        return SurfaceNodeOpt(result)


class TextureNodeOpt(_AbsNodeOpt):
    SCHEME_BASE = '/texture'

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
        _AbsNodeOpt.DataKeys.Node,
        _AbsNodeOpt.DataKeys.Sources
    ]

    SOURCE_ARGS = [
        ('uvCoord', 'place2dTexture')
    ]

    def __init__(self, *args, **kwargs):
        super(TextureNodeOpt, self).__init__(*args, **kwargs)

    def to_scr_type_path(self):
        return '/look/shader/texture'


class TextureCreator(_AbsNodeCreator):
    """
    createRenderNodeCB -as2DTexture "" ramp "";
    """
    def __init__(self, *args, **kwargs):
        super(TextureCreator, self).__init__(*args, **kwargs)


class _AbsShapeOpt(_AbsNodeOpt):
    SCHEME_BASE = '/shape'

    DATA_KEY_INCLUDES = [
        _AbsNodeOpt.DataKeys.Node,
        _AbsNodeOpt.DataKeys.Transform
    ]

    def __init__(self, *args, **kwargs):
        super(_AbsShapeOpt, self).__init__(*args, **kwargs)

    def find_transform(self):
        return qsm_mya_core.Shape.get_transform(self._node_path)


class AnyShapeOpt(_AbsShapeOpt):
    def __init__(self, *args, **kwargs):
        super(AnyShapeOpt, self).__init__(*args, **kwargs)


class NonLinearShapeOpt(_AbsShapeOpt):
    SCHEME_BASE = '/non_linear'

    TYPE_INCLUDES = [
        'deformBend',
        'deformFlare',
        'deformSine',
        'deformSquash',
        'deformTwist',
        'deformWave',
    ]

    DATA_KEY_INCLUDES = [
        _AbsNodeOpt.DataKeys.Node,
        _AbsNodeOpt.DataKeys.Transform,
        _AbsNodeOpt.DataKeys.Targets
    ]

    TARGET_ARGS = [
        ('deformerData', 'nonLinear')
    ]

    def __init__(self, *args, **kwargs):
        super(NonLinearShapeOpt, self).__init__(*args, **kwargs)


class NonlinearCreator(_AbsNodeCreator):
    KEY_MAPPER = dict(
        deformBend='bend',
        deformFlare='flare',
        deformSine='sine',
        deformSquash='squash',
        deformTwist='twist',
        deformWave='wave',
    )

    def __init__(self, *args, **kwargs):
        super(NonlinearCreator, self).__init__(*args, **kwargs)

    @qsm_mya_core.Undo.execute
    def do_create(self):
        result = qsm_mya_core.NonLinear.create_for(
            self.KEY_MAPPER[self._node_type], self._node_path, self._any_paths
        )
        if result is not None:
            return NonLinearShapeOpt(
                result
            )


class NucleusShapeOpt(_AbsShapeOpt):
    SCHEME_BASE = '/nucleus'

    TYPE_INCLUDES = [
        'hairSystem',
        'nCloth',
        'nRigid',
        'nParticle',
    ]

    DATA_KEY_INCLUDES = [
        _AbsNodeOpt.DataKeys.Node,
        _AbsNodeOpt.DataKeys.Transform,
        _AbsNodeOpt.DataKeys.Targets
    ]

    SOURCE_ARGS = [
        ('nextState', 'nucleus')
    ]

    def __init__(self, *args, **kwargs):
        super(NucleusShapeOpt, self).__init__(*args, **kwargs)


class XformNodeOpt(_AbsNodeOpt):
    TYPE_INCLUDES = [
        'nucleus',

        'airField',
        'dragField',
        'gravityField',
        'newtonField',
        'radialField',
        'turbulenceField',
        'uniformField',
        'vortexField',
    ]

    SCHEME_BASE = '/xform'

    def __init__(self, *args, **kwargs):
        super(XformNodeOpt, self).__init__(*args, **kwargs)
