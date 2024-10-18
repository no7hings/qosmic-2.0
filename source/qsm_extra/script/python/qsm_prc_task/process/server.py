# coding:utf-8
from __future__ import print_function

import sys

import time

import flask

import psutil

import threading

import multiprocessing

import subprocess

import six


def update_dict(d, k, v):
    d[k] = v


class TaskProcessBase(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def auto_string(cls, text):
        if isinstance(text, six.text_type):
            return text.encode('utf-8')
        return text

    @classmethod
    def stdout(cls, name, text):
        text = cls.auto_string(text)
        sys.stdout.write(
            '{}         | <{}> {}\n'.format(time.strftime(
                cls.TIME_FORMAT, time.localtime(time.time())),
                name, text
            ),
        )

    @classmethod
    def stderr(cls, name, text):
        text = cls.auto_string(text)
        sys.stderr.write(
            '{}         | <{}> {}\n'.format(time.strftime(
                cls.TIME_FORMAT, time.localtime(time.time())),
                name, text
            ),
        )

    @classmethod
    def update_killed(cls, task_id):
        import qsm_prc_task.core as qsm_tsk_core

        pool = qsm_tsk_core.TaskPool.generate()
        prc_task = pool.find_entity(task_id)
        if prc_task:
            prc_task.set_status(prc_task.Status.Killed)

    @classmethod
    def update_stopped(cls, task_id):
        import qsm_prc_task.core as qsm_tsk_core

        task_pool = qsm_tsk_core.TaskPool.generate()
        prc_task = task_pool.find_entity(task_id)
        if prc_task:
            prc_task.set_status(prc_task.Status.Stopped)


class TaskProcessServer(object):
    LOG_KEY = 'task process server'
    APP = flask.Flask('Hook Server')

    @staticmethod
    @APP.route('/server_status', methods=['GET'])
    def server_status_fnc():
        return flask.jsonify(
            dict(
                started=True
            )
        )

    @staticmethod
    @APP.route('/worker_status', methods=['GET'])
    def worker_status_fnc():
        with TaskProcessWorker.LOCK:
            maximum = TaskProcessWorker.MAXIMUM.value
            value = TaskProcessWorker.VALUE.value
        return flask.jsonify(
            dict(
                maximum=maximum,
                value=value
            )
        )

    @staticmethod
    @APP.route('/worker_maximum', methods=['POST'])
    def worker_maximum_fnc():
        data = flask.request.get_json()
        if not data or 'maximum' not in data:
            return flask.jsonify({'error': 'Invalid input'}), 400

        prc_maximum_new = data['maximum']
        if prc_maximum_new < 0:
            return flask.jsonify({'error': 'Pool maximum cannot be negative'}), 400

        with TaskProcessWorker.MAXIMUM.get_lock():
            prc_maximum = TaskProcessWorker.MAXIMUM.value
            if prc_maximum_new > prc_maximum:
                for _ in range(prc_maximum_new-prc_maximum):
                    i_prc = multiprocessing.Process(
                        target=TaskProcessWorker.task_process_queue,
                        args=(TaskProcessWorker.QUEUE, TaskProcessWorker.LOCK, TaskProcessWorker.VALUE)
                    )
                    i_prc.start()
                    TaskProcessWorker.PROCESS_LIST.append(i_prc)
                TaskProcessWorker.MAXIMUM.value = prc_maximum_new
            elif prc_maximum_new < prc_maximum:
                for _ in range(prc_maximum-prc_maximum_new):
                    TaskProcessWorker.QUEUE.put(None)

                TaskProcessWorker.PROCESS_LIST[:] = [p for p in TaskProcessWorker.PROCESS_LIST if p.is_alive()]
                TaskProcessWorker.MAXIMUM.value = prc_maximum_new

        return flask.jsonify(
            {'status': 'Pool maximum updated', 'maximum': TaskProcessWorker.MAXIMUM.value}
        )

    @staticmethod
    @APP.route('/worker_queue', methods=['GET'])
    def worker_queue_fnc():
        with TaskProcessWorker.LOCK:
            waiting_list = TaskProcessWorker.TASK_WAITING_LIST
            started_list = TaskProcessWorker.TASK_RUNNING_LIST
        return flask.jsonify(
            dict(
                waiting=list(waiting_list),
                running=list(started_list)
            )
        )

    @staticmethod
    @APP.route('/task_new', methods=['POST'])
    def task_new_fnc():
        try:
            data = flask.request.get_json()
            if not data or 'cmd_script' not in data:
                return flask.jsonify({'error': 'Invalid input'}), 400

            import qsm_prc_task.core as qsm_tsk_core

            task_pool = qsm_tsk_core.TaskPool.generate()
            prc_task = task_pool.new_entity(**data)

            task_id = prc_task.id
            TaskProcessWorker.TASK_WAITING_LIST.append(task_id)

            TaskProcessBase.stdout(
                TaskProcessServer.LOG_KEY, 'Add task to queue: "{}"'.format(task_id)
            )
            TaskProcessWorker.QUEUE.put(prc_task)
            return flask.jsonify({'status': 'Task added to queue'}), 202
        except Exception as e:
            import traceback
            traceback.print_stack()
            return flask.jsonify({'error': str(e)}), 500

    @staticmethod
    @APP.route('/task_requeue', methods=['POST'])
    def task_requeue_fnc():
        data = flask.request.get_json()
        if not data or 'task_id' not in data:
            return flask.jsonify({'error': 'invalid input'}), 400

        task_id = data['task_id']

        if task_id in TaskProcessWorker.TASK_WAITING_LIST or task_id in TaskProcessWorker.TASK_RUNNING_LIST:
            TaskProcessBase.stderr(
                TaskProcessServer.LOG_KEY, 'Task is already in queue: "{}"'.format(task_id)
            )
            return flask.jsonify({'error': 'task is already in queue'}), 400

        import qsm_prc_task.core as qsm_tsk_core

        task_pool = qsm_tsk_core.TaskPool.generate()
        prc_task = task_pool.find_entity(task_id)
        prc_task.set_status(prc_task.Status.Waiting)

        TaskProcessWorker.TASK_WAITING_LIST.append(task_id)
        TaskProcessBase.stdout(
            TaskProcessServer.LOG_KEY, 'Add(requeue) task to queue: "{}"'.format(task_id)
        )
        TaskProcessWorker.QUEUE.put(prc_task)
        return flask.jsonify({'status': 'Task added to queue'}), 202

    @staticmethod
    @APP.route('/task_stop', methods=['POST'])
    def task_stop_fnc():
        data = flask.request.get_json()
        if not data or 'task_id' not in data:
            return flask.jsonify({'error': 'Invalid input'}), 400

        task_id = data['task_id']
        with TaskProcessWorker.LOCK:
            if task_id in TaskProcessWorker.TASK_WAITING_LIST:
                try:
                    TaskProcessWorker.TASK_WAITING_LIST.remove(task_id)
                    TaskProcessBase.update_stopped(task_id)
                    TaskProcessBase.stdout(
                        TaskProcessServer.LOG_KEY, 'Stop task: "{}"'.format(task_id)
                    )
                    return flask.jsonify({'status': 'Task Stopped'}), 200
                except Exception as e:
                    return flask.jsonify({'error': 'Failed to stop task: {}'.format(e)}), 500
            elif task_id in TaskProcessWorker.TASK_RUNNING_LIST:
                try:
                    TaskProcessWorker.TASK_RUNNING_LIST.remove(task_id)
                    TaskProcessBase.update_stopped(task_id)
                    TaskProcessBase.stdout(
                        TaskProcessServer.LOG_KEY, 'Kill task: "{}"'.format(task_id)
                    )
                    if task_id in TaskProcessWorker.TASK_PROCESS_PID_DICT:
                        pid = TaskProcessWorker.TASK_PROCESS_PID_DICT.get(task_id)
                        try:
                            p = psutil.Process(pid)
                            p.kill()
                            TaskProcessWorker.TASK_PROCESS_PID_DICT.pop(task_id, None)
                            TaskProcessBase.update_killed(task_id)
                            TaskProcessBase.stdout(
                                TaskProcessServer.LOG_KEY, 'Kill process: "{}"'.format(pid)
                            )
                            return flask.jsonify({'status': 'Process killed'}), 200
                        except Exception as e:
                            return flask.jsonify({'error': 'Failed to kill process: {}'.format(e)}), 500
                    return flask.jsonify({'status': 'Task Killed'}), 200
                except Exception as e:
                    return flask.jsonify({'error': 'Failed to kill task: {}'.format(e)}), 500
            else:
                return flask.jsonify({'error': 'Task not found'}), 404


class TaskProcess(object):
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


class TaskProcessWorker(object):
    LOG_KEY = 'task process worker'

    QUEUE = multiprocessing.Queue()
    LOCK = multiprocessing.Lock()

    MAXIMUM_INITIAL = 5

    MAXIMUM = multiprocessing.Value('i', 0)

    VALUE = multiprocessing.Value('i', 0)

    PROCESS_LIST = []

    TASK_PROCESS_PID_DICT = {}

    TASK_WAITING_LIST = []
    TASK_RUNNING_LIST = []

    @classmethod
    def task_process_queue(
        cls,
        index, task_process_queue, task_process_lock, process_value,
        task_process_pid_dict, task_waiting_list, task_running_list
    ):
        while True:
            prc_task = task_process_queue.get()
            if prc_task is None:
                break

            with task_process_lock:
                process_value.value += 1

            try:
                task_id = prc_task.id
                if task_id in task_waiting_list:
                    with task_process_lock:
                        task_waiting_list.remove(task_id)
                        task_running_list.append(task_id)

                    cls.update_started_fnc(prc_task, task_running_list)
                    # run
                    cls.task_process(index, prc_task, task_process_lock, task_running_list, task_process_pid_dict)
                    # finish
                    with task_process_lock:
                        # maybe it is removed by stop
                        if task_id in task_running_list:
                            task_running_list.remove(task_id)
            finally:
                with task_process_lock:
                    process_value.value -= 1

    @classmethod
    def task_process(cls, index, prc_task, task_process_lock, task_running_list, task_process_pid_dict):
        cmd_script = prc_task.get('cmd_script')
        t_s = time.time()
        if cmd_script:
            task_id = prc_task.id

            if task_id not in task_running_list:
                return

            task_prc = TaskProcess(cmd_script)

            with task_process_lock:
                task_process_pid_dict[task_id] = task_prc.get_pid()

            try:
                with cls.LOCK:
                    cls.update_running_fnc(prc_task, task_running_list)

                rtc = task_prc.execute()
                if rtc == 0:
                    TaskProcessBase.stdout(
                        cls.LOG_KEY, 'Process is completed: `{}`'.format(cmd_script)
                    )
                    # completed
                    with cls.LOCK:
                        cls.update_completed_fnc(prc_task, task_running_list)
                else:
                    TaskProcessBase.stderr(
                        cls.LOG_KEY, 'Process is failed: `{}`'.format(cmd_script)
                    )
                    if rtc != 15:
                        # failed
                        with task_process_lock:
                            cls.update_failed_fnc(prc_task, task_running_list)
                # finished
                with cls.LOCK:
                    cls.update_finished_fnc(prc_task, task_prc.get_results(), task_running_list)
            except Exception as e:
                cls.update_error_occurred_fnc(prc_task, e, task_running_list)
                TaskProcessBase.stderr(
                    cls.LOG_KEY, 'Process is error occurred: `{}`'.format(cmd_script)
                )
            finally:
                with task_process_lock:
                    if task_id in task_process_pid_dict:
                        task_process_pid_dict.pop(task_id)

                t_c = time.time()-t_s
                TaskProcessBase.stdout(
                    cls.LOG_KEY, 'Process exit cost time {}s'.format(t_c)
                )

    @classmethod
    def update_started_fnc(cls, prc_task, task_running_list):
        if prc_task.id not in task_running_list:
            return

        TaskProcessBase.stdout(
            cls.LOG_KEY, 'Task is started: "{}"'.format(prc_task.id)
        )
        prc_task.refresh_start()
        # cls.send_task_socket(
        #     'status_changed',
        #     task_id=prc_task.id, status=prc_task.Status.Started
        # )

    @classmethod
    def update_running_fnc(cls, prc_task, task_running_list):
        if prc_task.id not in task_running_list:
            return
        prc_task.set_status(
            prc_task.Status.Running
        )

    @classmethod
    def update_completed_fnc(cls, prc_task, task_running_list):
        if prc_task.id not in task_running_list:
            return

        prc_task.set_status(prc_task.Status.Completed)

        _completed_notice = prc_task.get('completed_notice')
        if _completed_notice:
            # noinspection PyBroadException
            try:
                import lxbasic.web as bsc_web

                import qsm_prc_task.process as qsm_prc_tsk_process

                skt = bsc_web.WebSocket(
                    qsm_prc_tsk_process.NoticeWebServerBase.HOST, qsm_prc_tsk_process.NoticeWebServerBase.PORT
                )
                if skt.connect() is True:
                    skt.send(_completed_notice)

                import qsm_prc_task.core as qsm_tsk_core

                notice_pool = qsm_tsk_core.NoticePool.generate()
                notice_pool.new_entity(
                    type=prc_task.get('type'),
                    name=prc_task.get('name'),
                    file=prc_task.get('output_file'),
                    task=prc_task.id
                )
            except Exception:
                import traceback
                traceback.print_stack()

    @classmethod
    def update_failed_fnc(cls, prc_task, task_running_list):
        if prc_task.id not in task_running_list:
            return
        prc_task.set_status(prc_task.Status.Failed)

    @classmethod
    def update_finished_fnc(cls, prc_task, results, task_running_list):
        if prc_task.id not in task_running_list:
            return

        TaskProcessBase.stdout(
            cls.LOG_KEY, 'Task is finished: "{}"'.format(prc_task.id)
        )
        prc_task.refresh_finish()
        prc_task.save_log(results)

    @classmethod
    def update_error_occurred_fnc(cls, prc_task, results, task_running_list):
        if prc_task.id not in task_running_list:
            return
        prc_task.set_status(prc_task.Status.Error)

    @classmethod
    def send_task_socket(cls, key, **kwargs):
        # noinspection PyBroadException
        try:
            import lxbasic.web as bsc_web

            import qsm_prc_task.process as qsm_prc_tsk_process

            skt = bsc_web.WebSocket(
                qsm_prc_tsk_process.TaskWebServerBase.HOST, qsm_prc_tsk_process.TaskWebServerBase.PORT
            )
            if skt.connect() is True:
                value = bsc_web.UrlOptions.to_string(kwargs)
                skt.send('{}?{}'.format(key, value))
        except Exception:
            import traceback
            traceback.print_stack()


def start(host, port, dbug=False, use_reloader=False):
    manager = multiprocessing.Manager()

    TaskProcessWorker.PROCESS_LIST = []
    TaskProcessWorker.TASK_PROCESS_PID_DICT = manager.dict()
    TaskProcessWorker.TASK_WAITING_LIST = manager.list()
    TaskProcessWorker.TASK_RUNNING_LIST = manager.list()

    with TaskProcessWorker.MAXIMUM.get_lock():
        TaskProcessWorker.MAXIMUM.value = TaskProcessWorker.MAXIMUM_INITIAL

    for i_idx in range(TaskProcessWorker.MAXIMUM_INITIAL):
        i_prc = multiprocessing.Process(
            target=TaskProcessWorker.task_process_queue,
            args=(
                i_idx,
                TaskProcessWorker.QUEUE,
                TaskProcessWorker.LOCK,
                TaskProcessWorker.VALUE,
                TaskProcessWorker.TASK_PROCESS_PID_DICT,
                TaskProcessWorker.TASK_WAITING_LIST,
                TaskProcessWorker.TASK_RUNNING_LIST,
            )
        )
        i_prc.start()
        TaskProcessWorker.PROCESS_LIST.append(i_prc)

    TaskProcessServer.APP.run(
        host=host,
        port=port,
        debug=dbug,
        use_reloader=use_reloader
    )

    for _ in range(TaskProcessWorker.MAXIMUM.value):
        TaskProcessWorker.QUEUE.put(None)

    for i_prc in TaskProcessWorker.PROCESS_LIST:
        i_prc.join()


def start_use_process(host, port, dbug=True, use_reloader=False):
    prc = multiprocessing.Process(
        target=start, args=(host, port, dbug, use_reloader)
    )
    prc.start()
    return prc


if __name__ == '__main__':
    start(host='localhost', port=9528, use_reloader=False)

