# coding:utf-8
import six

import functools


def get_hook_args(key, search_paths=None):
    import lxbasic.storage as bsc_storage

    import lxbasic.session as bsc_session

    import lxsession.core as ssn_core

    import lxbasic.content as bsc_content

    yaml_file_path = ssn_core.SsnHookFileMtd.get_yaml(key, search_paths)
    if yaml_file_path:
        yaml_file_opt = bsc_storage.StgFileOpt(yaml_file_path)
        configure = bsc_content.Content(value=yaml_file_opt.path)
        type_name = configure.get('option.type')
        if type_name in {
            'application',
            'tool',
            'dcc-tool',
            'kit-panel',
            'tool-panel', 'kit-panel',
            'dcc-tool-panel', 'dcc-menu', 'dcc-action',
            'rsv-tool-panel', 'rsv-loader', 'rsv-publisher'
        }:
            session = bsc_session.GenerSession(
                type=type_name,
                hook=key,
                configure=configure
            )
        elif type_name in {
            'python-script', 'shell-script'
        }:
            session = bsc_session.ScriptSession(
                type=type_name,
                hook=key,
                configure=configure
            )
        else:
            raise TypeError()

        session.set_configure_yaml_file(yaml_file_path)
        python_file_path = ssn_core.SsnHookFileMtd.get_python(key, search_paths)
        if python_file_path is not None:
            session.set_python_script_file(python_file_path)
        shell_file_path = ssn_core.SsnHookFileMtd.get_shell(key, search_paths)
        if shell_file_path:
            session.set_shell_script_file(shell_file_path)

        execute_fnc = functools.partial(session.execute)
        return session, execute_fnc


def execute_hook(key):
    import lxbasic.log as bsc_log

    hook_args = get_hook_args(key)
    if hook_args is not None:
        session, execute_fnc = hook_args
        execute_fnc()
        return session
    else:
        bsc_log.Log.trace_method_warning(
            'hook execute',
            'hook_key="{}" is not found'.format(key)
        )


def get_option_hook_args(option, search_paths=None):
    def execute_fnc():
        session.execute_python_file(
            python_file_path, session=session
        )

    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxbasic.session as bsc_session

    import lxbasic.content as bsc_content

    import lxsession.core as ssn_core

    import lxsession.objects as ssn_objects

    option_opt = bsc_core.ArgDictStringOpt(option)

    option_hook_key = option_opt.get('option_hook_key')

    yaml_file_path = ssn_core.SsnOptionHookFileMtd.get_yaml(option_hook_key, search_paths)
    if yaml_file_path:
        python_file_path = ssn_core.SsnOptionHookFileMtd.get_python(option_hook_key, search_paths)
        python_file_opt = bsc_storage.StgFileOpt(python_file_path)
        yaml_file_opt = bsc_storage.StgFileOpt(yaml_file_path)
        if python_file_opt.get_is_exists() is True and yaml_file_opt.get_is_exists() is True:
            configure = bsc_content.Content(value=yaml_file_opt.path)
            type_name = configure.get('option.type')
            #
            session = None
            if type_name in {
                'action',
                'launcher'
            }:
                session = bsc_session.GenerOptionSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'dtb-action':
                session = ssn_objects.DatabaseOptionActionSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'launcher':
                session = bsc_session.GenerOptionSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'tool-panel':
                session = ssn_objects.OptionToolPanelSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'rsv-tool-panel':
                session = ssn_objects.RsvOptionToolPanelSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'method':
                session = ssn_objects.SsnOptionMethod(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name in {'rsv-project-batcher', 'rsv-project-method'}:
                session = ssn_objects.RsvProjectMethodSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name in {'rsv-task-batcher', 'rsv-task-method'}:
                session = ssn_objects.RsvTaskMethodSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            elif type_name == 'kit-panel':
                session = ssn_objects.OptionGuiSession(
                    type=type_name,
                    hook=option_hook_key,
                    configure=configure,
                    option=option_opt.to_string()
                )
            else:
                raise TypeError()
            #
            session.set_python_script_file(python_file_path)
            session.set_configure_yaml_file(yaml_file_path)
            return session, execute_fnc
    else:
        raise RuntimeError(
            bsc_log.Log.trace_method_error(
                'option-hook gain',
                'option-hook key="{}" configue (.yml) is not found'.format(option_hook_key)
            )
        )


def get_option_hook_configure(option):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxbasic.content as bsc_content

    import lxsession.core as ssn_core

    option_opt = bsc_core.ArgDictStringOpt(option)

    option_hook_key = option_opt.get('option_hook_key')

    yaml_file_path = ssn_core.SsnOptionHookFileMtd.get_yaml(option_hook_key)
    if yaml_file_path:
        yaml_file_opt = bsc_storage.StgFileOpt(yaml_file_path)
        if yaml_file_opt.get_is_exists() is True:
            return bsc_content.Content(value=yaml_file_opt.path)


def execute_option_hook(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        execute_fnc()
        return session


def get_option_hook_session(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        return session


def get_option_hook_shell_script_command(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        return session, session.get_shell_script_command()


def execute_option_hook_by_shell(option, block=False):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        #
        session.execute_hook_with_shell(block)
        return session


def execute_option_hook_by_deadline(option):
    hook_args = get_option_hook_args(option)
    if hook_args is not None:
        session, execute_fnc = hook_args
        #
        session.execute_hook_with_deadline()
        return session


if __name__ == '__main__':
    pass
