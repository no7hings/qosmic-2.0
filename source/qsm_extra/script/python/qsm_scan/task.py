# coding:utf-8
from . import base as _base


class Task(_base.AbsTask):
    Type = _base.EntityTypes.Task
    VariantKey = _base.VariantKeys.Task

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)


class TasksCache(_base.AbsTaskQuery):
    EntityClass = Task

    def __init__(self, *args, **kwargs):
        super(TasksCache, self).__init__(*args, **kwargs)
