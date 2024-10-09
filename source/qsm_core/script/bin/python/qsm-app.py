# coding:utf-8
from __future__ import print_function

import sys

import os

import getopt

LOG_KEY = 'qsm-app'


def main(argv):
    try:
        opt_kwargs_0, opt_args_0 = getopt.getopt(
            argv[1:],
            'ho:',
            ['help', 'option=']
        )
        option = None
        args_execute = None
        args_extend = None
        environs_extend = None
        # etc. -o "project=nsa_dev&application=maya"
        if opt_kwargs_0:
            input_option = None
            for i_key, i_value in opt_kwargs_0:
                if i_key in ('-h', '--help'):
                    __print_help()
                    #
                    sys.exit()
                elif i_key in ('-o', '--option'):
                    input_option = i_value

            if input_option:
                _ = __guess_by_kwargs(input_option)
                if _:
                    option, args_execute, args_extend, environs_extend = _
        # etc. nsa_dev.maya
        else:
            if opt_args_0:
                _ = __guess_by_args(
                    opt_args_0
                )
                if _ is not None:
                    option, args_execute, args_extend, environs_extend = _
        #
        if option is not None:
            __execute(option, args_execute, args_extend, environs_extend)
    #
    except getopt.GetoptError:
        # import traceback
        # sys.stderr.write(traceback.print_exc())
        sys.stderr.write('argv error\n')


def __guess_by_kwargs(opt_string):
    import lxbasic.core as bsc_core

    option_opt = bsc_core.ArgDictStringOpt(opt_string)
    project = option_opt.get('project')
    if not project:
        return

    # find resolver project
    import lxbasic.extra.methods as bsc_etr_methods
    import lxresolver.core as rsv_core
    resolver = rsv_core.RsvBase.generate_root()
    rsv_project = resolver.get_rsv_project(project=project)
    if not rsv_project:
        return

    app_arg = option_opt.get('application')
    if not app_arg:
        return
    # guess execute argument
    framework_scheme = rsv_project.get_framework_scheme()
    m = bsc_etr_methods.get_module(framework_scheme)
    app_execute_mapper = m.EtrBase.get_app_execute_mapper(rsv_project)
    if app_arg in app_execute_mapper:
        cfg = app_execute_mapper[app_arg]
        application = cfg['application']
        args_execute = cfg['args_execute']
    else:
        application = app_arg
        args_execute = ['-- {}'.format(application)]
    # guess extend and task arguments
    args_extend = []
    kwargs_task = None
    if 'task' in option_opt:
        task = option_opt['task']
        if 'asset' in option_opt:
            kwargs_task = dict(project=project, asset=option_opt['asset'], task=task)
        elif 'sequence' in option_opt:
            kwargs_task = dict(project=project, sequence=option_opt['sequence'], task=task)
        elif 'shot' in option_opt:
            kwargs_task = dict(project=project, shot=option_opt['shot'], task=task)
        elif 'resource' in option_opt:
            kwargs_task = dict(project=project, resource=option_opt['resource'], task=task)
        else:
            kwargs_task = dict(project=project, task=task)
    # generate option
    option = 'project={}&application={}'.format(project, application)
    return option, args_execute, args_extend, kwargs_task


