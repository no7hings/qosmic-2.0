# coding:utf-8
from . import base as _base

from . import task as _task


class Sequence(_base.AbsEntity):
    Type = _base.EntityTypes.Sequence
    VariantKey = _base.VariantKeys.Sequence

    TaskQueryClass = _task.TasksCache

    def __init__(self, *args, **kwargs):
        super(Sequence, self).__init__(*args, **kwargs)


class SequencesCache(_base.AbsEntitiesCache):
    EntityClass = Sequence

    def __init__(self, *args, **kwargs):
        super(SequencesCache, self).__init__(*args, **kwargs)