# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node_category as _node_category


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
