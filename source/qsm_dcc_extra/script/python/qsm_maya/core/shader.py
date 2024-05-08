# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ShaderCategory(object):
    CACHE = {}

    @classmethod
    def create_cache(cls):
        if not cls.CACHE:
            # custom
            for i_category in ['shader', 'texture', 'light', 'utility']:
                for j_type in cmds.listNodeTypes(i_category) or []:
                    cls.CACHE[j_type] = i_category

    @classmethod
    def get(cls, type_name, default='unknown'):
        cls.create_cache()
        return cls.CACHE.get(type_name, default)

    @classmethod
    def is_shader_type(cls, type_name):
        cls.create_cache()
        return type_name in cls.CACHE


class Shader(object):
    @classmethod
    def create(cls, name, type_name):
        if cmds.objExists(name) is True:
            return name
        category = ShaderCategory.get(type_name, 'utility')
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
