# coding:utf-8
import _base

import _sequence

import _shot

import _task


class Episode(_base.AbsEntity):
    Type = _base.EntityTypes.Episode
    VariantKey = _base.VariantKeys.Episode

    NextEntitiesCacheClassDict = {
        _base.EntityTypes.Sequence: _sequence.SequencesCacheOpt,
        _base.EntityTypes.Shot: _shot.ShotsCacheOpt,
    }

    TasksCacheOptClass = _task.TasksCacheOpt

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return (
            _base.VariantKeyMatch.match_fnc(variants, _base.VariantKeys.Episode) and
            _base.VariantKeyMatch.match_fnc(variants, cls.VariantKey)
        )

    def __init__(self, *args, **kwargs):
        super(Episode, self).__init__(*args, **kwargs)

    def find_sequences(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Sequence, variants_extend, cache_flag)

    def find_shots(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Shot, variants_extend, cache_flag)


class EpisodesCacheOpt(_base.AbsEntitiesCacheOpt):
    EntityClass = Episode

    def __init__(self, *args, **kwargs):
        super(EpisodesCacheOpt, self).__init__(*args, **kwargs)
