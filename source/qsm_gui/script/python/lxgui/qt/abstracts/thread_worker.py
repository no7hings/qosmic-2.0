# coding=utf-8
# qt
from ..core.wrap import *

from .. import core as _qt_core


class AbsQtThreadWorkerExtraDef(object):
    def _init_thread_worker_extra_def_(self, widget):
        self._widget = widget

        self._thread_worker_mutex = QtCore.QMutex()
        self._thread_worker_condition = QtCore.QWaitCondition()

        self._thread_worker_maximum = 16
        self._thread_worker_value = 0

        self._thread_workers = []

        self._thread_terminate_flag = False

    def _do_kill_all_thread_workers_(self):
        for seq, i_thread in enumerate(self._thread_workers):
            i_thread.do_quit()
            # del self._thread_workers[seq]
        self._thread_worker_value = 0
        self._thread_workers = []

    def _thread_lock_(self):
        self._thread_worker_mutex.lock()

    def _thread_unlock_(self):
        self._thread_worker_mutex.unlock()

    def _generate_thread_(self, cache_fnc, build_fnc, post_fnc=None, previous_fnc=None):
        t = _qt_core.QtThreadWorkerForBuild.generate(self._widget)
        t.set_cache_fnc(cache_fnc)
        t.cache_value_accepted.connect(build_fnc)
        if post_fnc is not None:
            t.run_finished.connect(post_fnc)
        if previous_fnc is not None:
            t.run_started.connect(previous_fnc)
        return t

