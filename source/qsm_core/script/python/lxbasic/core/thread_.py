# coding:utf-8
import sys

import six

import threading

import subprocess

import functools

from . import base as _base

from . import configure as _configure

from . import process as _process


class TrdFnc(threading.Thread):
    THREAD_MAXIMUM = threading.Semaphore(1024)

    def __init__(self, fnc, *args, **kwargs):
        threading.Thread.__init__(self)
        self._fnc = fnc
        self._args = args
        self._kwargs = kwargs

    def run(self):
        TrdFnc.THREAD_MAXIMUM.acquire()
        self._fnc(*self._args, **self._kwargs)
        TrdFnc.THREAD_MAXIMUM.release()


class TrdSignal(object):
    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        self._fncs = []

    def connect_to(self, fnc):
        self._fncs.append(fnc)

    def send_emit(self, *args, **kwargs):
        if self._fncs:
            ts = [threading.Thread(target=i, args=args, kwargs=kwargs) for i in self._fncs]
            for t in ts:
                t.start()
            for t in ts:
                t.join()


class TrdCommandPool(threading.Thread):
    STACK = []
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
                self._index, status
            )

    def _do_completed(self, results):
        if self._kill_flag is False:
            self._signal_completed.send_emit(
                self._index, results
            )

    def _do_failed(self, results):
        if self._kill_flag is False:
            self._signal_failed.send_emit(
                self._index, results
            )

    def _do_started(self):
        if self._kill_flag is False:
            self._signal_started.send_emit(
                self._index
            )

    def _do_finished(self, status, results):
        if self._kill_flag is False:
            self._signal_finished.send_emit(
                self._index, status, results
            )

    def __init__(self, cmd, index=0):
        threading.Thread.__init__(self)
        self._cmd = cmd
        self._index = index

        self._kill_flag = False

        self._signal_status_changed = TrdSignal(object, int)
        self._signal_completed = TrdSignal(object, list)
        self._signal_failed = TrdSignal(object, list)
        self._signal_started = TrdSignal(object)
        self._signal_finished = TrdSignal(object, int, list)

        self._status = self.Status.Unknown

        self._options = {}

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

    def run(self):
        if self._kill_flag is True:
            return

        self._do_update_status(self.Status.Running)

        status = self.Status.Running
        return_dicts = []
        try:
            # single process
            if isinstance(self._cmd, six.string_types):
                return_dict = {}
                return_dicts.append(return_dict)
                _process.BscProcess.execute_as_block(
                    self._cmd, clear_environ='auto', return_dict=return_dict
                )
                status = self.Status.Completed
            # many process execute one by one
            elif isinstance(self._cmd, (set, tuple, list)):
                for i_cmd in self._cmd:
                    i_return_dict = {}
                    return_dicts.append(i_return_dict)
                    _process.BscProcess.execute_as_block(
                        i_cmd, clear_environ='auto', return_dict=i_return_dict
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
            #
            self._do_finished(self._status, results)

            TrdCommandPool.LOCK.acquire()
            TrdCommandPool.STACK.remove(self)
            # unlock
            if len(TrdCommandPool.STACK) < TrdCommandPool.MAXIMUM:
                TrdCommandPool.EVENT.set()
                TrdCommandPool.EVENT.clear()

            TrdCommandPool.LOCK.release()

    @staticmethod
    def is_busy():
        return len(TrdCommandPool.STACK) >= TrdCommandPool.MAXIMUM

    @staticmethod
    def do_pool_wait():
        TrdCommandPool.LOCK.acquire()
        # lock
        if TrdCommandPool.is_busy() is True:
            TrdCommandPool.LOCK.release()
            TrdCommandPool.EVENT.wait()
        else:
            TrdCommandPool.LOCK.release()

    @staticmethod
    def set_start(cmd, index=0):
        TrdCommandPool.LOCK.acquire()
        t = TrdCommandPool(cmd, index)
        TrdCommandPool.STACK.append(t)
        TrdCommandPool.LOCK.release()
        t.start()
        return t

    @staticmethod
    def generate(cmd, index=0):
        TrdCommandPool.LOCK.acquire()
        t = TrdCommandPool(cmd, index)
        TrdCommandPool.STACK.append(t)
        TrdCommandPool.LOCK.release()
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

    def do_wait(self):
        self._do_update_status(self.Status.Waiting)
        self.do_pool_wait()

    def do_wait_for_start(self):
        self.do_wait()
        self._do_started()
        self._do_update_status(self.Status.Started)
        self.start()

    def do_start(self):
        self._do_started()
        self._do_update_status(self.Status.Started)
        self.start()


class TrdCommand(threading.Thread):
    Status = _configure.BasProcessStatus

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self._cmd = cmd
        #
        self._status = self.Status.Started
        #
        self.__is_killed = False
        self.__is_stopped = False
        #
        self._signal_status_changed = TrdSignal(int)
        self._logging_signal = TrdSignal(str)
        #
        self._signal_completed = TrdSignal(tuple)
        self._signal_failed = TrdSignal(tuple)
        self._signal_finished = TrdSignal(tuple)

    def _do_update_status(self, status):
        self._status = status
        self._signal_status_changed.send_emit(
            status
        )

    def _do_completed(self, results):
        self._signal_completed.send_emit(
            (self._status, results)
        )

    def _do_failed(self, results):
        self._signal_failed.send_emit(
            (self._status, results)
        )

    def _do_finished(self, results):
        self._signal_finished.send_emit(
            (self._status, results)
        )

    def __set_logging(self, text):
        self._logging_signal.send_emit(
            text
        )

    @property
    def status_changed(self):
        return self._signal_status_changed

    @property
    def completed(self):
        return self._signal_completed

    @property
    def failed(self):
        return self._signal_failed

    @property
    def finished(self):
        return self._signal_finished

    @property
    def logging(self):
        return self._logging_signal

    def get_status(self):
        return self._status

    def set_stopped(self):
        self.__is_stopped = True

    def do_kill(self):
        self.__is_killed = True

    def run(self):
        self._do_update_status(self.Status.Running)
        results = []
        s_p = subprocess.Popen(
            self._cmd,
            shell=True,
            # close_fds=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            startupinfo=_process.BscProcess.NO_WINDOW
        )

        while True:
            next_line = s_p.stdout.readline()
            #
            return_line = next_line
            if return_line == '' and s_p.poll() is not None:
                break
            #
            return_line = return_line.decode('utf-8', 'ignore')
            return_line = return_line.replace(u'\u2018', "'").replace(u'\u2019', "'")

            log = return_line.encode('utf-8').rstrip()
            results.append(log)
            #
            if self.__is_stopped is True:
                s_p.kill()
                self._do_failed(results)
                self._do_finished(results)
                return False
            if self.__is_killed is True:
                s_p.kill()
                self.__set_logging('process is killed')
                self._do_update_status(self.Status.Killed)
                #
                self._do_failed(results)
                self._do_finished(results)
                return False
            #
            self.__set_logging(
                log
            )

        retcode = s_p.poll()
        if retcode:
            self._do_update_status(self.Status.Failed)
            self._do_failed(results)
            self._do_finished(results)
            return False
        #
        s_p.stdout.close()
        self._do_update_status(self.Status.Completed)
        self._do_completed(results)
        self._do_finished(results)
        return True


class TrdMethod(threading.Thread):
    STACK = []
    MAXIMUM = 256
    EVENT = threading.Event()
    LOCK = threading.Lock()
    #
    Status = _configure.BasProcessStatus

    def __init__(self, fnc, index, *args, **kwargs):
        threading.Thread.__init__(self)
        self._fnc = fnc
        self._args = args
        self._kwargs = kwargs
        #
        self._index = index

        self._status = self.Status.Started

        self._signal_status_changed = TrdSignal(int, int)
        self._signal_completed = TrdSignal(int, list)
        self._signal_failed = TrdSignal(int, list)
        self._signal_finished = TrdSignal(int, int, list)

    @property
    def status_changed(self):
        return self._signal_status_changed

    @property
    def completed(self):
        return self._signal_completed

    @property
    def failed(self):
        return self._signal_failed

    @property
    def finished(self):
        return self._signal_finished

    def run(self):
        self._do_update_status(self.Status.Running)
        results = []
        try:
            results = self._fnc(*self._args, **self._kwargs) or []
            self._do_update_status(self.Status.Completed)
            self._do_completed(results)
        except subprocess.CalledProcessError as _exc:
            # o = exc.output
            # s = exc.returncode
            results = []
            self._do_update_status(self.Status.Failed)
            self._do_failed(results)
        finally:
            TrdMethod.LOCK.acquire()
            TrdMethod.STACK.remove(self)
            # unlock
            if len(TrdMethod.STACK) < TrdMethod.MAXIMUM:
                TrdMethod.EVENT.set()
                TrdMethod.EVENT.clear()

            TrdMethod.LOCK.release()

            self._do_finished(self._status, results)

    @staticmethod
    def is_busy():
        return len(TrdMethod.STACK) >= TrdMethod.MAXIMUM

    @staticmethod
    def do_pool_wait():
        TrdMethod.LOCK.acquire()
        # lock
        if len(TrdMethod.STACK) >= TrdMethod.MAXIMUM:
            TrdMethod.LOCK.release()
            TrdMethod.EVENT.wait()
        else:
            TrdMethod.LOCK.release()

    @staticmethod
    def set_start(fnc, index, *args, **kwargs):
        TrdMethod.LOCK.acquire()
        t = TrdMethod(fnc, index, *args, **kwargs)
        TrdMethod.STACK.append(t)
        TrdMethod.LOCK.release()
        t.start()
        return t

    def _do_completed(self, results):
        self._signal_completed.send_emit(
            self._index, results
        )

    def _do_failed(self, results):
        self._signal_failed.send_emit(
            self._index, results
        )

    def _do_finished(self, status, results):
        self._signal_finished.send_emit(
            self._index, status, results
        )

    def _do_update_status(self, status):
        self._status = status
        self._signal_status_changed.send_emit(
            self._index, status
        )

    def get_status(self):
        return self._status


class TrdFunction(TrdMethod):
    MAXIMUM = 6

    def __init__(self, fnc, index, *args, **kwargs):
        super(TrdFunction, self).__init__(fnc, index, *args, **kwargs)


class TrdFncsChainPool(object):
    class Trd(threading.Thread):
        def __init__(self, index, fnc):
            threading.Thread.__init__(self)
            self._index = index
            self._fnc = fnc

            self.__started_signal = TrdSignal()
            self._signal_finished = TrdSignal()
            self._signal_failed = TrdSignal(str)

            self._kill_flag = False

        def run(self):
            if self._kill_flag is True:
                return

            self.__started()
            # noinspection PyBroadException
            try:
                self._fnc()
            except Exception:
                text = _base.Debug.get_error_stack()
                if text:
                    self.__failed(text)
            finally:
                self.__finished()

        def __started(self):
            if self._kill_flag is True:
                return

            self.__started_signal.send_emit()

        def connect_started_to(self, fnc):
            self.__started_signal.connect_to(fnc)

        def __finished(self):
            if self._kill_flag is True:
                return

            self._signal_finished.send_emit()

        def connect_finished_to(self, fnc):
            self._signal_finished.connect_to(fnc)

        def __failed(self, text):
            if self._kill_flag is True:
                return
            self._signal_failed.send_emit(text)

        def connect_failed_to(self, fnc):
            self._signal_failed.connect_to(fnc)

        @classmethod
        def start_loop(cls, threads):
            t_cur = None
            for i_t in threads:
                if t_cur is not None:
                    t_cur.connect_finished_to(i_t.start)
                t_cur = i_t

            threads[0].start()

        def do_kill(self):
            self._kill_flag = True

    def __init__(self):
        self._threads = []
        self._next_fncs = []
        self._maximum = 0

        self._all_finish_signal = TrdSignal(int)

    def add_next_fnc(self, fnc):
        self._next_fncs.append(fnc)

    def create_one(self, fnc):
        index = len(self._threads)
        thread = TrdFncsChainPool.Trd(
            index, fnc
        )
        thread.connect_finished_to(
            functools.partial(self.__update_finish, index)
        )
        self._threads.append(thread)
        return thread

    def start_all(self):
        t_cur = None
        self._maximum = len(self._threads)-1
        for i_t in self._threads:
            if t_cur is not None:
                t_cur.connect_finished_to(i_t.start)
            t_cur = i_t

        self._threads[0].start()

    def kill_all(self):
        for i_index, i in enumerate(self._threads):
            i.do_kill()
            del self._threads[i_index]

    def __update_finish(self, index):
        if index == self._maximum:
            self._all_finish_signal.send_emit()

    def connect_all_finish_to(self, fnc):
        self._all_finish_signal.connect_to(fnc)


class TrdGainSignal(object):
    THREAD_MAXIMUM = threading.Semaphore(1024)

    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        self._methods = []

    def connect_to(self, method):
        self._methods.append(method)

    def send_emit(self, *args, **kwargs):
        if self._methods:
            TrdGainSignal.THREAD_MAXIMUM.acquire()
            #
            ts = [threading.Thread(target=i_method, args=args, kwargs=kwargs) for i_method in self._methods]
            for t in ts:
                t.start()
            for t in ts:
                t.join()
            #
            TrdGainSignal.THREAD_MAXIMUM.release()


class TrdGain(threading.Thread):
    THREAD_MAXIMUM = threading.Semaphore(1024)

    def __init__(self):
        super(TrdGain, self).__init__()
        #
        self.run_started = TrdGainSignal()
        self.run_finished = TrdGainSignal()
        #
        self.__fnc = None
        #
        self.__data = None

    def connect_to(self, fnc):
        self.__fnc = fnc

    def __gain_fnc(self, data):
        self.__data = data
        self.run_finished.send_emit()

    def get_data(self):
        return self.__data

    def run(self):
        TrdGain.THREAD_MAXIMUM.acquire()

        self.run_started.send_emit()

        self.__gain_fnc(
            self.__fnc()
        )

        TrdGain.THREAD_MAXIMUM.release()


class TrdGainStack(object):
    def __init__(self):
        self.run_started = TrdGainSignal()
        self.run_finished = TrdGainSignal()

        self.__fncs = []
        self._item_count = 0
        self.__count_finish = 0
        self.__result_dict = {}

        self.__data = []

    def get_data(self):
        return self.__data

    def register(self, fnc):
        index = len(self.__fncs)
        self.__fncs.append(fnc)
        self.__data.append(None)
        self.__result_dict[index] = False
        self._item_count += 1

    def __gain_fnc(self, thread, index):
        self.__data[index] = thread.get_data()
        self.__result_dict[index] = True

        self.__count_finish += 1

        if self.__count_finish == self._item_count:
            self.run_finished.send_emit()

    def start(self):
        c = len(self.__fncs)
        self.run_started.send_emit()

        ts = []

        for i_index in range(c):
            i_fnc = self.__fncs[i_index]

            i_t = TrdGain()
            ts.append(i_t)
            i_t.connect_to(i_fnc)
            i_t.run_finished.connect_to(
                functools.partial(self.__gain_fnc, i_t, i_index)
            )

            i_t.start()

        [i.join() for i in ts]


class TrdProcessMonitor(object):
    Status = _configure.BasProcessStatus

    def __init__(self, process):
        self._process = process
        self._name = process.get_name()
        self._elements = process.get_elements()
        #
        self._time_interval = .5
        self._processing_time_cost = 0
        self._running_time_cost = 0
        self._waiting_time_cost = 0
        self._processing_time_maximum = 3600
        self._running_time_maximum = 3600
        self._waiting_time_maximum = 3600
        #
        self._is_disable = True
        #
        self._timer = None
        self._status = self.Status.Stopped
        self._sub_process_statuses = [self.Status.Stopped]*len(self._elements)
        #
        self.logging = TrdSignal(str)
        self.status_changed = TrdSignal(int)
        self.element_statuses_changed = TrdSignal(int)
        self.started = TrdSignal()
        self.waiting = TrdSignal(int)
        self.running = TrdSignal(int)
        self.processing = TrdSignal(int)
        self.suspended = TrdSignal()
        self.completed = TrdSignal()
        self.failed = TrdSignal()
        self.stopped = TrdSignal()
        self.error_occurred = TrdSignal(int)
        #
        self._status_update_methods = [
            # Unknown = 0
            self.__set_stopped_,
            # Started = 1
            self.__set_started_,
            # Running = 2
            self.__set_running_,
            # Waiting = 3
            self.__set_waiting_,
            # Completed = 4
            self.__set_completed_,
            # Suspended = 5
            self.__set_suspended_,
            # Failed = 6
            self.__set_failed_,
            # Stopped = 7
            self.__set_stopped_,
            # Error = 8
            self.__set_error_occurred_
        ]

    def __set_status_update_method_run_(self):
        return self._status_update_methods[self._process.get_status()]()

    def __set_started_(self):
        self._is_disable = False
        #
        self._status = self.Status.Started
        #
        self.__set_emit_send_(self.started)
        #
        self.__set_processing_time_update_()
        #
        self.__set_logging_(
            'process-name="{}" is started'.format(
                self._name
            )
        )

    def __set_emit_send_(self, signal, *args, **kwargs):
        # noinspection PyBroadException
        # signal.send_emit(*args, **kwargs)
        try:
            signal.send_emit(*args, **kwargs)
        except Exception:
            self.__set_error_occurred_()
            raise

    # waiting
    def __set_waiting_(self):
        self._status = self.Status.Waiting
        #
        self.__set_emit_send_(self.waiting, self._waiting_time_cost)
        self.__set_emit_send_(self.processing, self._processing_time_cost)
        #
        self.__set_processing_time_update_()
        self.__set_waiting_time_update_()

    # running
    def __set_running_(self):
        self._status = self.Status.Running
        #
        self.__set_emit_send_(self.running, self._running_time_cost)
        self.__set_emit_send_(self.processing, self._processing_time_cost)
        #
        self.__set_processing_time_update_()
        self.__set_running_time_update_()

    def __set_elements_running_(self):
        pre_element_status = str(self._sub_process_statuses)
        for index, i_element in enumerate(self._elements):
            i_element_status = i_element.get_status()
            if i_element_status is self.Status.Error:
                pass
            self._sub_process_statuses[index] = i_element_status
        if pre_element_status != str(self._sub_process_statuses):
            self.__set_element_statuses_changed_()

    def __set_logging_(self, text):
        sys.stdout.write(text+'\n')
        self.__set_emit_send_(self.logging, text)

    # status changed
    def __set_status_changed_(self):
        self.__set_emit_send_(self.status_changed, self._status)

    def __set_element_statuses_changed_(self):
        self.__set_emit_send_(self.element_statuses_changed, self._sub_process_statuses)

    def __set_suspended_(self):
        self._status = self.Status.Suspended
        #
        self.__set_emit_send_(self.suspended)
        #
        self.__set_logging_(
            'process-name="{}" is suspended'.format(
                self._name
            )
        )

    def __set_completed_(self):
        self._status = self.Status.Completed
        #
        self.__set_emit_send_(self.completed)
        #
        self.__set_logging_(
            'process-name="{}" is completed'.format(
                self._name
            )
        )

    def __set_failed_(self):
        self._is_disable = True
        #
        self._status = self.Status.Failed
        #
        self.__set_emit_send_(self.failed)
        #
        self.__set_logging_(
            'process-name="{}" is failed'.format(
                self._name
            )
        )

    def __set_stopped_(self):
        self._is_disable = True
        #
        self._status = self.Status.Stopped
        self._sub_process_statuses = [self.Status.Stopped]*len(self._elements)
        #
        self.__set_emit_send_(self.stopped)
        #
        self.__set_logging_(
            'process-name="{}" is stopped'.format(
                self._name
            )
        )

    def __set_error_occurred_(self):
        self._is_disable = True
        #
        self._status = self.Status.Error
        #
        self.__set_logging_(
            'process-name="{}" is error'.format(
                self._name
            )
        )

    def __set_run_(self):
        if self._is_disable is False:
            pre_process_status = self._status
            #
            self.__set_status_update_method_run_()
            #
            if pre_process_status != self._status:
                self.__set_status_changed_()
            #
            self.__set_elements_running_()

    def __set_processing_time_update_(self):
        self._processing_time_cost += self._time_interval
        if self._processing_time_cost >= self._processing_time_maximum:
            self.__set_logging_(
                'process-name="{}" is timeout'.format(
                    self._name
                )
            )
            self.__set_error_occurred_()
            return False
        #
        if self._timer is not None:
            self._timer.cancel()
        self._timer = threading.Timer(self._time_interval, self.__set_run_)
        self._timer.start()
        # self._timer.join()

    def __set_waiting_time_update_(self):
        self._waiting_time_cost += self._time_interval
        if self._waiting_time_cost >= self._waiting_time_maximum:
            self.__set_logging_(
                'process-name="{}" waiting is timeout'.format(
                    self._name
                )
            )
            self.__set_error_occurred_()
            return False

    def __set_running_time_update_(self):
        self._running_time_cost += self._time_interval
        if self._running_time_cost >= self._running_time_maximum:
            self.__set_logging_(
                'process-name="{}" running is timeout'.format(
                    self._name
                )
            )
            self.__set_error_occurred_()
            return False

    def get_running_time_maximum(self):
        return self._running_time_maximum

    def do_start(self):
        self.__set_started_()
        self.__set_status_changed_()

    def set_stop(self):
        self.__set_stopped_()
        #
        self.__set_status_changed_()
        self.__set_element_statuses_changed_()

    def get_is_started(self):
        return self._status == self.Status.Started

    def get_is_running(self):
        return self._status == self.Status.Running

    def get_is_completed(self):
        return self._status == self.Status.Completed

    def get_is_stopped(self):
        return self._status == self.Status.Stopped

    def get_running_time_cost(self):
        return self._running_time_cost

    def get_status(self):
        return self._status

    def get_element_statuses(self):
        return self._sub_process_statuses
