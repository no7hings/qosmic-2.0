# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ShaderCategory(object):
    CACHE = {}

    @classmethod
    def generate_cache(cls):
        if not cls.CACHE:
            # custom
            for i_category in ['shader', 'texture', 'light', 'utility']:
                for j_type in cmds.listNodeTypes(i_category) or []:
                    cls.CACHE[j_type] = i_category
        return cls.CACHE

    @classmethod
    def get(cls, type_name, default='unknown'):
        cls.generate_cache()
        return cls.CACHE.get(type_name, default)

    @classmethod
    def is_shader_type(cls, type_name):
        cls.generate_cache()
        return type_name in cls.CACHE
