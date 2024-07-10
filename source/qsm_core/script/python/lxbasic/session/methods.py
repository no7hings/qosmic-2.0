# coding:utf-8
import functools

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

from . import base as _base


class Hook(object):
    @classmethod
    def get_args(cls, key):
        _ = bsc_resource.RscHook.get_args(
                key
            )
        if _:
            hook_type, hook_key, hook_configure, yaml_file_path, python_file_path, shell_file_path = _
            if hook_type in {
                'python-script', 'shell-script'
            }:
                session = _base.ScriptSession(
                    type=hook_type,
                    hook=hook_key,
                    configure=hook_configure
                )
            else:
                session = _base.GenerSession(
                    type=hook_type,
                    hook=hook_key,
                    configure=hook_configure
                )

            session.set_configure_yaml_file(yaml_file_path)
            if python_file_path is not None:
                session.set_python_script_file(python_file_path)
            if shell_file_path:
                session.set_shell_script_file(shell_file_path)

            return session, functools.partial(session.execute)

    @classmethod
    def execute(cls, key):
        hook_args = cls.get_args(key)
        if hook_args is not None:
            session, execute_fnc = hook_args
            execute_fnc()
            return session
        else:
            bsc_log.Log.trace_method_warning(
                'hook execute',
                'hook_key="{}" is not found'.format(key)
            )


class OptionHook(object):
    @classmethod
    def get_args(cls, option, search_paths=None):
        option_opt = bsc_core.ArgDictStringOpt(option)
        option_hook_key = option_opt.get('option_hook_key')

        _ = bsc_resource.RscOptionHook.get_args(
            option_hook_key, search_paths
        )
        if _:
            hook_type, hook_key, hook_configure, yaml_file_path, python_file_path, shell_file_path = _
            # print hook_type, hook_key, hook_configure, yaml_file_path, python_file_path, shell_file_path

            session = _base.GenerOptionSession(
                type=hook_type,
                hook=option_hook_key,
                configure=hook_configure,
                option=option_opt.to_string()
            )
            session.set_configure_yaml_file(yaml_file_path)
            if python_file_path is not None:
                session.set_python_script_file(python_file_path)
            if shell_file_path:
                session.set_shell_script_file(shell_file_path)

            return session, functools.partial(session.execute)

    @classmethod
    def execute(cls, option, search_paths=None):
        hook_args = cls.get_args(option, search_paths)
        if hook_args is not None:
            session, execute_fnc = hook_args
            execute_fnc()
            return session
        else:
            bsc_log.Log.trace_method_warning(
                'option hook execute',
                'option="{}" is not valid'.format(option)
            )
