# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _asset

from . import _task


class Role(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Role
    VariantKey = _cor_base.EntityVariantKeys.Role

    NextEntitiesGeneratorClsDict = {
        _cor_base.EntityTypes.Asset: _asset.AssetsGenerator,
    }

    TasksGeneratorCls = _task.TasksGenerator

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return _cor_base.EntityVariantKeyFnc.match_fnc(variants, cls.VariantKey)

    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)

    # asset
    @_base.EntityFactory.find_all(_cor_base.EntityTypes.Asset)
    def assets(self, **kwargs):
        pass

    @_base.EntityFactory.find_one(_cor_base.EntityTypes.Asset)
    def asset(self, name, **kwargs):
        pass


class RolesGenerator(_base.AbsEntitiesGenerator):
    EntityCls = Role

    def __init__(self, *args, **kwargs):
        super(RolesGenerator, self).__init__(*args, **kwargs)
