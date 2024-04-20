# coding:utf-8
from . import base as _base

from . import step as _step


class Sequence(_base.AbsEntity):
    Type = _base.EntityTypes.Sequence
    VariantKey = _base.VariantKeys.Sequence

    StepQueryClass = _step.StepQuery

    def __init__(self, *args, **kwargs):
        super(Sequence, self).__init__(*args, **kwargs)


class SequenceQuery(_base.AbsEntityQuery):
    EntityClass = Sequence

    def __init__(self, *args, **kwargs):
        super(SequenceQuery, self).__init__(*args, **kwargs)