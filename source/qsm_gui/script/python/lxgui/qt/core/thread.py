# coding:utf-8
import functools

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from .wrap import *


class QtActionSignals(QtCore.QObject):
    dict_accepted = qt_signal(dict)
    str_accepted = qt_signal(str)


class QtPrintSignals(QtCore.QObject):
    added = qt_signal(str)
    overed = qt_signal(str)
    #
    print_add_accepted = qt_signal(str)
    print_over_accepted = qt_signal(str)


class QtMethodSignals(QtCore.QObject):
    stated = qt_signal()
    running = qt_signal()
    stopped = qt_signal()
    #
    completed = qt_signal()
    error_occurred = qt_signal()


class QtCommandSignals(QtCore.QObject):
    completed = qt_signal(tuple)
    failed = qt_signal(tuple)
    #
    finished = qt_signal(tuple)


class QtMethodThread(QtCore.QThread):
    run_started = qt_signal()
    run_finished = qt_signal()
    #
    completed = qt_signal()
    failed = qt_signal(str)
    error_occurred = qt_signal()
    #
    start_accepted = qt_signal(QtCore.QObject)
    finish_accepted = qt_signal(QtCore.QObject)

    def __init__(self, *args, **kwargs):
        super(QtMethodThread, self).__init__(*args, **kwargs)
        self._methods = []

    def append_method(self, method):
        self._methods.append(method)

    def run(self):
        self.run_started.emit()
        self.start_accepted.emit(self)
        # noinspection PyBroadException
        try:
            for i in self._methods:
                i()
            #
            self.completed.emit()
        except Exception:
            bsc_core.BscException.set_print()
            self.failed.emit(bsc_core.BscException.get_stack_())
        finally:
            self.run_finished.emit()
            self.finish_accepted.emit(self)

    def do_quit(self):
        self.quit()
        self.wait()
        self.deleteLater()


class QtBuildThread(QtCore.QThread):
    run_started = qt_signal()
    run_finished = qt_signal()
    #
    cache_started = qt_signal()
    cache_finished = qt_signal()
    #
    cache_value_accepted = qt_signal(list)
    #
    start_accepted = qt_signal(QtCore.QObject)
    finish_accepted = qt_signal(QtCore.QObject)
    #
    run_failed = qt_signal()
    #
    status_changed = qt_signal(int)
    #
    Status = gui_core.GuiProcessStatus

    def __init__(self, *args, **kwargs):
        super(QtBuildThread, self).__init__(*args, **kwargs)
        self._cache_fnc = None
        self._is_killed = False

        self._status = self.Status.Waiting

    def set_cache_fnc(self, method):
        self._cache_fnc = method

    def do_kill(self):
        self._status = self.Status.Killed

    def set_status(self, status):
        self._status = status
        self.status_changed.emit(status)

    def do_quit(self):
        self.do_kill()
        self.quit()
        self.wait()
        self.deleteLater()

    def run(self):
        if self._status == self.Status.Waiting:
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
                    if cache is not None:
                        self.cache_value_accepted.emit(list(cache))
            except Exception:
                self.run_failed.emit()
                self.set_status(self.Status.Failed)
                print 'thread failed'
                bsc_core.BscException.print_stack()
            #
            finally:
                self.run_finished.emit()
                self.finish_accepted.emit(self)
                self.set_status(self.Status.Finished)


class QtBuildThreadStack(QtCore.QObject):
    run_started = qt_signal()
    run_finished = qt_signal()
    run_resulted = qt_signal(list)
    Status = gui_core.GuiProcessStatus

    def __init__(self, *args, **kwargs):
        super(QtBuildThreadStack, self).__init__(*args, **kwargs)
        #
        self._widget = self.parent()

        self._threads = []
        self._results = []

        self._status = self.Status.Waiting
        self._sub_statuses = []

        self._thread_mutex = QtCore.QMutex()
        self._thread_maximum = 8
        self._item_count = 0

    def generate(self, cache_fnc, build_fnc, previous_fnc=None, post_fnc=None):
        thread = QtBuildThread(self._widget)
        thread.set_cache_fnc(cache_fnc)
        thread.cache_value_accepted.connect(build_fnc)
        thread.start_accepted.connect(self.start_accept_fnc)
        thread.finish_accepted.connect(self.finish_accept_fnc)
        self._results.append(0)
        self._sub_statuses.append(self.Status.Waiting)
        if previous_fnc is not None:
            thread.run_started.connect(previous_fnc)
        if post_fnc is not None:
            thread.run_finished.connect(post_fnc)
        return thread

    def register(self, cache_fnc, build_fnc, previous_fnc=None, post_fnc=None):
        thread = self.generate(cache_fnc, build_fnc, previous_fnc, post_fnc)
        self._threads.append(thread)
        return thread

    def start_accept_fnc(self, thread):
        index = self._threads.index(thread)
        self._sub_statuses[index] = self.Status.Running

    def finish_accept_fnc(self, thread):
        if thread in self._threads:
            index = self._threads.index(thread)
            self._sub_statuses[index] = self.Status.Finished
            self._results[index] = 1
            if len(self._results) == sum(self._results):
                self.run_finished.emit()

    def do_kill(self):
        [i.do_kill() for i in self._threads]
        # self._mutex.unlock()

    def do_quit(self):
        self.do_kill()
        for seq, i in enumerate(self._threads):
            i.quit()
            i.wait()
            i.deleteLater()
            # release
            del self._threads[seq]

    def do_start(self):
        self._status = self.Status.Running
        self.run_started.emit()
        c_t = None
        # running one by one for keep the order
        for i_t in self._threads:
            if c_t is None:
                i_t.start()
            else:
                c_t.cache_finished.connect(i_t.start)
            #
            c_t = i_t


class QtBuildThreadExtra(QtBuildThread):
    MUTEX = QtCore.QMutex()
    MAXIMUM = 1
    COUNT = 0

    def __init__(self, *args, **kwargs):
        super(QtBuildThreadExtra, self).__init__(*args, **kwargs)

    def run(self):
        QtBuildThreadExtra.MUTEX.lock()
        QtBuildThreadExtra.COUNT += 1
        super(QtBuildThreadExtra, self).run()
        QtBuildThreadExtra.COUNT -= 1
        QtBuildThreadExtra.MUTEX.unlock()

    def do_quit(self):
        super(QtBuildThreadExtra, self).do_quit()
        QtBuildThreadExtra.MUTEX.unlock()


class QtItemSignals(
    QtCore.QObject
):
    visible = qt_signal(bool)
    expanded = qt_signal(bool)
    #
    pressed = qt_signal(object, int)
    #
    press_dbl_clicked = qt_signal(object, int)
    press_clicked = qt_signal(object, int)
    #
    check_clicked = qt_signal(object, int)
    check_toggled = qt_signal(object, int, bool)

    user_check_clicked = qt_signal(object, int)
    user_check_toggled = qt_signal(object, int, bool)
    #
    drag_pressed = qt_signal(tuple)
    drag_move = qt_signal(tuple)
    drag_released = qt_signal(tuple)
