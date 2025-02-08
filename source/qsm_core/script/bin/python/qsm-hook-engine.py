# coding:utf-8
from __future__ import print_function

import sys

import os

import getopt

LOG_KEY = 'qsm-hook-engine'


def main(argv):
    try:
        sys.stdout.write('execute qsm-hook-engine from: "{}"\n'.format(__file__))
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
        '***** qsm-hook-engine *****\n'
        '\n'
        'run command(s) by rez-env and application program\n'
        '\n'
        '-h or --help: show help\n'
        '-o or --option: set run with option\n'
        '\n'
        'engines:\n'
        '    python,'
        '    maya, maya-python,\n'
        '    houdini, houdini-python,\n'
        '    katana, katana-python...\n'
        '\n'
        '***** qsm-hook-engine *****\n'
    )


def __execute_with_option(option):
    import lxbasic.core as bsc_core
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    #
    option_hook_key = option_opt.get('option_hook_key')
    if option_hook_key:
        __execute_option_hook_new(hook_option=option)


def __execute_option_hook(hook_option):
    """
    :param hook_option:
    :return:
    """
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.session as bsc_session

    import lxbasic.extra.methods as bsc_etr_methods

    import lxresolver.core as rsv_core

    resolver = rsv_core.RsvBase.generate_root()

    all_hook_engines = bsc_session.SsnHookEngine.get_all()
    option_opt = bsc_core.ArgDictStringOpt(hook_option)

    project = option_opt.get('project')
    rsv_project = resolver.get_rsv_project(project=project)
    if rsv_project is None:
        raise RuntimeError()

    hook_engine = option_opt.get('hook_engine')
    # check engine is in configure
    if hook_engine not in all_hook_engines:
        raise RuntimeError(
            bsc_log.Log.trace_method_error(
                LOG_KEY,
                'engine="{}" is not available'.format(hook_engine)
            )
        )

    test_flag = option_opt.get('test_flag') or False
    if test_flag is True:
        bsc_core.BscEnviron.set(
            'QSM_TEST', '1'
        )

    kwargs = option_opt.value
    kwargs.update(
        dict(
            lxdcc_root=os.environ.get('QSM_CORE_BASE'),
            hook_option=hook_option,
        )
    )
    opt_args_execute = []
    opt_packages_extend = []
    # add extend packages
    hook_packages_extend = option_opt.get('rez_extend_packages', as_array=True)
    if hook_packages_extend:
        opt_packages_extend.extend(
            hook_packages_extend
        )

    opt_args_execute.append(
        bsc_session.SsnHookEngine.get_command(
            **kwargs
        )
    )

    application = hook_engine.split('-')[0]
    if application == 'katana':
        # todo: use configure
        katana_version = option_opt.get('katana_version')
        if katana_version:
            if katana_version >= '4.5':
                application = 'katana4.5'

    rsv_app = rsv_project.get_rsv_app(
        application=application
    )
    if rsv_app is None:
        raise RuntimeError()

    use_thread = option_opt.get('use_thread') or False
    # add extend environs
    environs_extend = {}

    _ = bsc_core.BscEnviron.get('QSM_EXTEND_RESOURCES')
    if _:
        environs_extend['QSM_EXTEND_RESOURCES'] = _

    framework_scheme = rsv_project.get_framework_scheme()
    m = bsc_etr_methods.get_module(framework_scheme)
    framework_packages_extend = m.EtrBase.get_base_packages_extend()
    if framework_packages_extend:
        opt_packages_extend.extend(framework_packages_extend)

    command = rsv_app.get_command(
        args_execute=opt_args_execute,
        packages_extend=opt_packages_extend
    )

    if use_thread is True:
        rsv_app.execute_with_result_use_thread(
            command, environs_extend=environs_extend
        )
    else:
        rsv_app.execute_with_result(
            command, environs_extend=environs_extend
        )


def __execute_option_hook_new(hook_option):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.session as bsc_session

    # fixme, option has ""
    if hook_option.startswith('"'):
        hook_option = eval(hook_option)

    option_opt = bsc_core.ArgDictStringOpt(hook_option)

    hook_engine = option_opt.get('hook_engine')
    if hook_engine is None:
        raise RuntimeError(
            bsc_log.Log.trace_method_error(
                LOG_KEY, 'hook engine is not valid or not definition'
            )
        )

    all_hook_engines = bsc_session.SsnHookEngine.get_all()
    if hook_engine not in all_hook_engines:
        raise RuntimeError(
            bsc_log.Log.trace_method_error(
                LOG_KEY, 'hook engine is not in configure'
            )
        )

    application = hook_engine.split('-')[0]

    test_flag = option_opt.get('test_flag') or False
    if test_flag is True:
        bsc_core.BscEnviron.set(
            'QSM_TEST', '1'
        )

    kwargs = option_opt.value
    kwargs.update(
        dict(
            lxdcc_root=os.environ.get('QSM_CORE_BASE'),
            hook_option=hook_option,
        )
    )
    opt_args_execute = []
    opt_packages_extend = []
    # add extend packages
    hook_packages_extend = option_opt.get('rez_extend_packages', as_array=True)
    if hook_packages_extend:
        opt_packages_extend.extend(
            hook_packages_extend
        )

    opt_args_execute.append(
        bsc_session.SsnHookEngine.get_command(
            **kwargs
        )
    )

    cmd_args = [
        r'rez-env',
        r' '.join(hook_packages_extend),
        r' '.join(opt_args_execute)
    ]
    cmd_script = r' '.join(cmd_args)

    bsc_core.BscProcess.execute_as_trace(
        cmd_script
    )


if __name__ == '__main__':
    main(sys.argv)
