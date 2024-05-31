# coding:utf-8
import six

import lxbasic.web as bsc_web

import lxbasic.core as bsc_core


class MayaCacheProcess(object):
    @classmethod
    def generate_command(cls, option):
        if bsc_core.SysApplicationMtd.get_is_maya():
            maya_version = bsc_core.SysApplicationMtd.get_maya_version()
        else:
            maya_version = '2019'
        # do not use unicode
        # windows
        cmd_scripts = [
            'rez-env maya-{} qsm_dcc_main'.format(maya_version),
            (
                r'-- mayabatch -command '
                r'"python('
                r'\"import lxsession.commands as ssn_commands;'
                r'ssn_commands.execute_option_hook(option=\\\"{hook_option}\\\")\")"'
            ).format(
                hook_option='option_hook_key=dcc-process/maya-cache-process&' + option
            )
        ]
        return ' '.join(cmd_scripts)
