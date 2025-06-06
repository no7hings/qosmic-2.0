# coding:utf-8
import time

import sys

import lxbasic.core as bsc_core
# qt
from .wrap import *


class QtThreadWorkerForBuild(QtCore.QThread):
    run_started = qt_signal()
    run_finished = qt_signal()

    cache_started = qt_signal()
    cache_finished = qt_signal()

    cache_value_accepted = qt_signal(list)

    start_accepted = qt_signal(QtCore.QObject)
    finish_accepted = qt_signal(QtCore.QObject)

    run_failed = qt_signal()

    status_changed = qt_signal(int)

    Status = bsc_core.BasProcessStatus

    VERBOSE = False

    def __init__(self, *args, **kwargs):
        super(QtThreadWorkerForBuild, self).__init__(*args, **kwargs)

        self.parent()._thread_workers.append(self)

        self._entity = 0
        self._cache_fnc = None
        self._kill_flag = False

        self._status = self.Status.Waiting

    def set_cache_fnc(self, method):
        self._cache_fnc = method

    def set_entity(self, entity):
        self._entity = entity

    def _stdout(self, text):
        if self.VERBOSE is True:
            sys.stdout.write(text)

    def _stderr(self, text):
        if self.VERBOSE is True:
            sys.stderr.write(text)

    def do_kill(self):
        self._status = self.Status.Killed
        self._kill_flag = True

    def do_quit(self):
        self._stdout(
            'quit thread: {}\n'.format(self._entity)
        )
        self.do_kill()

        self.wait()
        self.quit()
        self.deleteLater()

    def do_start(self):
        self.start()

    def set_status(self, status):
        self._status = status
        self.status_changed.emit(status)

    def _check_parent_busy(self):
        value = self.parent()._thread_worker_value
        maximum = self.parent()._thread_worker_maximum
        self._stdout(
            'thread status: {}/{}\n'.format(value, maximum)
        )
        # if value > 0:
        #     self.parent().setCursor(QtCore.Qt.BusyCursor)
        # else:
        #     self.parent().unsetCursor()
        # print maximum, value
        # self.parent().setCursor(QtCore.Qt.BusyCursor)
        # self.parent().unsetCursor()

    @staticmethod
    def generate(widget):
        t = QtThreadWorkerForBuild(widget)
        t.run_started.connect(t._check_parent_busy)
        t.run_finished.connect(t._check_parent_busy)
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

            self.run_started.emit()
            self.start_accepted.emit(self)
            self.set_status(self.Status.Running)
            # noinspection PyBroadException
            try:
                self.cache_started.emit()
                cache = self._cache_fnc()
                self.cache_finished.emit()
                # ignore when status is killed or other (not running)
                if self._status == self.Status.Running:
                    self.cache_value_accepted.emit(list(cache))
            except Exception:
                self._stderr('thread is failed at: {}\n'.format(self._entity))
                self.run_failed.emit()
                self.set_status(self.Status.Failed)
                bsc_core.Debug.trace()
            #
            finally:
                with QtCore.QMutexLocker(self.parent()._thread_worker_mutex):
                    ct = time.time()-st
                    self._stdout(
                        'thread is finished at: {}, cost {}s\n'.format(self._entity, ct)
                    )
                    # may remove when close
                    if self in self.parent()._thread_workers:
                        self.parent()._thread_workers.remove(self)
                        self.parent()._thread_worker_value -= 1
                    self.parent()._thread_worker_condition.wakeOne()

                self.run_finished.emit()
                self.finish_accepted.emit(self)
                self.set_status(self.Status.Finished)
        else:
            with QtCore.QMutexLocker(self.parent()._thread_worker_mutex):
                # may remove when close
                if self in self.parent()._thread_workers:
                    self.parent()._thread_workers.remove(self)
                    self.parent()._thread_worker_value -= 1
                self.parent()._thread_worker_condition.wakeOne()

            self._stderr('thread is ignored at: {}\n'.format(self._entity))
