# coding:utf-8
from __future__ import print_function

import os

import six

import re

import sys

import time

import types

import platform

import getpass

import datetime

from ..wrap import *

from . import bridge as _bridge


class LogBase:
    LOG_ROOT_KEY = 'QSM_LOG_ROOT'
    DATE_TAG_FORMAT = '%Y_%m%d'

    TIME_TAG_FORMAT = '%Y_%m%d_%H%M_%S_%f'

    @staticmethod
    def ensure_string(s):
        if isinstance(s, six.text_type):
            if six.PY2:
                return s.encode('utf-8')
        elif isinstance(s, six.binary_type):
            if six.PY3:
                return s.decode('utf-8')
        return s

    @staticmethod
    def generate_timestamp():
        return time.time()

    @staticmethod
    def second_to_time_args(second):
        h = int(int(second)/3600.0)
        m = int(int(second)/60.0-60.0*h)
        s = float(second-3600.0*h-60.0*m)
        return h, m, s

    @classmethod
    def second_to_time_prettify(cls, second, mode=0):
        h, m, s = cls.second_to_time_args(second)
        if mode == 0:
            return '%02d:%02d:%07.4f'%(h, m, s)
        return '%02d:%02d:%02d'%(h, m, s)

    @classmethod
    def get_date_tag(cls):
        timestamp = time.time()
        return time.strftime(
            cls.DATE_TAG_FORMAT,
            time.localtime(timestamp)
        )

    @classmethod
    def get_time_tag(cls):
        return datetime.datetime.now().strftime(
            cls.TIME_TAG_FORMAT
        )

    @classmethod
    def get_user_name(cls):
        return getpass.getuser()

    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'

    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'

    @classmethod
    def get_windows_user_directory(cls):
        return '{}{}/.qosmic'.format(
            os.environ.get('HOMEDRIVE', 'c:'),
            os.environ.get('HOMEPATH', '/temp')
        ).replace('\\', '/')

    @classmethod
    def get_linux_user_directory(cls):
        return '{}/.qosmic'.format(
            os.environ.get('HOME', '/temp')
        )

    @classmethod
    def get_user_directory(cls):
        if cls.get_is_windows():
            return cls.get_windows_user_directory()
        elif cls.get_is_linux():
            return cls.get_linux_user_directory()
        raise SystemError()

    @classmethod
    def get_user_debug_directory(cls, tag, create=False):
        root = os.environ.get(cls.LOG_ROOT_KEY)
        if root:
            if os.path.exists(root):
                variants = dict(
                    root=root,
                    tag=tag,
                    date_tag=cls.get_date_tag(),
                    user=cls.get_user_name()
                )
                _ = '{root}/debug/{user}/{date_tag}/{tag}'.format(**variants)
                if create is True:
                    if os.path.exists(_) is False:
                        os.makedirs(_)
                return _

        root = cls.get_user_directory()
        _ = '{root}/debug/{date_tag}/{tag}'.format(
            root=root,
            date_tag=cls.get_date_tag(),
            tag=tag
        )
        if create is True:
            if os.path.exists(_) is False:
                os.makedirs(_)
        return _

    @classmethod
    def get_user_debug_file(cls, tag, create=False):
        directory_path = cls.get_user_debug_directory(tag, create=create)
        return '{}/{}.log'.format(
            directory_path, cls.get_time_tag()
        )


