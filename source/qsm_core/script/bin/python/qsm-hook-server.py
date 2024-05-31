# coding:utf-8
from __future__ import print_function

import sys

import getopt

argv = sys.argv

IS_STARTED = False


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'ho:',
            ['help', 'option=']
        )
        option = [None] * 1
        for key, value in opts:
            if key in ('-h', '--help'):
                __print_help()
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
        '***** qsm-hook-server *****\n'
        '\n'
        '-h or --help: show help\n'
        '-o or --option: set run with option\n'
        'start sever: -o start=true\n'
    )


def __execute_with_option(option):
    import lxbasic.core as bsc_core

    option_opt = bsc_core.ArgDictStringOpt(option)
    # start server
    if option_opt.get_as_boolean('start') or False is True:
        if IS_STARTED is False:
            __start_server()


def __start_server():
    import lxsession.commands as ssn_commands
    ssn_commands.execute_hook('desktop-tools/qsm-prc-task-manager')


if __name__ == '__main__':
    main()
