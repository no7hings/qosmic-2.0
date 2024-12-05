# coding:utf-8
from __future__ import print_function

import sys

import os

import json

import getopt

argv = sys.argv

LOG_KEY = 'qsm-hook-json'


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'hj:',
            ['help', 'json=']
        )
        json_path = None
        for key, value in opts:
            if key in ('-h', '--help'):
                __print_help()
                #
                sys.exit()
            elif key in ('-j', '--json'):
                json_path = value
        #
        if json_path is not None:
            __execute_with_option(json_path)
    #
    except getopt.GetoptError:
        sys.stdout.write('argv error\n')


def __read_json(json_path):
    with open(json_path) as j:
        # noinspection PyTypeChecker
        raw = json.load(j)
        j.close()
        return raw


def __print_help():
    sys.stdout.write(
        '***** qsm-hook-json *****\n'
        '\n'
        '-h or --help: show help\n'
        '\n'
        'etc.\n'
        '-j "test.json"\n'
    )


def __execute_with_option(json_path):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    bsc_log.Log.trace_method_result(
        LOG_KEY,
        'execute from: {}'.format(__file__)
    )

    data = __read_json(json_path)

    bsc_core.BscEnviron.set(
        'hook_start_m', str(bsc_core.BscSystem.get_minute())
    )
    bsc_core.BscEnviron.set(
        'hook_start_s', str(bsc_core.BscSystem.get_second())
    )
    # do not use thread, there will be run with subprocess, run with thread use "qsm-hook-command"
    option_hook_key = data.get('option_hook_key')
    if option_hook_key:
        __execute_option_hook(
            bsc_core.ArgDictStringOpt(option=dict(option_hook_key=option_hook_key, json=json_path)).to_string()
        )
    else:
        hook_key = data.get('hook_key')
        if hook_key:
            __execute_hook(hook_key)


def __execute_hook(hook_key):
    import lxsession.commands as ssn_commands; ssn_commands.execute_hook(hook_key)


def __execute_option_hook(option):
    import lxsession.commands as ssn_commands; ssn_commands.execute_option_hook(option)


if __name__ == '__main__':
    main()
