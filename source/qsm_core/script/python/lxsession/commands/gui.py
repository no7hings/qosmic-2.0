# coding:utf-8
import six


def get_menu_content_by_hooks(hooks):
    import lxcontent.core as ctt_core

    import lxbasic.core as bsc_core

    from . import hook as ssn_cmd_hook

    d_ = ctt_core.Dict()
    for i_hook in hooks:
        if isinstance(i_hook, six.string_types):
            i_hook_key = i_hook
            i_extra_kwargs = None
        elif isinstance(i_hook, dict):
            i_hook_key = i_hook.keys()[0]
            i_extra_kwargs = i_hook.values()[0]
        else:
            raise RuntimeError()
        #
        i_hook_args = ssn_cmd_hook.get_hook_args(i_hook_key)
        if i_hook_args:
            i_session, i_execute_fnc = i_hook_args
            if i_session.get_is_loadable() is True:
                i_gui_configure = i_session.gui_configure
                #
                i_gui_parent_path = '/'
                #
                i_gui_name = i_gui_configure.get('name')
                if i_extra_kwargs:
                    if 'gui_parent' in i_extra_kwargs:
                        i_gui_parent_path = i_extra_kwargs['gui_parent']
                #
                i_gui_parent_path_opt = bsc_core.PthNodeOpt(i_gui_parent_path)
                #
                if i_gui_parent_path_opt.get_is_root():
                    i_gui_path = '/{}'.format(i_gui_name)
                else:
                    i_gui_path = '{}/{}'.format(i_gui_parent_path, i_gui_name)
                #
                i_gui_separator_name = i_gui_configure.get('group_name')
                if i_gui_separator_name:
                    if i_gui_parent_path_opt.get_is_root():
                        i_gui_separator_path = '/{}'.format(i_gui_separator_name)
                    else:
                        i_gui_separator_path = '{}/{}'.format(i_gui_parent_path, i_gui_separator_name)
                    #
                    d_.set(
                        '{}.properties.type'.format(i_gui_separator_path), 'separator'
                    )
                    d_.set(
                        '{}.properties.name'.format(i_gui_separator_path), i_gui_configure.get('group_name')
                    )
                #
                d_.set(
                    '{}.properties.type'.format(i_gui_path), 'action'
                )
                d_.set(
                    '{}.properties.group_name'.format(i_gui_path), i_gui_configure.get('group_name')
                )
                d_.set(
                    '{}.properties.name'.format(i_gui_path), i_gui_configure.get('name')
                )
                d_.set(
                    '{}.properties.icon_name'.format(i_gui_path), i_gui_configure.get('icon_name')
                )
                if i_extra_kwargs:
                    if 'gui_icon_name' in i_extra_kwargs:
                        d_.set(
                            '{}.properties.icon_name'.format(i_gui_path), i_extra_kwargs.get('gui_icon_name')
                        )
                #
                d_.set(
                    '{}.properties.executable_fnc'.format(i_gui_path), i_session.get_is_executable
                )
                d_.set(
                    '{}.properties.execute_fnc'.format(i_gui_path), i_execute_fnc
                )
    return d_


def get_menu_content_by_hook_options(hook_options):
    import lxcontent.core as ctt_core

    import lxbasic.core as bsc_core

    from . import hook as ssn_cmd_hook

    d_ = ctt_core.Dict()
    for i_hook_option in hook_options:
        i_hook_args = ssn_cmd_hook.get_option_hook_args(i_hook_option)
        if i_hook_args:
            i_session, i_execute_fnc = i_hook_args
            if i_session.get_is_loadable() is True:
                i_hook_option_opt = i_session.option_opt
                i_gui_configure = i_session.gui_configure
                i_gui_parent_path = '/'
                #
                i_gui_name = i_gui_configure.get('name')
                if i_hook_option_opt.get_key_is_exists('gui_name'):
                    i_gui_name = i_hook_option_opt.get('gui_name')
                #
                i_gui_group_name = i_gui_configure.get('group_name')
                if i_hook_option_opt.get_key_is_exists('gui_group_name'):
                    i_gui_group_name = i_hook_option_opt.get('gui_group_name')
                #
                if i_hook_option_opt.get_value():
                    if i_hook_option_opt.get_key_is_exists('gui_parent'):
                        i_gui_parent_path = i_hook_option_opt.get('gui_parent')
                #
                i_gui_parent_path_opt = bsc_core.PthNodeOpt(i_gui_parent_path)
                #
                if i_gui_parent_path_opt.get_is_root():
                    i_gui_path = '/{}'.format(i_gui_name)
                else:
                    i_gui_path = '{}/{}'.format(i_gui_parent_path, i_gui_name)
                #
                if i_gui_group_name:
                    if i_gui_parent_path_opt.get_is_root():
                        i_gui_separator_path = '/{}'.format(i_gui_group_name)
                    else:
                        i_gui_separator_path = '{}/{}'.format(i_gui_parent_path, i_gui_group_name)
                    #
                    d_.set(
                        '{}.properties.type'.format(i_gui_separator_path), 'separator'
                    )
                    d_.set(
                        '{}.properties.name'.format(i_gui_separator_path), i_gui_configure.get('group_name')
                    )
                #
                d_.set(
                    '{}.properties.type'.format(i_gui_path), 'action'
                )
                d_.set(
                    '{}.properties.group_name'.format(i_gui_path), i_gui_group_name
                )
                d_.set(
                    '{}.properties.name'.format(i_gui_path), i_gui_name
                )
                d_.set(
                    '{}.properties.icon_name'.format(i_gui_path), i_gui_configure.get('icon_name')
                )
                if i_hook_option_opt.get_value():
                    if i_hook_option_opt.get_key_is_exists('gui_icon_name'):
                        d_.set(
                            '{}.properties.icon_name'.format(i_gui_path), i_hook_option_opt.get('gui_icon_name')
                        )
                #
                d_.set(
                    '{}.properties.executable_fnc'.format(i_gui_path), i_session.get_is_executable
                )
                d_.set(
                    '{}.properties.execute_fnc'.format(i_gui_path), i_execute_fnc
                )
    return d_


