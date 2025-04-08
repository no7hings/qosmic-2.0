# coding:utf-8
import lxbasic.pinyin as bsc_pinyin

from ..core import base as _cor_base

from . import _base

from . import _shot

from . import _task


class Sequence(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Sequence
    VariantKey = _cor_base.EntityVariantKeys.Sequence

    NextEntitiesCacheClassDict = {
        _cor_base.EntityTypes.Shot: _shot.ShotsGenerator,
    }

    TasksGeneratorClass = _task.TasksGenerator

    @classmethod
    def _variant_validation_fnc(cls, variants):
        # maybe episode is unused
        if _cor_base.EntityVariantKeys.Episode in variants:
            return (
                _cor_base.EntityVariantKeyFnc.match_fnc(variants, _cor_base.EntityVariantKeys.Episode) and
                _cor_base.EntityVariantKeyFnc.match_fnc(variants, cls.VariantKey)
            )
        return _cor_base.EntityVariantKeyFnc.match_fnc(variants, cls.VariantKey)

    def __init__(self, *args, **kwargs):
        super(Sequence, self).__init__(*args, **kwargs)

    def _find_shots(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_cor_base.EntityTypes.Shot, variants_extend, cache_flag)

    def shots(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_shots(variants_extend=kwargs, cache_flag=cache_flag)


class SequencesGenerator(_base.AbsEntitiesGenerator):
    EntityClass = Sequence

    def __init__(self, *args, **kwargs):
        super(SequencesGenerator, self).__init__(*args, **kwargs)
