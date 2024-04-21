# coding:utf-8
from . import base as _base

from . import task as _task


class Sequence(_base.AbsEntity):
    Type = _base.EntityTypes.Sequence
    VariantKey = _base.VariantKeys.Sequence

    TaskQueryClass = _task.TaskQuery

    def __init__(self, *args, **kwargs):
        super(Sequence, self).__init__(*args, **kwargs)


class SequenceQuery(_base.AbsEntityQuery):
    EntityClass = Sequence

    def __init__(self, *args, **kwargs):
        super(SequenceQuery, self).__init__(*args, **kwargs)