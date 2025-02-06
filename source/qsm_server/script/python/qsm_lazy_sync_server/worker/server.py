# coding:utf-8
from __future__ import print_function

import shutil

import sys

import os

import enum

import time

import flask

import threading

import multiprocessing

import subprocess

import six

import json


class TaskBase(object):
    VERBOSE_LEVEL = 0

    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    @classmethod
    def read_json(cls, json_path):
        with open(json_path) as j:
            # noinspection PyTypeChecker
            raw = json.load(j)
            j.close()
            return raw

    @classmethod
    def write_json(cls, json_path, data):
        dir_path = os.path.dirname(json_path)
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)

        with open(json_path, 'w') as j:
            json.dump(
                data,
                j,
                indent=4
            )

    @classmethod
    def ensure_string(cls, text):
        if isinstance(text, six.text_type):
            return text.encode('utf-8')
        return text

    @classmethod
    def stdout(cls, name, text):
        if cls.VERBOSE_LEVEL < 1:
            text = cls.ensure_string(text)
            sys.stdout.write(
                '{}         | <{}> {}\n'.format(time.strftime(
                    cls.TIME_FORMAT, time.localtime(time.time())),
                    name, text
                ),
            )

    @classmethod
    def stderr(cls, name, text):
        if cls.VERBOSE_LEVEL <= 1:
            text = cls.ensure_string(text)
            sys.stderr.write(
                '{}         | <{}> {}\n'.format(time.strftime(
                    cls.TIME_FORMAT, time.localtime(time.time())),
                    name, text
                ),
            )


class Task(object):
    DEFAULT_LOCATION = 'Z:/caches/database/sync-task/tasks'

    class Status(enum.IntEnum):
        Unknown = 0
        Started = 1
        Running = 2
        Waiting = 3
        Completed = 4
        Suspended = 5
        Failed = 6
        Stopped = 7
        Error = 8
        Killed = 9
        Finished = 10

        @classmethod
        def to_mapper(cls):
            return {
                int(i): str(i).split('.')[-1].lower() for i in [
                    cls.Unknown, cls.Started, cls.Running, cls.Waiting,
                    cls.Completed, cls.Suspended, cls.Failed, cls.Stopped,
                    cls.Error, cls.Killed, cls.Finished
                ]
            }

    def __init__(self, json_path):
        self._json_path = json_path

        self._task_id = os.path.splitext(os.path.basename(json_path))[0]
        self._task_data = TaskBase.read_json(json_path)

        self._json_location = self.DEFAULT_LOCATION

        self._status_mapper = self.Status.to_mapper()

        self.set_status(self.Status.Waiting)

    @property
    def id(self):
        return self._task_id
    
    @property
    def data(self):
        return self._task_data

    def update_by_start(self):
        pass

    def update_by_finish(self, results):
        pass

    def update_by_error(self, results):
        pass

    def save_process_log(self, text):
        pass

    def save_exception_log(self):
        pass

    def set_status(self, status):
        self._task_data['status'] = int(status)
        status_key = self._status_mapper[status]
        file_base = os.path.basename(self._json_path)
        json_path_new = '{}/.{}/{}'.format(
            self._json_location, status_key, file_base
        )

        if json_path_new != self._json_path:
            dir_path_new = os.path.dirname(json_path_new)
            if os.path.exists(dir_path_new) is False:
                os.makedirs(dir_path_new)
            shutil.move(self._json_path, json_path_new)

            self._json_path = json_path_new


class TaskServer(object):
    LOG_KEY = 'task server'
    APP = flask.Flask('Lazy Sync Server')

    @staticmethod
    @APP.route('/server_status', methods=['GET'])
    def server_status_fnc():
        return flask.jsonify(
            dict(
                started=True
            )
        )

    @staticmethod
    @APP.route('/task_new', methods=['POST'])
    def task_new_fnc():
        try:
            data = flask.request.get_json()
            if not data or 'json' not in data:
                return flask.jsonify({'error': 'invalid input.'}), 400

            json_path = data['json']

            task = Task(json_path)

            task_id = task.id
            TaskWorker.WAITING_TASK_IDS.append(task_id)

            TaskBase.stdout(
                TaskServer.LOG_KEY, 'task is wait for start: {}'.format(task_id)
            )
            TaskWorker.QUEUE.put(task)
            return flask.jsonify({'status': 'task added to queue.'}), 202
        except Exception as e:
            import traceback
            traceback.print_exc()
            return flask.jsonify({'error': str(e)}), 500


class TaskSubprocess(object):
    VERBOSE_LEVEL = 1

    def __init__(self, cmd_script):
        self._cmd_script = cmd_script

        self._prc = subprocess.Popen(
            self._cmd_script,
            shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
            # universal_newlines=True
        )
        self._results = []

    @classmethod
    def _stdout(cls, text):
        if cls.VERBOSE_LEVEL < 1:
            text = text.decode('utf-8', 'ignore')
            sys.stdout.write(text.encode('utf-8'))

    @classmethod
    def _stderr(cls, text):
        if cls.VERBOSE_LEVEL <= 1:
            text = text.decode('utf-8', 'ignore')
            sys.stderr.write(text.encode('utf-8'))

    @classmethod
    def _read(cls, prc, results, interval):
        while prc.poll() is None:
            time.sleep(interval)
            output = prc.stdout.read()
            if output:
                cls._stdout(output)
                results.append(output.strip())

        stdout, stderr = prc.communicate()
        if stdout:
            cls._stdout(stdout)
            results.append(stdout.strip())
        if stderr:
            cls._stderr(stderr)
            results.append(stderr.strip())

    def execute(self, interval=5):
        trd = threading.Thread(
            target=self._read, args=(self._prc, self._results, interval)
        )
        trd.start()
        trd.join()
        return self._prc.returncode

    def get_results(self):
        return self._results

    def get_pid(self):
        return self._prc.pid


