# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _sequence

from . import _shot

from . import _task


class Episode(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Episode
    VariantKey = _cor_base.EntityVariantKeys.Episode

    NextEntitiesGeneratorClsDict = {
        _cor_base.EntityTypes.Sequence: _sequence.SequencesGenerator,
        _cor_base.EntityTypes.Shot: _shot.ShotsGenerator,
    }

    TasksGeneratorCls = _task.TasksGenerator

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return _cor_base.EntityVariantKeyFnc.match_fnc(variants, cls.VariantKey)

    def __init__(self, *args, **kwargs):
        super(Episode, self).__init__(*args, **kwargs)

    # sequence
    @_base.EntityFactory.find_all(_cor_base.EntityTypes.Sequence)
    def sequences(self, **kwargs):
        pass

    @_base.EntityFactory.find_one(_cor_base.EntityTypes.Sequence)
    def sequence(self, name, **kwargs):
        pass

    # shot
    @_base.EntityFactory.find_all(_cor_base.EntityTypes.Shot)
    def shots(self, **kwargs):
        pass

    @_base.EntityFactory.find_one(_cor_base.EntityTypes.Shot)
    def shot(self, name, **kwargs):
        pass


class EpisodesGenerator(_base.AbsEntitiesGenerator):
    EntityClass = Episode

    def __init__(self, *args, **kwargs):
        super(EpisodesGenerator, self).__init__(*args, **kwargs)
