# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _task


class Asset(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Asset
    VariantKey = _cor_base.EntityVariantKeys.Asset

    TasksGeneratorCls = _task.TasksGenerator

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return _cor_base.EntityVariantKeyFnc.match_fnc(variants, cls.VariantKey)

    def __init__(self, *args, **kwargs):
        super(Asset, self).__init__(*args, **kwargs)


class AssetsGenerator(_base.AbsEntitiesGenerator):
    EntityCls = Asset

    def __init__(self, *args, **kwargs):
        super(AssetsGenerator, self).__init__(*args, **kwargs)