def __guess_by_args(args):
    import lxbasic.log as bsc_log

    bsc_log.Log.trace_method_result(
        LOG_KEY,
        'execute from: {}'.format(__file__)
    )
    # etc. nsa_dev.maya
    launcher_arg = args[0]
    if '.' not in launcher_arg:
        raise SyntaxError(
            sys.stderr.write('argv error\n')
        )
    #
    _ = launcher_arg.split('.')
    if len(_) < 2:
        raise SyntaxError(
            sys.stderr.write('argv error\n')
        )
    #
    project = _[0]
    app_arg = '.'.join(_[1:])
    # guess resolver project
    import lxbasic.extra.methods as bsc_etr_methods
    import lxresolver.core as rsv_core
    resolver = rsv_core.RsvBase.generate_root()
    rsv_project = resolver.get_rsv_project(project=project)
    if not rsv_project:
        return
    # guess execute argument
    framework_scheme = rsv_project.get_framework_scheme()
    m = bsc_etr_methods.get_module(framework_scheme)
    app_execute_mapper = m.EtrBase.get_app_execute_mapper(rsv_project)
    if app_arg in app_execute_mapper:
        cfg = app_execute_mapper[app_arg]
        application = cfg['application']
        args_execute = cfg['args_execute']
    else:
        application = app_arg
        args_execute = ['-- {}'.format(application)]
    # guess extend and task arguments
    args_extend = args[1:]
    kwargs_task = None
    if len(args) == 2:
        arg_sub = args[1]
        # when arg_sub is file path, ignore
        if os.path.exists(arg_sub) is False:
            task_arg = arg_sub
            # asset/sequence/shot task, etc. td_tst.surfacing
            if '.' in task_arg:
                arg_sub = task_arg.split('.')
                if len(arg_sub) == 2:
                    resource, task = arg_sub
                    kwargs_task = dict(project=project, resource=resource, task=task)
                    args_extend = []
            # project task, etc. template
            else:
                task = args[1]
                kwargs_task = dict(project=project, task=task)
                args_extend = []
    # generate option
    option = 'project={}&application={}'.format(project, application)
    return option, args_execute, args_extend, kwargs_task


def __print_help():
    sys.stdout.write(
        '***** qsm-app *****\n'
        'etc.\n'
        'qsm-app {project}.{application}\n'
        '   qsm-app nsa_dev.katana\n'
        'qsm-app {project}.{application} {asset/sequence/shot/project}.{task}\n'
        '   qsm-app nsa_dev.katana td_test.surfacing\n'
        'qsm-app -o "project={project}&application={application}"\n'
        '   qsm-app -o "project=nsa_dev&application=maya"\n'
    )


def __execute(option, args_execute=None, args_extend=None, kwargs_task=None):
    import lxbasic.core as bsc_core

    import lxbasic.extra.methods as bsc_etr_methods

    import lxresolver.core as rsv_core

    option_opt = bsc_core.ArgDictStringOpt(option)
    # find project
    project = option_opt.get('project')
    if not project:
        return
    # find resolver project
    resolver = rsv_core.RsvBase.generate_root()
    rsv_project = resolver.get_rsv_project(project=project)
    if not rsv_project:
        return

    application = option_opt.get('application')
    if not application:
        return

    opt_packages_extend = []

    framework_scheme = rsv_project.get_framework_scheme()
    m = bsc_etr_methods.get_module(framework_scheme)
    framework_packages_extend = m.EtrBase.get_base_packages_extend()
    if framework_packages_extend:
        opt_packages_extend.extend(framework_packages_extend)

    rsv_app = rsv_project.get_rsv_app(application=application)

    command = rsv_app.get_command(
        args_execute=args_execute,
        args_extend=args_extend,
        packages_extend=opt_packages_extend
    )
    if command:
        sys.stdout.write(
            (
                '\033[34m'
                'resolved full command:\n'
                '\033[32m'
                '{}'
                '\033[0m\n'
            ).format(command)
        )

    if kwargs_task:
        environs_extend = m.EtrBase.get_task_environs_extend_(**kwargs_task)
        if 'project' in kwargs_task:
            # noinspection PyBroadException
            try:
                import lxbasic.shotgun as bsc_shotgun
                c = bsc_shotgun.StgConnector()
                stg_task = c.find_stg_task(**kwargs_task)
                if stg_task:
                    task_id = stg_task['id']
                    task_data = c.get_data_from_task_id(task_id)
                    rsv_project.auto_create_user_task_directory_by_task_data(task_data)
            except Exception:
                bsc_core.BscException.set_print()
    else:
        environs_extend = m.EtrBase.get_project_environs_extend(project)

    if environs_extend:
        sys.stdout.write(
            (
                '\033[34m'
                'resolved environments:\n'
                '\033[32m'
                '{}'
                '\033[0m\n'
            ).format('\n'.join(['{}={}'.format(k.rjust(20), v) for k, v in environs_extend.items()]))
        )
    if args_execute:
        rsv_app.execute_command(
            args_execute=args_execute,
            args_extend=args_extend,
            packages_extend=opt_packages_extend,
            #
            environs_extend=environs_extend,
            # clear_environ='auto'
        )


if __name__ == '__main__':
    main(sys.argv)
