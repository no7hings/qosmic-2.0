# coding:utf-8
import qsm_maya.core as qsm_mya_core

from . import node_for_dynamic as _node_for_dynamic

from . import base as _base

from . import node_for_any as _node_for_any

from . import node_for_locator as _node_for_locator

from . import node_for_look as _node_for_look

from . import node_graph_for_any as _node_graph_for_any


class BaseGenerator(object):
    SHAPE_EXTEND_TYPES = [
        'nurbsCurve',
        'nurbsSurface',
        'mesh',
    ]

    @classmethod
    def generate_node_graph_opt(cls, node_paths):
        return _node_graph_for_any.AnyNodeGraphOpt(node_paths)


class DynamicGenerator(BaseGenerator):
    SHAPE_EXTEND_TYPES = [
        'nurbsCurve',
        'nurbsSurface',
        'mesh',
    ]

    @classmethod
    def generate_node_opt(cls, node_path):
        # transform
        if qsm_mya_core.Transform.check_is_transform(node_path) is True:
            shape_path = qsm_mya_core.Transform.get_shape(node_path)
            shape_type = qsm_mya_core.Node.get_type(shape_path)
            return cls._generate_for_shape(shape_type, shape_path)
        # shape
        elif qsm_mya_core.Shape.check_is_shape(node_path) is True:
            shape_path = qsm_mya_core.DagNode.to_path(node_path)
            shape_type = qsm_mya_core.Node.get_type(node_path)
            return cls._generate_for_shape(shape_type, shape_path)
        # other
        node_path = qsm_mya_core.DagNode.to_path(node_path)
        node_type = qsm_mya_core.Node.get_type(node_path)
        return cls._generate_for_node(node_type, node_path)

    @classmethod
    def generate_node_graph_opt(cls, node_paths):
        return _node_graph_for_any.AnyNodeGraphOpt(node_paths)

    @classmethod
    def generate_node_opts(cls, paths, scheme):
        list_ = []
        for i_path in paths:
            i_opt = cls.generate_node_opt(i_path)
            if i_opt:
                if scheme.startswith(i_opt.SCHEME_BASE):
                    list_.append(i_opt)
        return list_

    @classmethod
    def _generate_for_shape(cls, shape_type, shape_path):
        if _node_for_dynamic.NonLinearShapeOpt.check_is_valid(shape_type) is True:
            return _node_for_dynamic.NonLinearShapeOpt(shape_path)
        elif _node_for_dynamic.NucleusShapeOpt.check_is_valid(shape_type) is True:
            return _node_for_dynamic.NucleusShapeOpt(shape_path)
        return cls._generate_for_shape_extend_as_node(shape_type, shape_path)

    @classmethod
    def _generate_for_shape_extend_as_node(cls, shape_type, shape_path):
        # do not use elif
        if shape_type in _node_for_dynamic.NonLinearShapeOpt.TARGET_TYPE_INCLUDES:
            _ = qsm_mya_core.NonLinear.find_any_from(shape_path)
            if _:
                return _node_for_dynamic.NonLinearShapeOpt(_)
        #
        if shape_type in _node_for_dynamic.NucleusShapeOpt.TARGET_TYPE_INCLUDES:
            _ = qsm_mya_core.RebuildForNucleus.find_any_from(shape_path)
            if _:
                return _node_for_dynamic.NucleusShapeOpt(_)

    @classmethod
    def _generate_for_node(cls, node_type, node_path):
        if _node_for_dynamic.FieldOpt.check_is_valid(node_type) is True:
            return _node_for_dynamic.FieldOpt(node_path)

    @classmethod
    def generate_node_creators(cls, path_map, scheme):
        list_ = []
        for i_path, i_any_paths in path_map.items():
            i_creator = cls.generate_node_creator(i_path, i_any_paths, scheme)
            if i_creator:
                list_.append(i_creator)
        return list_

    @classmethod
    def generate_node_creator(cls, node_path, any_paths, scheme):
        if qsm_mya_core.Transform.check_is_transform(node_path) is True:
            shape_path = qsm_mya_core.Transform.get_shape(node_path)
            shape_type = qsm_mya_core.Node.get_type(shape_path)
            return cls._generate_node_creator_for_shape_extend(shape_path, shape_type, any_paths, scheme)
        elif qsm_mya_core.Shape.check_is_shape(node_path) is True:
            shape_path = qsm_mya_core.DagNode.to_path(node_path)
            shape_type = qsm_mya_core.Node.get_type(node_path)
            return cls._generate_node_creator_for_shape_extend(shape_path, shape_type, any_paths, scheme)

    @classmethod
    def _generate_node_creator_for_shape_extend(cls, shape_path, shape_type, any_paths, scheme):
        if scheme.startswith(
            _node_for_dynamic.NonLinearShapeOpt.SCHEME_BASE
        ):
            if shape_type in _node_for_dynamic.NonlinearCreator.TARGET_TYPE_INCLUDES:
                return _node_for_dynamic.NonlinearCreator(shape_path, any_paths, scheme)
        elif scheme.startswith(
            _node_for_dynamic.NucleusShapeOpt.SCHEME_BASE
        ):
            if shape_type in _node_for_dynamic.NucleusCreator.TARGET_TYPE_INCLUDES:
                return _node_for_dynamic.NucleusCreator(shape_path, any_paths, scheme)