def get_menu_content_by_hook_options_(hook_options):
    import lxcontent.core as ctt_core

    import lxbasic.core as bsc_core

    from . import hook as ssn_cmd_hook

    d_ = ctt_core.Dict()
    for i_key in hook_options:
        if isinstance(i_key, six.string_types):
            i_hook_option = i_key
            i_extra_kwargs = None
        elif isinstance(i_key, dict):
            i_hook_option = i_key.keys()[0]
            i_extra_kwargs = i_key.values()[0]
        else:
            raise RuntimeError()
        #
        i_hook_args = ssn_cmd_hook.get_option_hook_args(i_hook_option)
        if i_hook_args:
            i_session, i_execute_fnc = i_hook_args
            if i_session.get_is_loadable() is True:
                i_hook_option_opt = i_session.option_opt
                i_hook_option_opt.update_from(i_extra_kwargs)
                i_gui_configure = i_session.gui_configure
                i_gui_parent_path = '/'
                #
                i_gui_name = i_gui_configure.get('name')
                if i_hook_option_opt.get_key_is_exists('gui_name'):
                    i_gui_name = i_hook_option_opt.get('gui_name')
                #
                i_gui_group_name = i_gui_configure.get('group_name')
                if i_hook_option_opt.get_key_is_exists('gui_group_name'):
                    i_gui_group_name = i_hook_option_opt.get('gui_group_name')
                #
                if i_hook_option_opt.get_value():
                    if i_hook_option_opt.get_key_is_exists('gui_parent'):
                        i_gui_parent_path = i_hook_option_opt.get('gui_parent')
                #
                i_gui_parent_path_opt = bsc_core.PthNodeOpt(i_gui_parent_path)
                #
                if i_gui_parent_path_opt.get_is_root():
                    i_gui_path = '/{}'.format(i_gui_name)
                else:
                    i_gui_path = '{}/{}'.format(i_gui_parent_path, i_gui_name)
                #
                if i_gui_group_name:
                    if i_gui_parent_path_opt.get_is_root():
                        i_gui_separator_path = '/{}'.format(i_gui_group_name)
                    else:
                        i_gui_separator_path = '{}/{}'.format(i_gui_parent_path, i_gui_group_name)
                    #
                    d_.set(
                        '{}.properties.type'.format(i_gui_separator_path), 'separator'
                    )
                    d_.set(
                        '{}.properties.name'.format(i_gui_separator_path), i_gui_configure.get('group_name')
                    )
                #
                d_.set(
                    '{}.properties.type'.format(i_gui_path), 'action'
                )
                d_.set(
                    '{}.properties.group_name'.format(i_gui_path), i_gui_group_name
                )
                d_.set(
                    '{}.properties.name'.format(i_gui_path), i_gui_name
                )
                d_.set(
                    '{}.properties.icon_name'.format(i_gui_path), i_gui_configure.get('icon_name')
                )
                if i_hook_option_opt.get_value():
                    if i_hook_option_opt.get_key_is_exists('gui_icon_name'):
                        d_.set(
                            '{}.properties.icon_name'.format(i_gui_path), i_hook_option_opt.get('gui_icon_name')
                        )
                #
                d_.set(
                    '{}.properties.executable_fnc'.format(i_gui_path), i_session.get_is_executable
                )
                d_.set(
                    '{}.properties.execute_fnc'.format(i_gui_path), i_execute_fnc
                )
    return d_


if __name__ == '__main__':
    pass

