# coding:utf-8
import types

import time

import functools

import sys

import six

import threading

import subprocess

import locale

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log
# gui
from ... import core as _gui_core
# qt
from .wrap import *


class _Subprocess(object):
    ENCODING = locale.getpreferredencoding()

    KEY = 'sub process'

    VERBOSE_LEVEL = 1

    @classmethod
    def _stdout(cls, text):
        text = text.decode('utf-8', 'ignore')
        text = text.encode('utf-8')
        if cls.VERBOSE_LEVEL < 1:
            sys.stdout.write(text)
        return text

    @classmethod
    def _stderr(cls, text):
        text = text.decode('utf-8', 'ignore')
        text = text.encode('utf-8')
        if cls.VERBOSE_LEVEL <= 1:
            sys.stderr.write(text)
        return text

    def __init__(self, thread, command, **kwargs):
        self._trd = thread
        self._prc = None
        self._cmd_script = command

        self._results = []

        self._kill_flag = False
        self._finish_flag = False

    def _read_fd(self, prc, trd):
        while True:
            if trd._kill_flag is True:
                self._stderr(
                    'subprocess is killed at: {}'.format(self._trd._entity)
                )
                self._exit_flag.set()
                break

            rtc = prc.poll()
            if rtc is not None:
                self._stdout(
                    'subprocess is completed at: {}, return code is {}'.format(
                        self._trd._entity, rtc
                    )
                )
                self._exit_flag.set()
                break

            result = prc.stdout.readline()
            if result:
                result = self._stdout(result)
                self._results.append(result)
                trd._do_log_filter(result)

                sys.stdout.flush()

    def do_kill(self):
        if not self._kill_flag:
            self._kill_flag = True
            if self._prc is None:
                return

            if self._prc.poll() is None:
                self._kill_process_fnc(self._prc)
                try:
                    _ = subprocess.check_output(
                        ["taskkill", "/F", "/T", "/PID", str(self._prc.pid)],
                        shell=True,
                        stderr=subprocess.STDOUT
                    )
                    self._stderr('subprocess is killed at: {}\n'.format(self._trd._entity))
                except subprocess.CalledProcessError as e:
                    self._stderr('subprocess is kill failed at : {}\n'.format(self._trd._entity))

    @classmethod
    def _kill_process_fnc(cls, prc):
        pass
        # try:
        #     import psutil
        #
        #     parent = psutil.Process(prc.pid)
        #     for child in parent.children(recursive=True):
        #         child.kill()
        #     parent.kill()
        # except ImportError:
        #     prc.kill()

    def get_results(self):
        return self._results

    def run(self):
        if self._trd._kill_flag is True:
            return

        st = time.time()

        self._exit_flag = threading.Event()

        self._prc = subprocess.Popen(
            self._cmd_script,
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        t = threading.Thread(target=self._read_fd, args=(self._prc, self._trd))
        t.setDaemon(True)
        t.start()

        rtc = self._prc.wait()
        if rtc is not None:
            if self._trd._kill_flag is False:
                if rtc > 0:
                    self._stderr(
                        'subprocess is error at: {}, return code is {}'.format(
                            self._trd._entity, rtc
                        )
                    )
                    raise subprocess.CalledProcessError(rtc, self._cmd_script)

        ct = time.time()-st
        self._stdout(
            'subprocess is finished at: {}, return code is {}, cost {}s'.format(
                self._trd._entity, rtc, ct
            )
        )


class QtThreadWorkerForSubprocess(QtCore.QThread):
    started = qt_signal()
    running = qt_signal()
    finished = qt_signal()
    completed = qt_signal()
    killed = qt_signal()
    failed = qt_signal(list)

    Status = _gui_core.GuiProcessStatus

    THREAD_WAITING_LIST = []
    THREAD_RUNNING_LIST = []

    VERBOSE_LEVEL = 0

    INDEX = 0

    @classmethod
    def _stdout(cls, text):
        if cls.VERBOSE_LEVEL < 1:
            sys.stdout.write(text)

    @classmethod
    def _stderr(cls, text):
        if cls.VERBOSE_LEVEL <= 1:
            sys.stderr.write(text)

    def _do_progress_started(self, maximum):
        if self._kill_flag is True:
            return

        self._progress_bar._do_progress_started_(maximum)

    def _do_progress_update(self, percent):
        if self._kill_flag is True:
            return

        self._progress_bar._do_progress_update_(percent)

    def _do_log_update(self, text):
        if self._kill_flag is True:
            return

        # noinspection PyUnresolvedReferences
        self._progress_bar.log_update.emit(text)

    def _do_log_filter(self, text):
        if self._kill_flag is True:
            return

        process_start = bsc_log.Log.filter_process_start(text)
        if process_start:
            _count = process_start[-1]
            self._do_progress_started(_count)

        pgs_result = bsc_log.Log.filter_progress(text)
        if pgs_result:
            _time, _keyword, _percent = pgs_result
            self._do_progress_update(_percent)

        result = bsc_log.Log.filter_result(text)
        if result:
            self._do_log_update(text)

    def _do_status_update(self, status):
        if self._kill_flag is True:
            return

        # noinspection PyUnresolvedReferences
        self._progress_bar.status_update.emit(status)

    def __init__(self, *args, **kwargs):
        self._progress_bar = kwargs.pop('progress_bar')
        super(QtThreadWorkerForSubprocess, self).__init__(*args, **kwargs)

        self.parent()._thread_workers.append(self)

        self._kill_flag = False
        self._finish_flag = False

        self._entity = 0

        self._fnc = None
        self._args = ()
        self._kwargs = ()

        self._subprocess = None

        self._do_status_update(self.Status.Waiting)

    def set_fnc(self, fnc, *args, **kwargs):
        self._fnc = fnc
        self._args = args
        self._kwargs = kwargs

    def set_entity(self, entity):
        self._entity = entity

    def do_kill(self):
        if self._finish_flag is True:
            return

        if self._kill_flag is False:
            # send emit first
            self._do_status_update(self.Status.Killed)
            # set flag later
            self._kill_flag = True

            self.killed.emit()

            self._stderr(
                'thread is killed at: {}\n'.format(self._entity)
            )

    def do_quit(self):
        if self._finish_flag is False:
            if self._subprocess is not None:
                self._subprocess.do_kill()

            self.quit()
            self.wait()
            self.deleteLater()

            self._stderr(
                'thread is quit at: {}\n'.format(self._entity)
            )

    def do_start(self):
        self.start()

    @staticmethod
    def generate(window, progress_bar):
        t = QtThreadWorkerForSubprocess(window, progress_bar=progress_bar)
        QtThreadWorkerForSubprocess.INDEX += 1
        t.set_entity(QtThreadWorkerForSubprocess.INDEX)
        return t

    def run(self):
        # wait
        with QtCore.QMutexLocker(self.parent()._thread_worker_mutex):
            while self.parent()._thread_worker_value >= self.parent()._thread_worker_maximum:
                self._stderr(
                    'thread is waiting at: {}\n'.format(self._entity)
                )
                self.parent()._thread_worker_condition.wait(self.parent()._thread_worker_mutex)

        # start
        self.parent()._thread_worker_value += 1
        if self._kill_flag is False:
            with QtCore.QMutexLocker(self.parent()._thread_worker_mutex):
                self._stdout(
                    'thread is started at: {}\n'.format(self._entity)
                )
                self._stdout(
                    'running thread number is: "{}"\n'.format(self.parent()._thread_worker_value)
                )

            st = time.time()

            self._do_status_update(self.Status.Started)
            self.started.emit()
            # noinspection PyBroadException
            try:
                if isinstance(self._fnc, (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)):
                    # noinspection PyArgumentList
                    self._fnc(
                        self,
                        *self._args,
                        **self._kwargs
                    )
                elif isinstance(self._fnc, six.string_types):
                    self._subprocess = _Subprocess(self, self._fnc, clear_environ='auto')
                    self._do_status_update(self.Status.Running)
                    self.running.emit()
                    self._subprocess.run()
                else:
                    raise RuntimeError()

                if self._kill_flag is False:
                    self._do_status_update(self.Status.Completed)
                    self.completed.emit()
            except Exception:
                self._stderr('thread is failed at : {}\n'.format(self._entity))
                self._do_status_update(self.Status.Failed)
                if self._subprocess is not None:
                    self.failed.emit(self._subprocess.get_results())
                else:
                    self.failed.emit([])
                bsc_core.BscException.print_stack()
            finally:
                with QtCore.QMutexLocker(self.parent()._thread_worker_mutex):
                    ct = time.time()-st
                    self._stdout(
                        'thread is finished at: {}, cost {}s\n'.format(self._entity, ct)
                    )
                    self.parent()._thread_workers.remove(self)
                    self.parent()._thread_worker_value -= 1
                    self.parent()._thread_worker_condition.wakeOne()

                # send finish finally
                self.finished.emit()
                self._finish_flag = True

        else:
            with QtCore.QMutexLocker(self.parent()._thread_worker_mutex):
                self.parent()._thread_workers.remove(self)
                self.parent()._thread_worker_value -= 1
                self.parent()._thread_worker_condition.wakeOne()

            self._stderr('thread is ignored at: {}\n'.format(self._entity))

            self.finished.emit()
            self._finish_flag = True
