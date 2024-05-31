# coding:utf-8
# resource
from .. import resource as _bsc_resource
# log
from .. import log as _bsc_log
# process
from . import base as _base

from . import environ as _environ

from . import process as _process


class ExcBaseMtd(object):
    @classmethod
    def oiiotool(cls):
        if _base.SysBaseMtd.get_is_windows():
            name = 'oiiotool.exe'
            _ = _environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return _bsc_resource.RscExtendExe.get(name)
        elif _base.SysBaseMtd.get_is_linux():
            name = 'oiiotool'
            _ = _environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return _bsc_resource.RscExtendExe.get(name)

    @classmethod
    def oslc(cls):
        if _base.SysBaseMtd.get_is_windows():
            name = 'oslc.exe'
            _ = _environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return _bsc_resource.RscExtendExe.get(name)
        elif _base.SysBaseMtd.get_is_linux():
            name = 'oslc'
            _ = _environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return _bsc_resource.RscExtendExe.get(name)

    @classmethod
    def oslinfo(cls):
        if _base.SysBaseMtd.get_is_windows():
            name = 'oslinfo.exe'
            _ = _environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return _bsc_resource.RscExtendExe.get(name)
        elif _base.SysBaseMtd.get_is_linux():
            name = 'oslinfo'
            _ = _environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return _bsc_resource.RscExtendExe.get(name)

    @classmethod
    def ffmpeg(cls):
        if _base.SysBaseMtd.get_is_windows():
            name = 'ffmpeg.exe'
            _ = _environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return _bsc_resource.RscExtendExe.get(name)
        elif _base.SysBaseMtd.get_is_linux():
            name = 'ffmpeg'
            _ = _environ.EnvBaseMtd.find_execute(name)
            if _:
                return name
            return _bsc_resource.RscExtendExe.get(name)


class ExcExtraMtd(object):
    @staticmethod
    def execute_python_file(file_path, **kwargs):
        # use for python 3
        # with open(file_path, 'r') as f:
        #     exec (f.read())
        # use for python 2
        _bsc_log.Log.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        kwargs['__name__'] = '__main__'
        execfile(file_path, kwargs)
        _bsc_log.Log.trace_method_result(
            'option-hook', 'complete for: "{}"'.format(
                file_path
            )
        )

    @staticmethod
    def execute_python_script(cmd, **kwargs):
        # noinspection PyUnusedLocal
        session = kwargs['session']
        exec cmd

    @staticmethod
    def execute_shell_file_use_terminal(file_path, **kwargs):
        _bsc_log.Log.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        if _base.SysPlatformMtd.get_is_linux():
            cmds = [
                'gnome-terminal', '-t', kwargs.get('title') or 'untitled',
                '-e "bash -l {}"'.format(file_path)
            ]
            _process.PrcBaseMtd.execute_as_trace(
                ' '.join(cmds)
            )
        elif _base.SysPlatformMtd.get_is_windows():
            cmds = ['start', 'cmd', '/k', file_path]
            _process.PrcBaseMtd.execute_as_trace(
                ' '.join(cmds)
            )
        _bsc_log.Log.trace_method_result(
            'option-hook', 'complete for: "{}"'.format(
                file_path
            )
        )

    @staticmethod
    def execute_shell_script_use_terminal(cmd, **kwargs):
        if _base.SysPlatformMtd.get_is_linux():
            cmds = [
                'gnome-terminal',
                '-t', kwargs.get('title') or 'untitled',
                '--', 'bash', '-l', '-c', cmd
            ]
            _process.PrcBaseMtd.execute_as_trace(
                ' '.join(cmds)
            )
        elif _base.SysPlatformMtd.get_is_windows():
            cmds = ['start', 'cmd', '/k', cmd]
            _process.PrcBaseMtd.execute_as_trace(
                ' '.join(cmds)
            )

    @staticmethod
    def execute_shell_script(cmd, use_thread=True):
        if use_thread is True:
            _process.PrcBaseMtd.execute_use_thread(cmd)
        else:
            _process.PrcBaseMtd.execute(cmd)
