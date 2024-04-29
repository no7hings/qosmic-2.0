# coding:utf-8
from . import base as _base

from . import task as _task


class Shot(_base.AbsEntity):
    Type = _base.EntityTypes.Shot
    VariantKey = _base.VariantKeys.Sequence

    TaskQueryClass = _task.TasksCache

    def __init__(self, *args, **kwargs):
        super(Shot, self).__init__(*args, **kwargs)


class ShotsCache(_base.AbsEntitiesCache):
    EntityClass = Shot

    def __init__(self, *args, **kwargs):
        super(ShotsCache, self).__init__(*args, **kwargs)
