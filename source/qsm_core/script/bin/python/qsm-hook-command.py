# coding:utf-8
from __future__ import print_function

import sys

import getopt

argv = sys.argv

LOG_KEY = 'qsm-hook-command'


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'ho:',
            ['help', 'option=']
        )
        option = None
        for key, value in opts:
            if key in ('-h', '--help'):
                __print_help()
                #
                sys.exit()
            elif key in ('-o', '--option'):
                option = value
        #
        if option is not None:
            __execute_with_option(option)
    #
    except getopt.GetoptError:
        sys.stdout.write('argv error\n')


def __print_help():
    sys.stdout.write(
        '***** qsm-hook-command *****\n'
        '\n'
        #
        '-h or --help: show help\n'
    )


def __execute_with_option(option):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    bsc_log.Log.trace_method_result(
        LOG_KEY,
        'execute from: {}'.format(__file__)
    )

    option_opt = bsc_core.ArgDictStringOpt(option)
    option_hook_key = option_opt.get('option_hook_key')
    if option_hook_key:
        __execute_option_hook(option)
    else:
        hook_key = option_opt.get('hook_key')
        if hook_key:
            __execute_hook(option)


# hook
def __execute_hook(option):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.extra.methods as bsc_etr_methods

    import lxsession.commands as ssn_commands

    option_opt = bsc_core.ArgDictStringOpt(option)

    hook_key = option_opt.get('hook_key')
    hook_args = ssn_commands.get_hook_args(hook_key)
    if hook_args:
        session, fnc = hook_args
        #
        opt_packages_extend = []
        # extend package from base
        framework_packages_extend = bsc_etr_methods.EtrBase.get_base_packages_extend()
        if framework_packages_extend:
            bsc_log.Log.trace_method_result(
                LOG_KEY,
                'extend packages from framework: {}'.format(', '.join(framework_packages_extend))
            )
            opt_packages_extend.extend(
                bsc_etr_methods.EtrBase.packages_completed_to(framework_packages_extend)
            )
        # extend package from builtin
        builtin_package_extend = bsc_etr_methods.EtrBase.get_builtin_packages_extend()
        if builtin_package_extend:
            bsc_log.Log.trace_method_result(
                LOG_KEY,
                'extend packages from builtin: {}'.format(', '.join(builtin_package_extend))
            )
            opt_packages_extend.extend(
                bsc_etr_methods.EtrBase.packages_completed_to(builtin_package_extend)
            )
        # extend packages from session
        hook_packages_extend = session.get_packages_extend()
        if hook_packages_extend:
            bsc_log.Log.trace_method_result(
                LOG_KEY,
                'extend packages from session: {}'.format(', '.join(hook_packages_extend))
            )
            opt_packages_extend.extend(
                bsc_etr_methods.EtrBase.packages_completed_to(hook_packages_extend)
            )
        #
        opt_cmd = bsc_etr_methods.EtrBase.get_base_command(
            args_execute=['-- qsm-hook-python -o "{}"'.format(option)],
            packages_extend=opt_packages_extend
        )
        # extend resource paths
        environs_extend = {}
        _ = bsc_core.BscEnviron.get('QSM_EXTEND_RESOURCES')
        if _:
            environs_extend['QSM_EXTEND_RESOURCES'] = (_, 'prepend')
        #
        hook_environs_extend = session.get_environs_extend()
        if hook_environs_extend:
            for k, v in hook_environs_extend:
                environs_extend[k] = v
        # run command by subprocess
        bsc_core.BscProcess.execute_with_result_use_thread(
            opt_cmd, environs_extend=environs_extend
        )


# option hook
def __execute_option_hook(option):
    import lxbasic.core as bsc_core

    import lxsession.commands as ssn_commands

    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    hook_args = ssn_commands.get_option_hook_args(option)
    if hook_args:
        session, fnc = hook_args

        deadline_enable = option_opt.get_as_boolean('deadline_enable')
        if deadline_enable is True:
            session.execute_hook_with_deadline()
        else:
            session.execute_hook_with_shell()


if __name__ == '__main__':
    main()
