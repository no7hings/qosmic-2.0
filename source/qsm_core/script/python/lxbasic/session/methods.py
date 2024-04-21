# coding:utf-8
import functools

import lxbasic.resource as bsc_resource

from . import base as bsc_ssn_base


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
                session = bsc_ssn_base.CommandSession(
                    type=hook_type,
                    hook=hook_key,
                    configure=hook_configure
                )
            else:
                session = bsc_ssn_base.GenerSession(
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
