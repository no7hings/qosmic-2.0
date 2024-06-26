# coding:utf-8
from . import base as _base

from . import task as _task


class TaskPool(_base.AbsEntityPool):
    LOCATION_PTN = 'Z:/caches/database/prc-task/{user_name}/tasks'

    CACHE = None

    CACHE_CLS = _task.TasksCache

    def __init__(self, location):
        super(TaskPool, self).__init__(location)