class Log:
    DEFAULT_CODING = sys.getdefaultencoding()

    FILE_SYSTEM_CODING = sys.getfilesystemencoding()

    # sys.stdout.write(
    #     'logger is initialization, default coding is "{}"'.format(DEFAULT_CODING)+'\n'
    # )

    ENABLE = True

    RESULT_ENABLE = True
    WARNING_ENABLE = True
    ERROR_ENABLE = True

    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    DATE_TAG_FORMAT = '%Y_%m%d'

    DEBUG = False
    TEST = False

    TIMESTAMP = None
    TIMESTAMP_CACHE = dict()

    LEVEL = 3

    @classmethod
    def set_level(cls, level):
        pass

    @classmethod
    def get_time(cls):
        return time.strftime(cls.TIME_FORMAT, time.localtime(time.time()))

    @classmethod
    def get(cls, text):
        return '{} {}'.format(cls.get_time(), ensure_string(text))

    @classmethod
    def get_result(cls, text):
        return cls.get('''        | {}'''.format(ensure_string(text)))

    @classmethod
    def get_warning(cls, text):
        return cls.get('''warning | {}'''.format(ensure_string(text)))

    @classmethod
    def get_error(cls, text):
        return cls.get('''  error | {}'''.format(ensure_string(text)))

    @classmethod
    def get_debug(cls, text):
        return cls.get('''  debug | {}'''.format(ensure_string(text)))

    @classmethod
    def get_test(cls, text):
        return cls.get('''   test | {}'''.format(ensure_string(text)))

    @classmethod
    def result(cls, text):
        if cls.ENABLE is True:
            sys.stdout.write(text+'\n')

    @classmethod
    def error(cls, text):
        if cls.ENABLE is True:
            sys.stderr.write(text+'\n')

    @classmethod
    def trace(cls, *args):
        cls.trace_result(*args)

    @classmethod
    def trace_result(cls, *args):
        if cls.ENABLE is True and cls.RESULT_ENABLE is True:
            text = ''.join(ensure_string(i) for i in args)
            log = cls.get_result(text)
            sys.stdout.write(
                log+'\n'
            )
            if _bridge.BRG_FNC_LOG_GUI_TRACE_ENABLE is True:
                _bridge.BRG_FNC_LOG_GUI_TRACE_RESULT(log)
            return log

    @classmethod
    def trace_warning(cls, *args):
        if cls.ENABLE is True and cls.WARNING_ENABLE is True:
            text = ''.join(ensure_string(i) for i in args)
            log = cls.get_warning(text)
            sys.stdout.write(
                log+'\n'
            )
            if _bridge.BRG_FNC_LOG_GUI_TRACE_ENABLE is True:
                _bridge.BRG_FNC_LOG_GUI_TRACE_WARNING(log)
            return log

    @classmethod
    def trace_error(cls, *args):
        if cls.ENABLE is True and cls.ERROR_ENABLE is True:
            text = ''.join(ensure_string(i) for i in args)
            log = cls.get_error(text)
            sys.stderr.write(
                log+'\n'
            )
            if _bridge.BRG_FNC_LOG_GUI_TRACE_ENABLE is True:
                _bridge.BRG_FNC_LOG_GUI_TRACE_ERROR(log)
            return log

    @classmethod
    def get_method_result(cls, name, *args):
        name = ensure_string(name)
        text = ''.join(ensure_string(i) for i in args)
        return cls.get_result(
            '<{}> {}'.format(name, text)
        )

    @classmethod
    def get_method_warning(cls, name, *args):
        name = ensure_string(name)
        text = ''.join(ensure_string(i) for i in args)
        return cls.get_warning(
            '<{}> {}'.format(name, text)
        )

    @classmethod
    def get_method_error(cls, name, *args):
        """
        :param name: str/unicode
        :param args: str/unicode, ...
        :return:
        """
        return cls.get_error(
            '<{}> {}'.format(ensure_string(name), ''.join(ensure_string(i) for i in args))
        )

    @classmethod
    def trace_method_result(cls, name, *args):
        """
        :param name: str/unicode
        :param args: str/unicode, ...
        :return:
        """
        return cls.trace_result(
            '<{}> {}'.format(ensure_string(name), ''.join(ensure_string(i) for i in args))
        )

    @classmethod
    def trace_method_warning(cls, name, *args):
        return cls.trace_warning(
            '<{}> {}'.format(ensure_string(name), ''.join(ensure_string(i) for i in args))
        )

    @classmethod
    def trace_method_error(cls, name, *args):
        return cls.trace_error(
            '<{}> {}'.format(ensure_string(name), ''.join(ensure_string(i) for i in args))
        )

    @classmethod
    def debug(cls, text):
        if cls.DEBUG is True:
            sys.stdout.write(
                cls.get_debug(text+'\n')
            )
            return text

    @classmethod
    def debug_method(cls, name, *args):
        if cls.DEBUG is True:
            return cls.debug(
                '<{}> {}'.format(ensure_string(name), ''.join(ensure_string(i) for i in args))
            )

    @classmethod
    def test_start(cls, text):
        if cls.TEST is True:
            cls.TIMESTAMP_CACHE[text] = time.time()
            #
            sys.stdout.write(
                cls.get_test(text+' is start'+'\n')
            )
            return text

    @classmethod
    def test_end(cls, text):
        if cls.TEST is True:
            time_pre = cls.TIMESTAMP_CACHE.get(text)
            if time_pre:
                t = time.time()
                sys.stdout.write(
                    cls.get_test(text+' is end '+'cost: {}s\n'.format(t-time_pre))
                )
            else:
                sys.stdout.write(
                    cls.get_test(text+' is end'+'\n')
                )
            return text

    @classmethod
    def filter_process_start(cls, text):
        """
        print(Log.filter_process_start(
            '2023-09-13 15:25:20         | <test> process is started, total is 20'
        ))
        """
        p = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\|\s<(.*)> process is started, total is (\d+)'
        m = re.search(p, text)
        if m:
            _time = m.group(1)
            _keyword = m.group(2)
            _count = int(m.group(3))
            return _time, _keyword, _count

    @classmethod
    def filter_progress(cls, text):
        """
        print(Log.filter_progress(
            '2023-09-13 15:50:27         | <test> ■□□□□□□□□□□□□□□□□□□□   10%, cost time 00:00:00.5006'
        ))
        """
        p = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\|\s<(.*)>.*\s(\d+)\%, cost time (\d+)'
        m = re.search(p, text)
        if m:
            _time = m.group(1)
            _keyword = m.group(2)
            _percent = m.group(3)
            return _time, _keyword, float(_percent)/100.0

    @classmethod
    def filter_result(cls, text):
        """
        print(Log.filter_result(
            '2023-09-13 15:25:20         | process is started, total is 20'
        ))
        """
        p = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\|\s(.*)'
        m = re.search(p, text)
        if m:
            _time = m.group(1)
            _content = m.group(2)
            return _time, _content


