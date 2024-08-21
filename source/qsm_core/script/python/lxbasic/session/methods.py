# coding:utf-8
import six

import functools

import lxbasic.log as bsc_log

import lxbasic.content as bsc_content

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

    @classmethod
    def generate_menu_contents(cls, hook_options, language):
        d_ = bsc_content.Dict()
        for i_hook_option in hook_options:
            i_hook_args = cls.get_args(i_hook_option)
            if i_hook_args:
                i_session, i_execute_fnc = i_hook_args
                if i_session.get_is_loadable() is True:
                    i_hook_option_opt = i_session.option_opt
                    i_gui_configure = i_session.gui_configure
                    i_gui_parent_path = '/'
                    #
                    i_gui_name = i_gui_configure.get('name')
                    i_gui_group_name = i_gui_configure.get('group_name')
                    if language == 'chs':
                        if i_hook_option_opt.get_key_is_exists('gui_name_chs'):
                            i_gui_name = i_hook_option_opt.get('gui_name_chs')

                        if i_hook_option_opt.get_key_is_exists('gui_group_name_chs'):
                            i_gui_group_name = i_hook_option_opt.get('gui_group_name_chs')

                        if i_hook_option_opt.get_value():
                            if i_hook_option_opt.get_key_is_exists('gui_parent_chs'):
                                i_gui_parent_path = i_hook_option_opt.get('gui_parent_chs')
                    else:
                        if i_hook_option_opt.get_key_is_exists('gui_name'):
                            i_gui_name = i_hook_option_opt.get('gui_name')

                        if i_hook_option_opt.get_key_is_exists('gui_group_name'):
                            i_gui_group_name = i_hook_option_opt.get('gui_group_name')

                        if i_hook_option_opt.get_value():
                            if i_hook_option_opt.get_key_is_exists('gui_parent'):
                                i_gui_parent_path = i_hook_option_opt.get('gui_parent')

                    i_gui_parent_path_opt = bsc_core.BscPathOpt(i_gui_parent_path)

                    if i_gui_parent_path_opt.get_is_root():
                        i_gui_path = six.u('/{}').format(i_gui_name)
                    else:
                        i_gui_path = six.u('{}/{}').format(i_gui_parent_path, i_gui_name)

                    if i_gui_group_name:
                        if i_gui_parent_path_opt.get_is_root():
                            i_gui_separator_path = six.u('/{}').format(i_gui_group_name)
                        else:
                            i_gui_separator_path = six.u('{}/{}').format(i_gui_parent_path, i_gui_group_name)

                        d_.set(
                            six.u('{}.properties.type').format(i_gui_separator_path), 'separator'
                        )
                        d_.set(
                            six.u('{}.properties.name').format(i_gui_separator_path), i_gui_configure.get('group_name')
                        )

                    d_.set(
                        six.u('{}.properties.type').format(i_gui_path), 'action'
                    )
                    d_.set(
                        six.u('{}.properties.group_name').format(i_gui_path), i_gui_group_name
                    )
                    d_.set(
                        six.u('{}.properties.name').format(i_gui_path), i_gui_name
                    )
                    d_.set(
                        six.u('{}.properties.icon_name').format(i_gui_path), i_gui_configure.get('icon_name')
                    )
                    if i_hook_option_opt.get_value():
                        if i_hook_option_opt.get_key_is_exists('gui_icon_name'):
                            d_.set(
                                six.u('{}.properties.icon_name').format(i_gui_path),
                                i_hook_option_opt.get('gui_icon_name')
                            )
                    #
                    d_.set(
                        six.u('{}.properties.executable_fnc').format(i_gui_path),
                        i_session.get_is_executable
                    )
                    d_.set(
                        six.u('{}.properties.execute_fnc').format(i_gui_path),
                        i_execute_fnc
                    )
        return d_
