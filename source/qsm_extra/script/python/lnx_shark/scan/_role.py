# coding:utf-8
from . import _base

from . import _asset

from . import _task


class Role(_base.AbsEntity):
    Type = _base.EntityTypes.Role
    VariantKey = _base.EntityVariantKeys.Role

    NextEntitiesCacheClassDict = {
        _base.EntityTypes.Asset: _asset.AssetsGenerator,
    }

    TasksGeneratorClass = _task.TasksGenerator

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return _base.VariantKeyMatch.match_fnc(variants, cls.VariantKey)

    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)

    def find_assets(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Asset, variants_extend, cache_flag)

    def assets(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_assets(variants_extend=kwargs, cache_flag=cache_flag)


class RolesGenerator(_base.AbsEntitiesGenerator):
    EntityClass = Role

    def __init__(self, *args, **kwargs):
        super(RolesGenerator, self).__init__(*args, **kwargs)