class LogContext(object):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __init__(self, module, result=None):
        self._module = module
        self._result = result or ''

    def __enter__(self):
        Log.trace_method_result(
            self._module, self._result+' is started'
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Log.trace_method_result(
            self._module, self._result+' is completed'
        )


class LogProcessContext(object):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @classmethod
    def create_as_bar(cls, *args, **kwargs):
        kwargs['use_as_progress_bar'] = True
        return cls.create(*args, **kwargs)

    def __init__(self, maximum, label=None, use_as_progress_bar=False):
        self.__maximum = maximum
        self.__value = 0
        if label is None:
            label = 'process'

        self.__label = label
        self.__use_as_bar = use_as_progress_bar

        self._start_timestamp = LogBase.generate_timestamp()
        self._pre_timestamp = LogBase.generate_timestamp()

        self._p = 0

        Log.trace_method_result(
            self.__label,
            'process is started, total is {}'.format(self.__maximum)
        )
        if _bridge.BRG_FNC_LOG_GUI_PROCESS_ENABLE is True:
            if isinstance(_bridge.BRG_FNC_LOG_GUI_PROCESS_CREATE, (types.FunctionType, types.MethodType)):
                self.__gui_ps = _bridge.BRG_FNC_LOG_GUI_PROCESS_CREATE(maximum, label=label)
            else:
                raise RuntimeError()
        else:
            self.__gui_ps = []

    def do_update(self, *args, **kwargs):
        self.__update_trace(*args, **kwargs)
        self.__update_gui(*args, **kwargs)

    # noinspection PyUnusedLocal
    def __update_trace(self, *args, **kwargs):
        self.__value += 1
        percent = float(self.__value)/float(self.__maximum)
        # trace when value is integer
        p = '%3d'%(int(percent*100))
        if self._p == p:
            return

        cur_timestamp = LogBase.generate_timestamp()
        cost_timestamp = cur_timestamp-self._pre_timestamp
        self._pre_timestamp = cur_timestamp
        if self.__use_as_bar is True:
            Log.trace_method_result(
                '{}'.format(self.__label),
                '{} {}%, cost time {}'.format(
                    self.__get_progress_bar_string(percent),
                    p,
                    LogBase.second_to_time_prettify(cost_timestamp),

                )
            )
        else:
            Log.trace_method_result(
                '{}'.format(self.__label),
                '{}%, cost time {}'.format(
                    p,
                    LogBase.second_to_time_prettify(cost_timestamp),
                )
            )

    def __update_gui(self, *args, **kwargs):
        if self.__gui_ps:
            for i_p in self.__gui_ps:
                i_p.do_update(*args, **kwargs)

    @classmethod
    def __get_progress_bar_string(cls, percent):
        c = 20
        p = int(percent*c)
        p = max(p, 1)
        return '{}{}'.format(
            p*'■', (c-p)*'□'
        )

    def set_stop(self):
        self.__stop_trace()
        self.__stop_gui()

    def __stop_trace(self):
        self.__value = 0
        self.__maximum = 0
        #
        cost_timestamp = LogBase.generate_timestamp()-self._start_timestamp
        Log.trace_method_result(
            self.__label,
            'process is completed, cost time {}'.format(
                LogBase.second_to_time_prettify(cost_timestamp),
            )
        )

    def __stop_gui(self):
        if self.__gui_ps:
            for p in self.__gui_ps:
                p.set_stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_stop()


class LogDebug:
    @staticmethod
    def _trace():
        text = Debug.get_error_stack()
        if text:
            sys.stderr.write(text+'\n')

    @staticmethod
    def _gui_trace():
        if _bridge.BRG_FNC_LOG_GUI_EXCEPTION_ENABLE is True:
            if isinstance(_bridge.BRG_FNC_LOG_GUI_EXCEPTION_TRACE, (types.FunctionType, types.MethodType)):
                _bridge.BRG_FNC_LOG_GUI_EXCEPTION_TRACE()
                return True
        return False

    @classmethod
    def trace(cls):
        if cls._gui_trace() is False:
            # trace when gui is disabled
            cls._trace()

    @staticmethod
    def run(fnc):
        def fnc_(*args, **kwargs):
            # noinspection PyBroadException
            try:
                _fnc = fnc(*args, **kwargs)
                return _fnc
            except Exception:
                import lxbasic.core as bsc_core
                LogDebug.trace()
                raise
        return fnc_


if __name__ == '__main__':
    print(LogBase.get_user_debug_directory('qt'))