class TaskWorker(object):
    LOG_KEY = 'task worker'

    QUEUE = multiprocessing.Queue()
    LOCK = multiprocessing.Lock()

    MAXIMUM_INITIAL = 16

    MAXIMUM = multiprocessing.Value('i', 0)

    VALUE = multiprocessing.Value('i', 0)

    PROCESS_STACK = []

    TASK_PROCESS_PID_DICT = {}

    WAITING_TASK_IDS = []
    RUNNING_TASK_IDS = []

    @classmethod
    def fnc_prc(
        cls,
        index, task_worker_queue, task_worker_lock, process_value,
        task_process_pid_dict, waiting_task_ids, running_task_ids
    ):
        while True:
            task = task_worker_queue.get()
            if task is None:
                break

            with task_worker_lock:
                process_value.value += 1

            try:
                task_id = task.id
                if task_id in waiting_task_ids:
                    with task_worker_lock:
                        waiting_task_ids.remove(task_id)
                        running_task_ids.append(task_id)
                    # start
                    cls.update_started_fnc(task, running_task_ids)
                    # run
                    cls.execute_fnc(index, task, task_worker_lock, running_task_ids)
                    # finish
                    with task_worker_lock:
                        # maybe it is removed by stop
                        if task_id in running_task_ids:
                            running_task_ids.remove(task_id)
            finally:
                with task_worker_lock:
                    process_value.value -= 1

    @classmethod
    def execute_fnc(cls, index, task, task_worker_lock, running_task_ids):
        import qsm_lazy_sync_server.core as c

        task_data = task.data

        fnc = c.TaskFnc.generate_fnc(task_data)
        if fnc:
            task_id = task.id

            if task_id not in running_task_ids:
                return

            # noinspection PyBroadException
            try:
                fnc()
                with task_worker_lock:
                    cls.update_completed_fnc(task, running_task_ids)
            except Exception:
                import traceback
                traceback.print_exc()
                with task_worker_lock:
                    cls.update_failed_fnc(task, running_task_ids)
            finally:
                with task_worker_lock:
                    cls.update_finished_fnc(task, [], running_task_ids)

    @classmethod
    def update_started_fnc(cls, task, running_task_ids):
        if task.id not in running_task_ids:
            return

        TaskBase.stdout(cls.LOG_KEY, 'task is started: {}.'.format(task.id))
        task.update_by_start()

    @classmethod
    def update_running_fnc(cls, task, running_task_ids):
        if task.id not in running_task_ids:
            return

        task.set_status(task.Status.Running)

    @classmethod
    def update_completed_fnc(cls, task, running_task_ids):
        if task.id not in running_task_ids:
            return

        TaskBase.stdout(cls.LOG_KEY, 'task is completed: {}'.format(task.id))
        task.set_status(task.Status.Completed)

    @classmethod
    def update_failed_fnc(cls, task, running_task_ids):
        if task.id not in running_task_ids:
            return

        TaskBase.stderr(cls.LOG_KEY, 'task is failed: {}'.format(task.id))
        task.set_status(task.Status.Failed)

    @classmethod
    def update_finished_fnc(cls, task, results, running_task_ids):
        if task.id not in running_task_ids:
            return

        task.update_by_finish(results)


def start(host, port, dbug=False, use_reloader=False):
    manager = multiprocessing.Manager()

    TaskWorker.PROCESS_STACK = []
    TaskWorker.TASK_PROCESS_PID_DICT = manager.dict()
    TaskWorker.WAITING_TASK_IDS = manager.list()
    TaskWorker.RUNNING_TASK_IDS = manager.list()

    with TaskWorker.MAXIMUM.get_lock():
        TaskWorker.MAXIMUM.value = TaskWorker.MAXIMUM_INITIAL

    for i_idx in range(TaskWorker.MAXIMUM_INITIAL):
        i_prc = multiprocessing.Process(
            target=TaskWorker.fnc_prc,
            args=(
                i_idx,
                TaskWorker.QUEUE,
                TaskWorker.LOCK,
                TaskWorker.VALUE,
                TaskWorker.TASK_PROCESS_PID_DICT,
                TaskWorker.WAITING_TASK_IDS,
                TaskWorker.RUNNING_TASK_IDS,
            )
        )
        i_prc.start()
        TaskWorker.PROCESS_STACK.append(i_prc)

    TaskServer.APP.run(
        host=host,
        port=port,
        debug=dbug,
        use_reloader=use_reloader
    )

    for _ in range(TaskWorker.MAXIMUM.value):
        TaskWorker.QUEUE.put(None)

    for i_prc in TaskWorker.PROCESS_STACK:
        i_prc.join()


if __name__ == '__main__':
    start(host='localhost', port=12306, dbug=True, use_reloader=False)
