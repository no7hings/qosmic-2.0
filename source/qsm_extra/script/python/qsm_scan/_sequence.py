# coding:utf-8
import lxbasic.pinyin as bsc_pinyin

import _base

import _shot

import _task


class Sequence(_base.AbsEntity):
    Type = _base.EntityTypes.Sequence
    VariantKey = _base.EntityVariantKeys.Sequence

    NextEntitiesCacheClassDict = {
        _base.EntityTypes.Shot: _shot.ShotsCacheOpt,
    }

    TasksCacheOptClass = _task.TasksCacheOpt
    
    @classmethod
    def _variant_cleanup_fnc(cls, variants):
        # todo: cleanup name?
        name = variants[cls.VariantKey]
        variants[cls.VariantKey] = bsc_pinyin.Text.cleanup(name)
        return variants

    @classmethod
    def _variant_validation_fnc(cls, variants):
        # maybe episode is unused
        if _base.EntityVariantKeys.Episode in variants:
            return (
                _base.VariantKeyMatch.match_fnc(variants, _base.EntityVariantKeys.Episode) and
                _base.VariantKeyMatch.match_fnc(variants, cls.VariantKey)
            )
        return _base.VariantKeyMatch.match_fnc(variants, cls.VariantKey)

    def __init__(self, *args, **kwargs):
        super(Sequence, self).__init__(*args, **kwargs)

    def find_shots(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Shot, variants_extend, cache_flag)


class SequencesCacheOpt(_base.AbsEntitiesCacheOpt):
    EntityClass = Sequence

    def __init__(self, *args, **kwargs):
        super(SequencesCacheOpt, self).__init__(*args, **kwargs)
