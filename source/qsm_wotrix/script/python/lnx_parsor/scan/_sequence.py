# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _shot

from . import _task


class Sequence(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Sequence
    VariantKey = _cor_base.EntityVariantKeys.Sequence

    NextEntitiesGeneratorClsDict = {
        _cor_base.EntityTypes.Shot: _shot.ShotsGenerator,
    }

    TasksGeneratorCls = _task.TasksGenerator

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

    @_base.EntityFactory.find_all(_cor_base.EntityTypes.Shot)
    def shots(self, **kwargs):
        pass

    @_base.EntityFactory.find_one(_cor_base.EntityTypes.Shot)
    def shot(self, name, **kwargs):
        pass


class SequencesGenerator(_base.AbsEntitiesGenerator):
    EntityClass = Sequence

    def __init__(self, *args, **kwargs):
        super(SequencesGenerator, self).__init__(*args, **kwargs)
