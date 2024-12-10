# coding:utf-8
import _base


class Task(_base.AbsTask):
    Type = _base.EntityTypes.Task
    VariantKey = _base.EntityVariantKeys.Task

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)


class TasksCacheOpt(_base.AbsTasksCacheOpt):
    EntityClass = Task

    def __init__(self, *args, **kwargs):
        super(TasksCacheOpt, self).__init__(*args, **kwargs)
