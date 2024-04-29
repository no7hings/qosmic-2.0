# coding:utf-8
from . import base as _base

from . import task as _task


class Connection(object):
    CONNECTION = None

    @classmethod
    def generate(cls):
        if cls.CONNECTION is not None:
            return _base.Util.CONNECTION
        _ = cls(
            'Z:/caches/database/prc-task/{}'.format(
                _base.Util.get_user_name()
            )
        )
        _base.Util.CONNECTION = _
        return _

    def __init__(self, location):
        self._location = location

        self._date_tag_cur = _base.Util.get_date_tag()

        self._tasks_index_cur = _task.TasksIndex(self, self._date_tag_cur)

    def __str__(self):
        return '{}(location="{}")'.format(
            self.__class__.__name__, self._location
        )

    def __repr__(self):
        return self.__str__()

    @property
    def location(self):
        return self._location

    def get_tasks(self):
        return self._tasks_index_cur.get_tasks()

    def get_task(self, task_id):
        return self._tasks_index_cur.get_task(task_id)

    def new_task(self, batch_name, name, cmd_script):
        return self._tasks_index_cur.new_task(
            batch_name, name, cmd_script
        )

    def update_task_status(self, task_id, status):
        pass
