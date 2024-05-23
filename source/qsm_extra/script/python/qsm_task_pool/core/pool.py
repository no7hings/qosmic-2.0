# coding:utf-8
from . import base as _base

from . import task as _task


class Pool(object):
    CACHE = None

    @classmethod
    def generate(cls):
        if cls.CACHE is not None:
            return _base.Util.CACHE
        _ = cls(
            'Z:/caches/database/prc-task/{}'.format(
                _base.Util.get_user_name()
            )
        )
        _base.Util.CACHE = _
        return _

    def __init__(self, location):
        self._location = location

        self._tasks_cache = _task.TasksCache(self)

    def __str__(self):
        return '{}(location="{}")'.format(
            self.__class__.__name__, self._location
        )

    def __repr__(self):
        return self.__str__()

    @property
    def location(self):
        return self._location
    
    def do_update(self):
        return self._tasks_cache.do_update()

    def get_task_ids(self):
        return self._tasks_cache.get_task_ids()

    def find_tasks(self, task_ids):
        return self._tasks_cache.find_tasks(task_ids)

    def get_tasks(self):
        return self._tasks_cache.get_tasks()

    def find_task(self, task_id):
        return self._tasks_cache.find_task(task_id)

    def new_task(self, group, name, cmd_script, completion_notice=None):
        return self._tasks_cache.new_task(
            group, name, cmd_script, completion_notice
        )

    def update_task_status(self, task_id, status):
        pass
