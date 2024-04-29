# coding:utf-8
import os

import uuid

import lxbasic.content as bsc_content

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from . import base as _base


class Task(object):
    class PropertyKeys(object):
        ID = 'id'
        BatchName = 'batch_name'
        Name = 'name'
        Time = 'time'
        UtcTime = 'utc_time'

        HostName = 'host_name'
        UserName = 'user_name'

    class ProcessKeys(object):
        Status = 'status'
        SubmitTime = 'submit_time'
        StartTime = 'start_time'
        FinishTime = 'finish_time'

        Priority = 'priority'
        CmdScript = 'cmd_script'

    def __init__(self, tasks_index, task_id):
        self._tasks_index = tasks_index
        self._task_id = task_id
        self._location = '{}/{}.task'.format(
            self._tasks_index.location, self._task_id
        )
        self._json_location = '{}/task.json'.format(
            self._location
        )
        self._json_content = bsc_content.Content(
            key=None, value=self._json_location
        )

    def __str__(self):
        return '{}(id="{}")'.format(
            self.__class__.__name__,
            self._task_id
        )

    def __repr__(self):
        return self.__str__()

    @property
    def task_id(self):
        return self._task_id

    @property
    def name(self):
        return self._json_content.get('properties.name')

    @property
    def batch_name(self):
        return self._json_content.get('properties.batch_name')

    @property
    def content(self):
        return self._json_content

    @classmethod
    def create(cls, tasks_index, task_id, batch_name, name, cmd_script):
        location = '{}/{}.task'.format(
            tasks_index.location, task_id
        )
        json_location = '{}/task.json'.format(
            location
        )
        if os.path.isfile(json_location) is False:
            bsc_content.ContentFile(
                json_location
            ).write(
                {
                    'properties': {
                        cls.PropertyKeys.ID: task_id,
                        cls.PropertyKeys.BatchName: batch_name,
                        cls.PropertyKeys.Name: name,

                        cls.PropertyKeys.Time: _base.Util.get_time(),
                        cls.PropertyKeys.UtcTime: _base.Util.get_utc_time(),

                        cls.PropertyKeys.HostName: _base.Util.get_host_name(),
                        cls.PropertyKeys.UserName: _base.Util.get_user_name(),
                    },
                    'process': {
                        cls.ProcessKeys.Status: int(bsc_core.BscStatus.Waiting),
                        cls.ProcessKeys.SubmitTime: _base.Util.get_time(),
                        cls.ProcessKeys.StartTime: '',
                        cls.ProcessKeys.FinishTime: '',

                        cls.ProcessKeys.Priority: 50,
                        cls.ProcessKeys.CmdScript: cmd_script
                    }
                }

            )
        return cls(tasks_index, task_id)

    def do_update(self):
        self._json_content.reload()

    def update_status(self, status):
        pass

    def get_status(self):
        return self._json_content.get('process.status')

    def accept(self):
        self._json_content.save()


class TasksIndex(object):
    def __init__(self, connection, date_tag):
        self._connection = connection

        self._location = '{}/{}.tasks'.format(
            self._connection.location, date_tag
        )
        self._json_location = '{}/tasks.json'.format(
            self._location
        )
        if os.path.isfile(self._json_location) is False:
            bsc_content.ContentFile(
                self._json_location
            ).write(
                dict(
                    properties=dict(
                        utc_time=_base.Util.get_utc_time(),
                        time=_base.Util.get_time(),
                    ),
                    tasks=dict()
                )
            )

        self._json_content = bsc_content.Content(
            key=None, value=self._json_location
        )

        self._task_dict = {}
        self._task_index_dict = {}

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
        self._task_dict = {}
        self._task_index_dict = {}
        for i_task_id in self.get_task_ids():
            i_index = self.get_task_index(i_task_id)
            i_task = Task(self, i_task_id)
            self._task_index_dict[i_task_id] = i_index
            self._task_dict[i_task_id] = i_task

    def new_task(self, batch_name, name, cmd_script):
        task_id = _base.Util.new_uuid()
        # task_id = '26732170-051B-11EF-A9F6-4074E0DA267B'
        if self.exists_task(task_id) is False:
            task = Task.create(self, task_id, batch_name, name, cmd_script)
            index = len(self.get_task_ids())
            self._json_content.set(
                'tasks.{}'.format(task_id),
                dict(
                    index=index
                )
            )
            self.accept()
        else:
            task = Task(self, task_id)

        return task

    def get_task_ids(self):
        return self._json_content.get_key_names_at('tasks')

    def get_task_index(self, task_id):
        return self._json_content.get(
            'tasks.{}.index'.format(task_id)
        )

    def exists_task(self, task_id):
        return self._json_content.get_key_is_exists(
            'tasks.{}'.format(task_id)
        )

    def get_task(self, task_id):
        return self._task_dict[task_id]

    def get_tasks(self):
        self.do_update()
        _ = self._task_dict.values()
        _.sort(key=lambda x: self._task_index_dict[x.task_id])
        return _

    def accept(self):
        self._json_content.save()

