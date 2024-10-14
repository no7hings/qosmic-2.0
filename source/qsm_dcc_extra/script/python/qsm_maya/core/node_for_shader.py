# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from . import node_category as _node_category

from . import attribute as _attribute

from . import transform as _transform

from . import shape as _shape


class Shader(object):
    @classmethod
    def create(cls, name, type_name):
        if cmds.objExists(name) is True:
            return name

        category = _node_category.ShaderCategory.get(type_name, 'utility')
        kwargs = dict(
            name=name,
            skipSelect=1
        )
        if category == 'shader':
            kwargs['asShader'] = 1
        elif category == 'texture':
            kwargs['asTexture'] = 1
        elif category == 'light':
            kwargs['asLight'] = 1
        elif category == 'utility':
            kwargs['asUtility'] = 1

        _ = cmds.shadingNode(type_name, **kwargs)
        return _

    # fixme: component assign
    @classmethod
    def create_for(cls, shader_type, target_shape_path, target_any_paths):
        cmds.select(target_any_paths)

        if _transform.Transform.is_transform_type(target_shape_path):
            target_shape_path = _transform.Transform.get_shape(target_shape_path)

        mel_script = 'createAndAssignShader {} "";'.format(shader_type)
        mel.eval(mel_script)

        material_assign_map = _shape.Geometry.get_material_assign_map(target_shape_path)
        material = material_assign_map[target_any_paths[0]]

        shader = _attribute.NodeAttribute.get_source_node(
            material, 'surfaceShader', shader_type
        )
        return shader
