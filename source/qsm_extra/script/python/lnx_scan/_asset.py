# coding:utf-8
from . import _base

from . import _task


class Asset(_base.AbsEntity):
    Type = _base.EntityTypes.Asset
    VariantKey = _base.EntityVariantKeys.Asset

    TasksCacheOptClass = _task.TasksCacheOpt

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return _base.VariantKeyMatch.match_fnc(
            variants, cls.VariantKey
        )

    def __init__(self, *args, **kwargs):
        super(Asset, self).__init__(*args, **kwargs)


class AssetsCacheOpt(_base.AbsEntitiesCacheOpt):
    EntityClass = Asset

    def __init__(self, *args, **kwargs):
        super(AssetsCacheOpt, self).__init__(*args, **kwargs)
