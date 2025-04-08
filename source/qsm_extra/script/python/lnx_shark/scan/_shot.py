# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _task


class Shot(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Shot
    VariantKey = _cor_base.EntityVariantKeys.Shot

    TasksGeneratorClass = _task.TasksGenerator

    @classmethod
    def _variant_validation_fnc(cls, variants):
        # episode maybe unused
        if _cor_base.EntityVariantKeys.Episode in variants:
            return (
                _cor_base.EntityVariantKeyFnc.match_fnc(variants, _cor_base.EntityVariantKeys.Episode) and
                _cor_base.EntityVariantKeyFnc.match_fnc(variants, _cor_base.EntityVariantKeys.Sequence) and
                _cor_base.EntityVariantKeyFnc.match_fnc(variants, cls.VariantKey)
            )
        return (
            _cor_base.EntityVariantKeyFnc.match_fnc(variants, _cor_base.EntityVariantKeys.Sequence) and
            _cor_base.EntityVariantKeyFnc.match_fnc(variants, cls.VariantKey)
        )

    def __init__(self, *args, **kwargs):
        super(Shot, self).__init__(*args, **kwargs)


class ShotsGenerator(_base.AbsEntitiesGenerator):
    EntityClass = Shot

    def __init__(self, *args, **kwargs):
        super(ShotsGenerator, self).__init__(*args, **kwargs)
