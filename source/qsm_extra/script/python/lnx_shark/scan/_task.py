# coding:utf-8
from . import _base


class Task(_base.AbsTask):
    Type = _base.EntityTypes.Task
    VariantKey = _base.EntityVariantKeys.Task

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)


class TasksGenerator(_base.AbsTasksGenerator):
    EntityClass = Task

    def __init__(self, *args, **kwargs):
        super(TasksGenerator, self).__init__(*args, **kwargs)
