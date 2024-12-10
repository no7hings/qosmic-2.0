# coding:utf-8
import _base

import _task


class Shot(_base.AbsEntity):
    Type = _base.EntityTypes.Shot
    VariantKey = _base.EntityVariantKeys.Shot

    TasksCacheOptClass = _task.TasksCacheOpt

    @classmethod
    def _variant_validation_fnc(cls, variants):
        # episode maybe unused
        if _base.EntityVariantKeys.Episode in variants:
            return (
                _base.VariantKeyMatch.match_fnc(variants, _base.EntityVariantKeys.Episode) and
                _base.VariantKeyMatch.match_fnc(variants, _base.EntityVariantKeys.Sequence) and
                _base.VariantKeyMatch.match_fnc(variants, cls.VariantKey)
            )
        return (
            _base.VariantKeyMatch.match_fnc(variants, _base.EntityVariantKeys.Sequence) and
            _base.VariantKeyMatch.match_fnc(variants, cls.VariantKey)
        )

    def __init__(self, *args, **kwargs):
        super(Shot, self).__init__(*args, **kwargs)


class ShotsCacheOpt(_base.AbsEntitiesCacheOpt):
    EntityClass = Shot

    def __init__(self, *args, **kwargs):
        super(ShotsCacheOpt, self).__init__(*args, **kwargs)
