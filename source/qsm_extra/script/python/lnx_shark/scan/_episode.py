# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _sequence

from . import _shot

from . import _task


class Episode(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Episode
    VariantKey = _cor_base.EntityVariantKeys.Episode

    NextEntitiesCacheClassDict = {
        _cor_base.EntityTypes.Sequence: _sequence.SequencesGenerator,
        _cor_base.EntityTypes.Shot: _shot.ShotsGenerator,
    }

    TasksGeneratorClass = _task.TasksGenerator

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return _cor_base.EntityVariantKeyFnc.match_fnc(variants, cls.VariantKey)

    def __init__(self, *args, **kwargs):
        super(Episode, self).__init__(*args, **kwargs)

    def _find_sequences(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_cor_base.EntityTypes.Sequence, variants_extend, cache_flag)

    def sequences(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_sequences(variants_extend=kwargs, cache_flag=cache_flag)

    def _find_shots(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_cor_base.EntityTypes.Shot, variants_extend, cache_flag)

    def shots(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_shots(variants_extend=kwargs, cache_flag=cache_flag)


class EpisodesGenerator(_base.AbsEntitiesGenerator):
    EntityClass = Episode

    def __init__(self, *args, **kwargs):
        super(EpisodesGenerator, self).__init__(*args, **kwargs)
