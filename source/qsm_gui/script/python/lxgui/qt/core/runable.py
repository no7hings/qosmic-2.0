# coding:utf-8
from __future__ import print_function

import functools

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from .wrap import *


class QtBuildRunnableSignals(QtCore.QObject):
    cache_started = qt_signal()
    cache_finished = qt_signal()
    #
    cache_value_accepted = qt_signal(list)
    #
    run_started = qt_signal()
    run_finished = qt_signal()
    #
    run_failed = qt_signal()
    status_changed = qt_signal(int)


class QtBuildRunnable(QtCore.QRunnable):
    Status = gui_core.GuiProcessStatus

    def __init__(self, pool):
        super(QtBuildRunnable, self).__init__()

        self._pool = pool

        self._build_signals = QtBuildRunnableSignals()
        self._cache_fnc = None

        self._status = self.Status.Waiting

        self.setAutoDelete(True)

    def set_cache_fnc(self, method):
        self._cache_fnc = method

    def set_status(self, status):
        self._status = status
        self._build_signals.status_changed.emit(status)

    def do_kill(self):
        self.set_status(self.Status.Killed)

    def set_stop(self):
        self.set_status(self.Status.Stopped)

    def run(self):
        if self._status == self.Status.Waiting:
            self._build_signals.run_started.emit()
            self.set_status(self.Status.Running)
            # noinspection PyBroadException
            try:
                self._build_signals.cache_started.emit()
                cache = self._cache_fnc()
                self._build_signals.cache_finished.emit()
                # ignore when status is killed or other (not running)
                if self._status == self.Status.Running:
                    if cache is not None:
                        self._build_signals.cache_value_accepted.emit(list(cache))
            except Exception:
                self._build_signals.run_failed.emit()
                self.set_status(self.Status.Failed)
                bsc_core.Debug.trace()
            #
            finally:
                self._build_signals.run_finished.emit()
        else:
            self._build_signals.run_finished.emit()

    def do_start(self):
        self._pool.start(self)


class QtBuildRunnableStack(QtCore.QObject):
    run_started = qt_signal()
    run_finished = qt_signal()

    MAXIMUM = 4

    THREAD_POOL = QtCore.QThreadPool()
    THREAD_POOL.setMaxThreadCount(MAXIMUM)

    def __init__(self, *args, **kwargs):
        super(QtBuildRunnableStack, self).__init__(*args, **kwargs)

        self._widget = self.parent()

        self._cache_fncs = []
        self._build_fncs = []

        self._threads = []
        self._results = []

    @staticmethod
    def generate(cache_fnc, build_fnc, post_fnc=None):
        runnable = QtBuildRunnable(QtBuildRunnableStack.THREAD_POOL)
        runnable.set_cache_fnc(cache_fnc)
        runnable._build_signals.cache_value_accepted.connect(build_fnc)
        if post_fnc is not None:
            runnable._build_signals.run_finished.connect(post_fnc)
        return runnable

    def register(self, cache_fnc, build_fnc, post_fnc=None):
        thread = self.generate(cache_fnc, build_fnc, post_fnc)
        self._threads.append(thread)
        self._results.append(0)
        return thread

    def set_result_at(self, thread, result):
        index = self._threads.index(thread)
        self._results[index] = result
        if sum(self._results) == len(self._results):
            self.run_finished.emit()

    @staticmethod
    def start_runnable(runnable):
        # noinspection PyArgumentList
        QtBuildRunnableStack.THREAD_POOL.start(runnable)

    def do_kill(self):
        [i.do_kill() for i in self._threads]

    def do_quit(self):
        self.do_kill()

    def do_start(self):
        self.run_started.emit()
        c_t = None
        for i_t in self._threads:
            i_t._build_signals.run_finished.connect(
                functools.partial(self.set_result_at, i_t, 1)
            )
            #
            if c_t is None:
                i_t.do_start()
            else:
                c_t._build_signals.cache_finished.connect(i_t.do_start)
            #
            c_t = i_t


class QtVideoRunnableStack(QtCore.QObject):
    MAXIMUM = 1

    THREAD_POOL = QtCore.QThreadPool()
    THREAD_POOL.setMaxThreadCount(MAXIMUM)

    @classmethod
    def generate(cls, cache_fnc, build_fnc, post_fnc=None):
        runnable = QtBuildRunnable(QtVideoRunnableStack.THREAD_POOL)
        runnable.set_cache_fnc(cache_fnc)
        runnable._build_signals.cache_value_accepted.connect(build_fnc)
        if post_fnc is not None:
            runnable._build_signals.run_finished.connect(post_fnc)
        return runnable
