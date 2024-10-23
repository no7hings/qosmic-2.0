# coding:utf-8
import types

import time
# log
from .. import log as _bsc_log
# process
from . import base as _base


class BscModifier(object):
    @staticmethod
    def run_as_ignore(fnc):
        def fnc_(*args, **kw):
            # noinspection PyBroadException
            try:
                return fnc(*args, **kw)
            except Exception:
                _base.BscException.set_print()

        return fnc_

    @staticmethod
    def run_with_time_trace(fnc):
        def fnc_(*args, **kwargs):
            start_timestamp = time.time()
            #
            message = 'start function: "{}.{}" at {}'.format(
                fnc.__module__,
                fnc.__name__,
                time.strftime(
                    _base.BscSystem.TIME_FORMAT,
                    time.localtime(start_timestamp)
                )
            )
            _base.BscSystem.trace(message)

            _fnc = fnc(*args, **kwargs)

            end_timestamp = time.time()
            message = 'complete function: "{}.{}" at {} use {}s'.format(
                fnc.__module__,
                fnc.__name__,
                time.strftime(
                    _base.BscSystem.TIME_FORMAT,
                    time.localtime(end_timestamp)
                ),
                (end_timestamp-start_timestamp)
            )
            _base.BscSystem.trace(message)
            return _fnc

        return fnc_

    @staticmethod
    def run_with_result_trace(fnc):
        def fnc_(*args, **kwargs):
            if isinstance(fnc, types.FunctionType):
                fnc_path = '{}'.format(
                    fnc.__name__
                )
            elif isinstance(fnc, types.MethodType):
                fnc_path = '{}.{}'.format(
                    fnc.__class__.__name__, fnc.__name__
                )
            else:
                raise TypeError()
            # noinspection PyBroadException
            try:
                _bsc_log.Log.trace_method_result(
                    'fnc run',
                    'fnc="{}" is started'.format(
                        fnc_path
                    ),
                )
                #
                _result = fnc(*args, **kwargs)
                #
                _bsc_log.Log.trace_method_result(
                    'fnc run',
                    'fnc="{}" is completed'.format(
                        fnc_path
                    )
                )
            except Exception:
                _bsc_log.Log.trace_method_error(
                    'fnc run',
                    'fnc="{}" is error'.format(
                        fnc_path
                    )
                )
                _base.BscException.set_print()

        return fnc_

    @staticmethod
    def run_with_result_trace_extra(fnc):
        def fnc_(*args, **kwargs):
            if isinstance(fnc, types.FunctionType):
                fnc_path = '{}'.format(
                    fnc.__name__
                )
            elif isinstance(fnc, types.MethodType):
                fnc_path = '{}.{}'.format(
                    fnc.__class__.__name__, fnc.__name__
                )
            else:
                raise TypeError()
            # noinspection PyBroadException
            try:
                _bsc_log.Log.trace_method_result(
                    'fnc run',
                    'fnc="{}" is started'.format(
                        fnc_path
                    ),
                )
                #
                _result = fnc(*args, **kwargs)
                #
                if _result is True:
                    _bsc_log.Log.trace_method_result(
                        'fnc run',
                        'fnc="{}" is completed'.format(
                            fnc_path
                        )
                    )
                else:
                    _bsc_log.Log.trace_method_warning(
                        'fnc run',
                        'fnc="{}" is failed'.format(
                            fnc_path
                        )
                    )
            except Exception:
                _bsc_log.Log.trace_method_error(
                    'fnc run',
                    'fnc="{}" is error'.format(
                        fnc_path
                    )
                )
                _base.BscException.set_print()

        return fnc_

    @staticmethod
    def run_with_exception_catch(fnc):
        def fnc_(*args, **kwargs):
            # noinspection PyBroadException
            try:
                _fnc = fnc(*args, **kwargs)
                return _fnc
            except Exception:
                import lxbasic.core as bsc_core
                _bsc_log.LogException.trace()
                raise

        return fnc_
