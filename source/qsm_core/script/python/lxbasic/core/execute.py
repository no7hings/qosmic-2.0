# coding:utf-8
# resource
from .. import resource as _bsc_resource
# log
from .. import log as _bsc_log
# process
from . import base as _base

from . import environ as _environ

from . import process as _process


class BscBinExecute(object):
    @classmethod
    def oiiotool(cls):
        if _base.BscSystem.get_is_windows():
            name = 'oiiotool.exe'
            _ = _environ.BscEnviron.find_execute(name)
            if _:
                return name
            return _bsc_resource.BscExe.get(name)
        elif _base.BscSystem.get_is_linux():
            name = 'oiiotool'
            _ = _environ.BscEnviron.find_execute(name)
            if _:
                return name
            return _bsc_resource.BscExe.get(name)

    @classmethod
    def oslc(cls):
        if _base.BscSystem.get_is_windows():
            name = 'oslc.exe'
            _ = _environ.BscEnviron.find_execute(name)
            if _:
                return name
            return _bsc_resource.BscExe.get(name)
        elif _base.BscSystem.get_is_linux():
            name = 'oslc'
            _ = _environ.BscEnviron.find_execute(name)
            if _:
                return name
            return _bsc_resource.BscExe.get(name)

    @classmethod
    def oslinfo(cls):
        if _base.BscSystem.get_is_windows():
            name = 'oslinfo.exe'
            _ = _environ.BscEnviron.find_execute(name)
            if _:
                return name
            return _bsc_resource.BscExe.get(name)
        elif _base.BscSystem.get_is_linux():
            name = 'oslinfo'
            _ = _environ.BscEnviron.find_execute(name)
            if _:
                return name
            return _bsc_resource.BscExe.get(name)

    @classmethod
    def ffmpeg(cls):
        if _base.BscSystem.get_is_windows():
            name = 'ffmpeg.exe'
            _ = _environ.BscEnviron.find_execute(name)
            if _:
                return name
            return _bsc_resource.BscExe.get(name)
        elif _base.BscSystem.get_is_linux():
            name = 'ffmpeg'
            _ = _environ.BscEnviron.find_execute(name)
            if _:
                return name
            return _bsc_resource.BscExe.get(name)


class BscScriptExecute(object):
    LOG_KEY = 'script execute'

    @classmethod
    def execute_python_file(cls, file_path, **kwargs):
        _bsc_log.Log.trace_method_result(
            cls.LOG_KEY, 'start for : "{}"'.format(
                file_path
            )
        )
        kwargs['__name__'] = '__main__'
        _base.BscSystem.execfile(file_path, kwargs)
        _bsc_log.Log.trace_method_result(
            cls.LOG_KEY, 'complete for: "{}"'.format(
                file_path
            )
        )

    @staticmethod
    def execute_shell_file_use_terminal(file_path, **kwargs):
        _bsc_log.Log.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        if _base.BscPlatform.get_is_linux():
            cmd_args = [
                'gnome-terminal', '-t', kwargs.get('title') or 'untitled',
                '-e "bash -l {}"'.format(file_path)
            ]
            _process.BscProcess.execute_as_trace(
                ' '.join(cmd_args)
            )
        elif _base.BscPlatform.get_is_windows():
            cmd_args = ['start', 'cmd', '/k', file_path]
            _process.BscProcess.execute_as_trace(
                ' '.join(cmd_args)
            )
        _bsc_log.Log.trace_method_result(
            'option-hook', 'complete for: "{}"'.format(
                file_path
            )
        )

    @staticmethod
    def execute_shell_script_use_terminal(cmd, **kwargs):
        if _base.BscPlatform.get_is_linux():
            cmd_args = [
                'gnome-terminal',
                '-t', kwargs.get('title') or 'untitled',
                '--', 'bash', '-l', '-c', cmd
            ]
            _process.BscProcess.execute_as_trace(
                ' '.join(cmd_args)
            )
        elif _base.BscPlatform.get_is_windows():
            cmd_args = ['start', 'cmd', '/k', cmd]
            _process.BscProcess.execute_as_trace(
                ' '.join(cmd_args)
            )

    @staticmethod
    def execute_shell_script(cmd, use_thread=True):
        if use_thread is True:
            _process.BscProcess.execute_use_thread(cmd)
        else:
            _process.BscProcess.execute(cmd)
