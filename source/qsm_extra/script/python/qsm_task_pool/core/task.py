# coding:utf-8
import os

import lxbasic.content as bsc_content

import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import lxbasic.storage as bsc_storage

from . import base as _base


class Task(object):
    class PropertyKeys(object):
        ID = 'id'
        Group = 'group'
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
        self._tasks_cache = tasks_index
        self._task_id = task_id
        self._location = '{}/{}.task'.format(
            self._tasks_cache.location, self._task_id
        )
        self._json_location = '{}/task.json'.format(
            self._location
        )
        self._log_location = '{}/task.log'.format(
            self._location
        )
        self._json_content = bsc_content.Content(
            key=None, value=self._json_location
        )

        self._thread = None

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
    def group(self):
        return self._json_content.get('properties.group')

    @property
    def content(self):
        return self._json_content

    @classmethod
    def create(cls, tasks_index, task_id, group, name, cmd_script, time, utc_time):
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
                        cls.PropertyKeys.Group: group,
                        cls.PropertyKeys.Name: name,

                        cls.PropertyKeys.Time: time,
                        cls.PropertyKeys.UtcTime: utc_time,

                        cls.PropertyKeys.HostName: _base.Util.get_host_name(),
                        cls.PropertyKeys.UserName: _base.Util.get_user_name(),
                    },
                    'process': {
                        cls.ProcessKeys.Status: int(bsc_core.BscStatus.Waiting),
                        cls.ProcessKeys.SubmitTime: time,
                        cls.ProcessKeys.StartTime: '',
                        cls.ProcessKeys.FinishTime: '',

                        cls.ProcessKeys.Priority: 50,
                        cls.ProcessKeys.CmdScript: cmd_script
                    }
                }

            )
        return cls(tasks_index, task_id)

    def set_completion_notice(self, options):
        self._json_content.set(
            'completion_notice', options
        )
        self.accept()

    def get_completion_notice(self):
        return self._json_content.get(
            'completion_notice'
        )

    def do_update(self):
        self._json_content.reload()

    def get_status(self):
        return self._json_content.get('process.status')

    def get_start_time(self):
        return self._json_content.get('process.start_time')

    def get_finish_time(self):
        return self._json_content.get('process.finish_time')

    def set_status(self, status):
        self._json_content.set('process.status', int(status))
        self.accept()

    def refresh_start_time(self):
        self._json_content.set('process.start_time', _base.Util.get_time())
        self.accept()

    def refresh_finish_time(self):
        self._json_content.set('process.finish_time', _base.Util.get_time())
        self.accept()

    def accept(self):
        self._json_content.save()

    def save_log(self, text):
        if isinstance(text, list):
            text = '\n'.join(text)

        text = text.replace('\n\n', '\n')

        bsc_storage.StgFileOpt(
            self._log_location
        ).set_write(text)

    def read_log(self):
        if bsc_storage.StgPathMtd.get_is_file(
            self._log_location
        ):
            return bsc_storage.StgFileOpt(self._log_location).set_read()

    def do_wait_for_start(self):

        def _status_changed_fnc(task, status):
            task.set_status(status)

        def _started_fnc(task):
            task.refresh_start_time()

        def _completed_fnc(task, results):
            _completion_notice = task.get_completion_notice()
            if _completion_notice:
                # noinspection PyBroadException
                try:
                    skt = bsc_web.WebSocket()
                    if skt.connect() is True:
                        skt.send(_completion_notice)
                except Exception:
                    bsc_core.ExceptionMtd.print_stack()

        def _finished_fnc(task, status, results):
            task.refresh_finish_time()
            task.save_log(results)

        cmd_script = self._json_content.get('process.cmd_script')
        self._thread = bsc_core.TrdCommandPool.generate(cmd_script, self)
        self._thread.status_changed.connect_to(_status_changed_fnc)
        self._thread.started.connect_to(_started_fnc)
        self._thread.completed.connect_to(_completed_fnc)
        self._thread.finished.connect_to(_finished_fnc)
        self._thread.do_wait_for_start()

    def get_thread(self):
        return self._thread


class TasksCache(object):
    def __init__(self, connection):
        self._connection = connection

        self._location = '{}/tasks'.format(
            self._connection.location
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
        self._task_ids_new = []

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
        # reload json
        self._json_content.reload()

        self._task_ids_new = []
        for i_task_id in self.get_task_ids():
            if i_task_id not in self._task_dict:
                i_task = Task(self, i_task_id)
                self.register_task(i_task_id, i_task)
        return self._task_ids_new

    def register_task(self, task_id, task):
        index = self.get_task_index(task_id)
        self._task_index_dict[task_id] = index
        self._task_dict[task_id] = task
        self._task_ids_new.append(task_id)

    def new_task(self, group, name, cmd_script, completion_notice=None):
        task_id = _base.Util.new_uuid()
        time = _base.Util.get_time()
        utc_time = _base.Util.get_utc_time()
        task = Task.create(self, task_id, group, name, cmd_script, time, utc_time)
        if completion_notice is not None:
            task.set_completion_notice(completion_notice)
        index = len(self.get_task_ids())
        self._json_content.set(
            'tasks.{}'.format(task_id),
            dict(
                index=index,
                time=_base.Util.get_time(),
                utc_time=_base.Util.get_utc_time()
            )
        )
        self.accept()
        self.register_task(task_id, task)
        return task

    def get_task_ids(self):
        _ = self._json_content.get_key_names_at('tasks')
        return self._json_content.get_key_names_at('tasks')

    def get_task_index(self, task_id):
        return self._json_content.get(
            'tasks.{}.index'.format(task_id)
        )

    def exists_task_(self, task_id):
        return self._json_content.get_key_is_exists(
            'tasks.{}'.format(task_id)
        )

    def exists_task(self, task_id):
        return task_id in self._task_dict

    def find_task(self, task_id):
        return self._task_dict[task_id]

    def find_tasks(self, task_ids):
        _ = [self._task_dict[i] for i in task_ids]
        # _.sort(key=lambda x: self._task_index_dict[x.task_id])
        return _

    def get_tasks(self):
        _ = self._task_dict.values()
        _.sort(key=lambda x: self._task_index_dict[x.task_id])
        return _

    def accept(self):
        self._json_content.save()

