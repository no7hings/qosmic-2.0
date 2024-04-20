# coding:utf-8
from . import base as _base

from . import step as _step


class Shot(_base.AbsEntity):
    Type = _base.EntityTypes.Shot
    VariantKey = _base.VariantKeys.Sequence

    StepQueryClass = _step.StepQuery

    def __init__(self, *args, **kwargs):
        super(Shot, self).__init__(*args, **kwargs)


class ShotQuery(_base.AbsEntityQuery):
    EntityClass = Shot

    def __init__(self, *args, **kwargs):
        super(ShotQuery, self).__init__(*args, **kwargs)
