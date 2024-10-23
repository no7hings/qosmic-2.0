# coding:utf-8
import sys

import threading

import subprocess

import six
# process
from . import configure as _configure

from . import thread as _thread

from . import process as _process


class ThreadWorker(threading.Thread):
    WORKERS = []
    # MAXIMUM = int(CPU_COUNT*.75)
    MAXIMUM = 5
    VALUE = 0
    EVENT = threading.Event()
    LOCK = threading.Lock()
    #
    Status = _configure.BasProcessStatus

    def _do_update_status(self, status):
        self._status = status
        if self._kill_flag is False:
            self._signal_status_changed.send_emit(
                self._entity, status
            )

    def _do_completed(self, results):
        if self._kill_flag is False:
            self._signal_completed.send_emit(
                self._entity, results
            )

    def _do_failed(self, results):
        if self._kill_flag is False:
            self._signal_failed.send_emit(
                self._entity, results
            )

    def _do_started(self):
        if self._kill_flag is False:
            self._signal_started.send_emit(
                self._entity
            )

    def _do_finished(self, status, results):
        if self._kill_flag is False:
            self._signal_finished.send_emit(
                self._entity, status, results
            )

    def __init__(self, cmd_script, entity=0):
        threading.Thread.__init__(self)
        self._cmd_script = cmd_script
        self._entity = entity

        self._kill_flag = False

        self._signal_status_changed = _thread.TrdSignal(object, int)
        self._signal_completed = _thread.TrdSignal(object, list)
        self._signal_failed = _thread.TrdSignal(object, list)
        self._signal_started = _thread.TrdSignal(object)
        self._signal_finished = _thread.TrdSignal(object, int, list)

        self._status = self.Status.Unknown

        self._options = {}

    def run(self):
        if self._kill_flag is True:
            return

        self._do_update_status(self.Status.Running)

        status = self.Status.Running
        return_dicts = []
        try:
            # single process
            if isinstance(self._cmd_script, six.string_types):
                return_dict = {}
                return_dicts.append(return_dict)
                _process.BscProcess.execute_as_block(
                    self._cmd_script, clear_environ='auto', return_dict=return_dict
                )
                status = self.Status.Completed
            # many process execute one by one
            elif isinstance(self._cmd_script, (set, tuple, list)):
                for i_cmd_script in self._cmd_script:
                    i_return_dict = {}
                    return_dicts.append(i_return_dict)
                    _process.BscProcess.execute_as_block(
                        i_cmd_script, clear_environ='auto', return_dict=i_return_dict
                    )
                status = self.Status.Completed
            else:
                status = self.Status.Unknown
        except subprocess.CalledProcessError:
            status = self.Status.Failed
        finally:
            results = []
            for i_return_dict in return_dicts:
                if 'results' in i_return_dict:
                    i_results = i_return_dict['results']
                    if isinstance(i_results, list):
                        results.extend(i_results)
                    elif isinstance(i_results, six.string_types):
                        results.append(i_results)

            self._do_update_status(status)
            if status == self.Status.Completed:
                self._do_completed(results)
            elif status == self.Status.Failed:
                self._do_failed(results)

            self._do_finished(self._status, results)

            ThreadWorker.LOCK.acquire()
            ThreadWorker.WORKERS.remove(self)
            ThreadWorker.VALUE -= 1
            sys.stdout.write('thread is finished: {}\n'.format(self._entity))
            # unlock
            if ThreadWorker.VALUE < ThreadWorker.MAXIMUM:
                ThreadWorker.EVENT.set()
                ThreadWorker.EVENT.clear()
            ThreadWorker.LOCK.release()

    @property
    def status_changed(self):
        return self._signal_status_changed

    @property
    def completed(self):
        # index, results
        return self._signal_completed

    @property
    def failed(self):
        return self._signal_failed

    @property
    def started(self):
        return self._signal_started

    @property
    def finished(self):
        return self._signal_finished

    @staticmethod
    def is_busy():
        return ThreadWorker.VALUE >= ThreadWorker.MAXIMUM

    @staticmethod
    def check_waiting(entity):
        ThreadWorker.LOCK.acquire()
        # lock
        if ThreadWorker.VALUE >= ThreadWorker.MAXIMUM:
            sys.stderr.write('thread is waiting: {}\n'.format(entity))
            ThreadWorker.LOCK.release()
            ThreadWorker.EVENT.wait()
        else:
            ThreadWorker.LOCK.release()

    @staticmethod
    def generate(cmd_script, entity=0):
        ThreadWorker.LOCK.acquire()
        t = ThreadWorker(cmd_script, entity)
        ThreadWorker.WORKERS.append(t)
        ThreadWorker.LOCK.release()
        return t

    def get_status(self):
        return self._status

    def do_kill(self):
        self._do_update_status(
            self.Status.Killed
        )
        self._kill_flag = True

    def do_quit(self):
        pass

    def do_wait_for_start(self):
        self._do_update_status(self.Status.Waiting)
        self.check_waiting(self._entity)
        #
        ThreadWorker.VALUE += 1
        sys.stdout.write('thread is started: {}\n'.format(self._entity))
        self._do_update_status(self.Status.Started)
        self._do_started()
        self.start()
