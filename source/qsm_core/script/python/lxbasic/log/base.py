# coding:utf-8
import os

import six

import re

import sys

import time

import types

import platform

import getpass

from . import bridge as _bridge


class LogBase(object):
    LOG_ROOT_KEY = 'QSM_LOG_ROOT'
    DATA_TAG_FORMAT = '%Y_%m%d'

    @staticmethod
    def auto_string(text):
        if isinstance(text, six.text_type):
            return text.encode('utf-8')
        return text

    @staticmethod
    def get_timestamp():
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
            cls.DATA_TAG_FORMAT,
            time.localtime(timestamp)
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


class Log(object):
    DEFAULT_CODING = sys.getdefaultencoding()

    FILE_SYSTEM_CODING = sys.getfilesystemencoding()

    sys.stdout.write(
        'logger is initialization, default coding is "{}"'.format(DEFAULT_CODING)+'\n'
    )

    ENABLE = True

    RESULT_ENABLE = True
    WARNING_ENABLE = True
    ERROR_ENABLE = True

    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    DATA_TAG_FORMAT = '%Y_%m%d'

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
        text = LogBase.auto_string(text)
        return '{} {}'.format(cls.get_time(), text)

    @classmethod
    def get_result(cls, text):
        text = LogBase.auto_string(text)
        return cls.get('''        | {}'''.format(text))

    @classmethod
    def get_warning(cls, text):
        text = LogBase.auto_string(text)
        return cls.get('''warning | {}'''.format(text))

    @classmethod
    def get_error(cls, text):
        text = LogBase.auto_string(text)
        return cls.get('''  error | {}'''.format(text))

    @classmethod
    def get_debug(cls, text):
        text = LogBase.auto_string(text)
        return cls.get('''  debug | {}'''.format(text))

    @classmethod
    def get_test(cls, text):
        text = LogBase.auto_string(text)
        return cls.get('''   test | {}'''.format(text))

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
            text = ''.join(LogBase.auto_string(i) for i in args)
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
            text = ''.join(LogBase.auto_string(i) for i in args)
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
            text = ''.join(LogBase.auto_string(i) for i in args)
            log = cls.get_error(text)
            sys.stderr.write(
                log+'\n'
            )
            if _bridge.BRG_FNC_LOG_GUI_TRACE_ENABLE is True:
                _bridge.BRG_FNC_LOG_GUI_TRACE_ERROR(log)
            return log

    @classmethod
    def get_method_result(cls, name, *args):
        name = LogBase.auto_string(name)
        text = ''.join(LogBase.auto_string(i) for i in args)
        return cls.get_result(
            '<{}> {}'.format(name, text)
        )

    @classmethod
    def get_method_warning(cls, name, *args):
        name = LogBase.auto_string(name)
        text = ''.join(LogBase.auto_string(i) for i in args)
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
        name = LogBase.auto_string(name)
        text = ''.join(LogBase.auto_string(i) for i in args)
        return cls.get_error(
            '<{}> {}'.format(name, text)
        )

    @classmethod
    def trace_method_result(cls, name, *args):
        """
        :param name: str/unicode
        :param args: str/unicode, ...
        :return:
        """
        name = LogBase.auto_string(name)
        text = ''.join(LogBase.auto_string(i) for i in args)
        return cls.trace_result(
            '<{}> {}'.format(name, text)
        )

    @classmethod
    def trace_method_warning(cls, name, *args):
        name = LogBase.auto_string(name)
        text = ''.join(LogBase.auto_string(i) for i in args)
        return cls.trace_warning(
            '<{}> {}'.format(name, text)
        )

    @classmethod
    def trace_method_error(cls, name, *args):
        name = LogBase.auto_string(name)
        text = ''.join(LogBase.auto_string(i) for i in args)
        return cls.trace_error(
            '<{}> {}'.format(name, text)
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
            name = LogBase.auto_string(name)
            text = ''.join(LogBase.auto_string(i) for i in args)
            return cls.debug(
                '<{}> {}'.format(name, text)
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
        print Log.filter_process_start(
            '2023-09-13 15:25:20         | <test> process is started, total is 20'
        )
        """
        p = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\|\s<(.*)> process is started, total is (\d+)'
        m = re.search(p, text)
        if m:
            _time = m.group(1)
            _keyword = m.group(2)
            _count = int(m.group(3))
            return _time, _keyword, _count

    @classmethod
    def filter_process(cls, text):
        """
        print Log.filter_process(
            '2023-09-13 15:50:27         | <test> ■□□□□□□□□□□□□□□□□□□□   10%, cost time 00:00:00.5006'
        )
        """
        p = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\|\s<(.*)>.*\s(\d+)\%, cost time (\d+)'
        m = re.search(p, text)
        if m:
            _time = m.group(1)
            _keyword = m.group(2)
            _percent = m.group(3)
            return _time, _keyword, _percent

    @classmethod
    def filter_result(cls, text):
        """
        print Log.filter_result(
            '2023-09-13 15:25:20         | process is started, total is 20'
        )
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
            label = 'unknown'

        self.__label = label
        self.__use_as_bar = use_as_progress_bar
        #
        self._start_timestamp = LogBase.get_timestamp()
        self._pre_timestamp = LogBase.get_timestamp()
        #
        self._p = 0
        #
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
        cur_timestamp = LogBase.get_timestamp()
        cost_timestamp = cur_timestamp-self._pre_timestamp
        self._pre_timestamp = cur_timestamp
        #
        percent = float(self.__value)/float(self.__maximum)
        # trace when value is integer
        p = '%3d'%(int(percent*100))
        # if self._p != p:
        #     self._p = p
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
        cost_timestamp = LogBase.get_timestamp()-self._start_timestamp
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


class LogException(object):
    @staticmethod
    def __trace():
        import sys

        import traceback

        exc_texts = []
        exc_type, exc_value, exc_stack = sys.exc_info()
        if exc_type:
            value = repr(exc_value)
            sys.stderr.write('*'*80+'\n')
            for i_stk in traceback.extract_tb(exc_stack):
                i_file_path, i_line, i_fnc, i_fnc_line = i_stk
                exc_texts.append(
                    '    file "{}" line {} in {}\n        {}'.format(i_file_path, i_line, i_fnc, i_fnc_line)
                )

            sys.stderr.write('traceback:\n')
            sys.stderr.write('\n'.join(exc_texts)+'\n')
            sys.stderr.write(value+'\n')
            sys.stderr.write('*'*80+'\n')

    @staticmethod
    def __gui_trace():
        if _bridge.BRG_FNC_LOG_GUI_EXCEPTION_ENABLE is True:
            if isinstance(_bridge.BRG_FNC_LOG_GUI_EXCEPTION_TRACE, (types.FunctionType, types.MethodType)):
                _bridge.BRG_FNC_LOG_GUI_EXCEPTION_TRACE()

    @classmethod
    def trace(cls):
        cls.__trace()
        cls.__gui_trace()


if __name__ == '__main__':
    print LogBase.get_user_debug_directory('qt')
