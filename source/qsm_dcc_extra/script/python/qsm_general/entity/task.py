# coding:utf-8
from . import base as _base


class Task(_base.AbsTask):
    Type = _base.EntityTypes.Task

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)


class TaskQuery(_base.AbsTaskQuery):
    EntityClass = Task

    def __init__(self, *args, **kwargs):
        super(TaskQuery, self).__init__(*args, **kwargs)
