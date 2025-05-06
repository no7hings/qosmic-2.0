# coding:utf-8
from __future__ import print_function

import sys

import os

import getopt

argv = sys.argv

LOG_KEY = 'qsm-hook-python'


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
        '***** qsm-hook-python *****\n'
        '\n'
        '-h or --help: show help\n'
        '-o or --option: execute by option\n'
    )


def __execute_with_option(option):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core
    #
    bsc_log.Log.trace_method_result(
        LOG_KEY,
        'execute from: {}'.format(__file__)
    )
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    bsc_core.BscEnviron.set(
        'hook_start_m', str(bsc_core.BscSystem.get_minute())
    )
    bsc_core.BscEnviron.set(
        'hook_start_s', str(bsc_core.BscSystem.get_second())
    )
    # do not use thread, there will be run with subprocess, run with thread use "qsm-hook-command"
    option_hook_key = option_opt.get('option_hook_key')
    if option_hook_key:
        deadline_enable = option_opt.get_as_boolean('deadline_enable')
        if deadline_enable is True:
            __execute_option_hook_by_deadline(hook_option=option)
        else:
            __execute_option_hook(hook_option=option)
    else:
        hook_key = option_opt.get('hook_key')
        if hook_key:
            __execute_hook(hook_key)


def __execute_hook(hook_key):
    import lxsession.commands as ssn_commands; ssn_commands.execute_hook(hook_key)


def __execute_option_hook(hook_option):
    import lxsession.commands as ssn_commands; ssn_commands.execute_option_hook(hook_option)


def __execute_option_hook_by_deadline(hook_option):
    import lxsession.commands as ssn_commands; ssn_commands.execute_option_hook_by_deadline(hook_option)


if __name__ == '__main__':
    main()
