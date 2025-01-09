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


class TaskBase(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def ensure_string(cls, text):
        if isinstance(text, six.text_type):
            return text.encode('utf-8')
        return text

    @classmethod
    def stdout(cls, name, text):
        text = cls.ensure_string(text)
        sys.stdout.write(
            '{}         | <{}> {}\n'.format(time.strftime(
                cls.TIME_FORMAT, time.localtime(time.time())),
                name, text
            ),
        )

    @classmethod
    def stderr(cls, name, text):
        text = cls.ensure_string(text)
        sys.stderr.write(
            '{}         | <{}> {}\n'.format(time.strftime(
                cls.TIME_FORMAT, time.localtime(time.time())),
                name, text
            ),
        )

    @classmethod
    def update_killed(cls, task_id):
        import qsm_lazy_bks.core as lzy_bks_core

        task_pool = lzy_bks_core.TaskPool.generate()
        bks_task = task_pool.find_entity(task_id)
        if bks_task:
            bks_task.set_status(bks_task.Status.Killed)

    @classmethod
    def update_stopped(cls, task_id):
        import qsm_lazy_bks.core as lzy_bks_core

        task_pool = lzy_bks_core.TaskPool.generate()
        bks_task = task_pool.find_entity(task_id)
        if bks_task:
            bks_task.set_status(bks_task.Status.Stopped)


class TaskServer(object):
    LOG_KEY = 'task server'
    APP = flask.Flask('Backstage Task Server')

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
        with TaskWorker.LOCK:
            maximum = TaskWorker.MAXIMUM.value
            value = TaskWorker.VALUE.value
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

        with TaskWorker.MAXIMUM.get_lock():
            prc_maximum = TaskWorker.MAXIMUM.value
            if prc_maximum_new > prc_maximum:
                for _ in range(prc_maximum_new-prc_maximum):
                    i_prc = multiprocessing.Process(
                        target=TaskWorker.subprocess_prc,
                        args=(TaskWorker.QUEUE, TaskWorker.LOCK, TaskWorker.VALUE)
                    )
                    i_prc.start()
                    TaskWorker.PROCESS_STACK.append(i_prc)
                TaskWorker.MAXIMUM.value = prc_maximum_new
            elif prc_maximum_new < prc_maximum:
                for _ in range(prc_maximum-prc_maximum_new):
                    TaskWorker.QUEUE.put(None)

                TaskWorker.PROCESS_STACK[:] = [p for p in TaskWorker.PROCESS_STACK if p.is_alive()]
                TaskWorker.MAXIMUM.value = prc_maximum_new

        return flask.jsonify(
            {'status': 'Pool maximum updated', 'maximum': TaskWorker.MAXIMUM.value}
        )

    @staticmethod
    @APP.route('/worker_queue', methods=['GET'])
    def worker_queue_fnc():
        with TaskWorker.LOCK:
            waiting_list = TaskWorker.WAITING_TASK_IDS
            started_list = TaskWorker.RUNNING_TASK_IDS
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

            import qsm_lazy_bks.core as lzy_bks_core

            task_pool = lzy_bks_core.TaskPool.generate()
            bks_task = task_pool.new_entity(**data)

            task_id = bks_task.id
            TaskWorker.WAITING_TASK_IDS.append(task_id)

            TaskBase.stdout(
                TaskServer.LOG_KEY, 'Add task to queue: "{}"'.format(task_id)
            )
            TaskWorker.QUEUE.put(bks_task)
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

        if task_id in TaskWorker.WAITING_TASK_IDS or task_id in TaskWorker.RUNNING_TASK_IDS:
            TaskBase.stderr(
                TaskServer.LOG_KEY, 'Task is already in queue: "{}"'.format(task_id)
            )
            return flask.jsonify({'error': 'task is already in queue'}), 400

        import qsm_lazy_bks.core as lzy_bks_core

        task_pool = lzy_bks_core.TaskPool.generate()
        bks_task = task_pool.find_entity(task_id)
        bks_task.set_status(bks_task.Status.Waiting)

        TaskWorker.WAITING_TASK_IDS.append(task_id)
        TaskBase.stdout(
            TaskServer.LOG_KEY, 'Add(requeue) task to queue: "{}"'.format(task_id)
        )
        TaskWorker.QUEUE.put(bks_task)
        return flask.jsonify({'status': 'Task added to queue'}), 202

    @staticmethod
    @APP.route('/task_stop', methods=['POST'])
    def task_stop_fnc():
        data = flask.request.get_json()
        if not data or 'task_id' not in data:
            return flask.jsonify({'error': 'Invalid input'}), 400

        task_id = data['task_id']
        with TaskWorker.LOCK:
            if task_id in TaskWorker.WAITING_TASK_IDS:
                try:
                    TaskWorker.WAITING_TASK_IDS.remove(task_id)
                    TaskBase.update_stopped(task_id)
                    TaskBase.stdout(
                        TaskServer.LOG_KEY, 'Stop task: "{}"'.format(task_id)
                    )
                    return flask.jsonify({'status': 'Task Stopped'}), 200
                except Exception as e:
                    return flask.jsonify({'error': 'Failed to stop task: {}'.format(e)}), 500
            elif task_id in TaskWorker.RUNNING_TASK_IDS:
                try:
                    TaskWorker.RUNNING_TASK_IDS.remove(task_id)
                    TaskBase.update_stopped(task_id)
                    TaskBase.stdout(
                        TaskServer.LOG_KEY, 'Kill task: "{}"'.format(task_id)
                    )
                    if task_id in TaskWorker.TASK_PROCESS_PID_DICT:
                        pid = TaskWorker.TASK_PROCESS_PID_DICT.get(task_id)
                        try:
                            p = psutil.Process(pid)
                            p.kill()
                            TaskWorker.TASK_PROCESS_PID_DICT.pop(task_id, None)
                            TaskBase.update_killed(task_id)
                            TaskBase.stdout(
                                TaskServer.LOG_KEY, 'Kill process: "{}"'.format(pid)
                            )
                            return flask.jsonify({'status': 'Process killed'}), 200
                        except Exception as e:
                            return flask.jsonify({'error': 'Failed to kill process: {}'.format(e)}), 500
                    return flask.jsonify({'status': 'Task Killed'}), 200
                except Exception as e:
                    return flask.jsonify({'error': 'Failed to kill task: {}'.format(e)}), 500
            else:
                return flask.jsonify({'error': 'Task not found'}), 404


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

    MAXIMUM_INITIAL = 5

    MAXIMUM = multiprocessing.Value('i', 0)

    VALUE = multiprocessing.Value('i', 0)

    PROCESS_STACK = []

    TASK_PROCESS_PID_DICT = {}

    WAITING_TASK_IDS = []
    RUNNING_TASK_IDS = []

    @classmethod
    def subprocess_prc(
        cls,
        index, task_worker_queue, task_worker_lock, process_value,
        task_process_pid_dict, waiting_task_ids, running_task_ids
    ):
        while True:
            bks_task = task_worker_queue.get()
            if bks_task is None:
                break

            with task_worker_lock:
                process_value.value += 1

            try:
                task_id = bks_task.id
                if task_id in waiting_task_ids:
                    with task_worker_lock:
                        waiting_task_ids.remove(task_id)
                        running_task_ids.append(task_id)
                    # start
                    cls.update_started_fnc(bks_task, running_task_ids)
                    # run
                    cls.execute_subprocess(index, bks_task, task_worker_lock, running_task_ids, task_process_pid_dict)
                    # finish
                    with task_worker_lock:
                        # maybe it is removed by stop
                        if task_id in running_task_ids:
                            running_task_ids.remove(task_id)
            finally:
                with task_worker_lock:
                    process_value.value -= 1

    @classmethod
    def execute_subprocess(cls, index, bks_task, task_worker_lock, running_task_ids, task_process_pid_dict):
        cmd_script = bks_task.get('cmd_script')
        t_s = time.time()
        if cmd_script:
            task_id = bks_task.id

            if task_id not in running_task_ids:
                return

            task_prc = TaskSubprocess(cmd_script)

            with task_worker_lock:
                task_process_pid_dict[task_id] = task_prc.get_pid()

            try:
                with cls.LOCK:
                    cls.update_running_fnc(bks_task, running_task_ids)

                rtc = task_prc.execute()
                if rtc == 0:
                    TaskBase.stdout(
                        cls.LOG_KEY, 'Process is completed: `{}`'.format(cmd_script)
                    )
                    # completed
                    with cls.LOCK:
                        cls.update_completed_fnc(bks_task, running_task_ids)
                else:
                    TaskBase.stderr(
                        cls.LOG_KEY, 'Process is failed: `{}`'.format(cmd_script)
                    )
                    if rtc != 15:
                        # failed
                        with task_worker_lock:
                            cls.update_failed_fnc(bks_task, running_task_ids)
                # finished
                with cls.LOCK:
                    cls.update_finished_fnc(bks_task, task_prc.get_results(), running_task_ids)
            except Exception as e:
                cls.update_error_occurred_fnc(bks_task, e, running_task_ids)
                TaskBase.stderr(
                    cls.LOG_KEY, 'Process is error occurred: `{}`'.format(cmd_script)
                )
            finally:
                with task_worker_lock:
                    if task_id in task_process_pid_dict:
                        task_process_pid_dict.pop(task_id)

                t_c = time.time()-t_s
                TaskBase.stdout(
                    cls.LOG_KEY, 'Process exit cost time {}s'.format(t_c)
                )

    @classmethod
    def update_started_fnc(cls, bks_task, running_task_ids):
        if bks_task.id not in running_task_ids:
            return

        TaskBase.stdout(
            cls.LOG_KEY, 'Task is started: "{}"'.format(bks_task.id)
        )
        bks_task.update_by_start()

    @classmethod
    def update_running_fnc(cls, bks_task, running_task_ids):
        if bks_task.id not in running_task_ids:
            return
        bks_task.set_status(
            bks_task.Status.Running
        )

    @classmethod
    def update_completed_fnc(cls, bks_task, running_task_ids):
        if bks_task.id not in running_task_ids:
            return

        bks_task.set_status(bks_task.Status.Completed)

        _completed_notice = bks_task.get('completed_notice')
        if _completed_notice:
            # noinspection PyBroadException
            try:
                import lxbasic.web as bsc_web

                import qsm_lazy_bks.worker as lzy_bks_worker

                skt = bsc_web.WebSocket(
                    lzy_bks_worker.NoticeWebServerBase.HOST, lzy_bks_worker.NoticeWebServerBase.PORT
                )
                if skt.connect() is True:
                    skt.send(_completed_notice)

                import qsm_lazy_bks.core as lzy_bks_core

                notice_pool = lzy_bks_core.NoticePool.generate()
                notice_pool.new_entity(
                    type=bks_task.get('type'),
                    name=bks_task.get('name'),
                    file=bks_task.get('output_file'),
                    task=bks_task.id
                )
            except Exception:
                import traceback
                traceback.print_stack()

    @classmethod
    def update_failed_fnc(cls, bks_task, running_task_ids):
        if bks_task.id not in running_task_ids:
            return
        bks_task.set_status(bks_task.Status.Failed)

    @classmethod
    def update_finished_fnc(cls, bks_task, results, running_task_ids):
        if bks_task.id not in running_task_ids:
            return

        TaskBase.stdout(
            cls.LOG_KEY, 'Task is finished: "{}"'.format(bks_task.id)
        )
        bks_task.update_by_finish()
        bks_task.save_process_log(results)

    @classmethod
    def update_error_occurred_fnc(cls, bks_task, results, running_task_ids):
        if bks_task.id not in running_task_ids:
            return
        bks_task.set_status(bks_task.Status.Error)

    @classmethod
    def send_task_socket(cls, key, **kwargs):
        # noinspection PyBroadException
        try:
            import lxbasic.web as bsc_web

            import qsm_lazy_bks.worker as lzy_bks_worker

            skt = bsc_web.WebSocket(
                lzy_bks_worker.TaskWebServerBase.HOST, lzy_bks_worker.TaskWebServerBase.PORT
            )
            if skt.connect() is True:
                value = bsc_web.UrlOptions.to_string(kwargs)
                skt.send('{}?{}'.format(key, value))
        except Exception:
            import traceback
            traceback.print_stack()


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
            target=TaskWorker.subprocess_prc,
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


def start_use_process(host, port, dbug=True, use_reloader=False):
    prc = multiprocessing.Process(
        target=start, args=(host, port, dbug, use_reloader)
    )
    prc.start()
    return prc


if __name__ == '__main__':
    start(host='localhost', port=9528, use_reloader=False)