class LookGenerator(BaseGenerator):
    @classmethod
    def generate_node_opt(cls, node_path):
        # transform
        if qsm_mya_core.Transform.check_is_transform(node_path) is True:
            shape_path = qsm_mya_core.Transform.get_shape(node_path)
            shape_type = qsm_mya_core.Node.get_type(shape_path)
            return cls._generate_for_shape_extend(shape_type, shape_path)
        # shape
        elif qsm_mya_core.Shape.check_is_shape(node_path) is True:
            shape_path = qsm_mya_core.DagNode.to_path(node_path)
            shape_type = qsm_mya_core.Node.get_type(node_path)
            return cls._generate_for_shape_extend(shape_type, shape_path)
        # other
        node_path = qsm_mya_core.DagNode.to_path(node_path)
        node_type = qsm_mya_core.Node.get_type(node_path)
        return cls._generate_for_node(node_type, node_path)

    @classmethod
    def generate_node_opts(cls, paths, scheme):
        list_ = []
        for i_path in paths:
            i_opt = cls.generate_node_opt(i_path)
            if i_opt:
                if i_opt.get_scheme() == scheme:
                    list_.append(i_opt)
        return list_

    @classmethod
    def _generate_for_shape_extend(cls, shape_type, shape_path):
        if shape_type == 'mesh':
            materials = qsm_mya_core.Geometry.get_materials(shape_path)
            if materials:
                surface_shader = qsm_mya_core.Material.get_surface_shader(materials[0])
                if surface_shader:
                    return _node_for_look.SurfaceNodeOpt(surface_shader)

    @classmethod
    def _generate_for_node(cls, node_type, node_path):
        if _node_for_look.SurfaceNodeOpt.check_is_valid(node_type) is True:
            return _node_for_look.SurfaceNodeOpt(node_path)
        elif _node_for_look.TextureNodeOpt.check_is_valid(node_type) is True:
            return _node_for_look.TextureNodeOpt(node_path)

    @classmethod
    def generate_node_creators(cls, path_map, scheme):
        list_ = []
        for i_path, i_any_paths in path_map.items():
            i_creator = cls.generate_node_creator(i_path, i_any_paths, scheme)
            if i_creator:
                list_.append(i_creator)
        return list_

    @classmethod
    def generate_node_creator(cls, node_path, any_paths, scheme):
        if qsm_mya_core.Transform.check_is_transform(node_path) is True:
            shape_path = qsm_mya_core.Transform.get_shape(node_path)
            shape_type = qsm_mya_core.Node.get_type(shape_path)
            return cls._generate_node_creator_for_shape_extend(shape_path, shape_type, any_paths, scheme)
        elif qsm_mya_core.Shape.check_is_shape(node_path) is True:
            shape_path = qsm_mya_core.DagNode.to_path(node_path)
            shape_type = qsm_mya_core.Node.get_type(node_path)
            return cls._generate_node_creator_for_shape_extend(shape_path, shape_type, any_paths, scheme)

    @classmethod
    def _generate_node_creator_for_shape_extend(cls, shape_path, shape_type, any_paths, scheme):
        if scheme.startswith(
            _node_for_look.SurfaceNodeOpt.SCHEME_BASE
        ):
            if shape_type in {
                'mesh',
            }:
                return _node_for_look.SurfaceCreator(shape_path, any_paths, scheme)


class MotionGenerator(BaseGenerator):
    @classmethod
    def generate_node_opt(cls, node_path, data_type='node'):
        pass


class SceneGenerator(BaseGenerator):
    @classmethod
    def generate_node_opt(cls, node_path, data_type='node'):
        pass
