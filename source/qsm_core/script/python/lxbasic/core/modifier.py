# coding:utf-8
import types

import time

import lxbasic.log as bsc_log

from . import base as bsc_cor_base


class MdfBaseMtd(object):
    @staticmethod
    def run_as_ignore(fnc):
        def fnc_(*args, **kw):
            # noinspection PyBroadException
            try:
                return fnc(*args, **kw)
            except Exception:
                bsc_cor_base.ExceptionMtd.set_print()

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
                    bsc_cor_base.SysBaseMtd.TIME_FORMAT,
                    time.localtime(start_timestamp)
                )
            )
            bsc_cor_base.SysBaseMtd.trace(message)

            _fnc = fnc(*args, **kwargs)

            end_timestamp = time.time()
            message = 'complete function: "{}.{}" at {} use {}s'.format(
                fnc.__module__,
                fnc.__name__,
                time.strftime(
                    bsc_cor_base.SysBaseMtd.TIME_FORMAT,
                    time.localtime(end_timestamp)
                ),
                (end_timestamp-start_timestamp)
            )
            bsc_cor_base.SysBaseMtd.trace(message)
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
                bsc_log.Log.trace_method_result(
                    'fnc run',
                    'fnc="{}" is started'.format(
                        fnc_path
                    ),
                )
                #
                _result = fnc(*args, **kwargs)
                #
                bsc_log.Log.trace_method_result(
                    'fnc run',
                    'fnc="{}" is completed'.format(
                        fnc_path
                    )
                )
            except Exception:
                bsc_log.Log.trace_method_error(
                    'fnc run',
                    'fnc="{}" is error'.format(
                        fnc_path
                    )
                )
                bsc_cor_base.ExceptionMtd.set_print()

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
                bsc_log.Log.trace_method_result(
                    'fnc run',
                    'fnc="{}" is started'.format(
                        fnc_path
                    ),
                )
                #
                _result = fnc(*args, **kwargs)
                #
                if _result is True:
                    bsc_log.Log.trace_method_result(
                        'fnc run',
                        'fnc="{}" is completed'.format(
                            fnc_path
                        )
                    )
                else:
                    bsc_log.Log.trace_method_warning(
                        'fnc run',
                        'fnc="{}" is failed'.format(
                            fnc_path
                        )
                    )
            except Exception:
                bsc_log.Log.trace_method_error(
                    'fnc run',
                    'fnc="{}" is error'.format(
                        fnc_path
                    )
                )
                bsc_cor_base.ExceptionMtd.set_print()

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
                bsc_log.LogException.trace()
                raise

        return fnc_
