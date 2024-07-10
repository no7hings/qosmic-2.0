# coding:utf-8
import functools

import fnmatch

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

import lxbasic.extra.methods as bsc_etr_methods


class AbsSsnConfigureBaseDef(object):
    @property
    def configure(self):
        raise NotImplementedError()

    def _init_configure_base_def_(self):
        self._basic_configure = self.configure.get_as_content(
            'option'
        )
        self._gui_configure = self.configure.get_as_content(
            'option.gui'
        )

    def get_basic_configure(self):
        return self._basic_configure

    basic_configure = property(get_basic_configure)

    # gui
    def get_gui_configure(self):
        return self._gui_configure

    gui_configure = property(get_gui_configure)

    @property
    def gui_group_name(self):
        return self._gui_configure.get(
            'group_name'
        )

    def get_gui_name_(self, language='en_US'):
        if language == 'chs':
            _ = self._gui_configure.get('name_chs')
            if _:
                return _
        return self._gui_configure.get(
            'name'
        )

    def get_gui_tool_tip_(self, language='en_US'):
        if language == 'chs':
            _ = self._gui_configure.get('tool_tip_chs')
            if _:
                return _
        return self._gui_configure.get(
            'tool_tip'
        )

    def get_gui_name(self):
        return self._gui_configure.get(
            'name'
        )

    gui_name = property(get_gui_name)

    @property
    def gui_icon_name(self):
        return self._gui_configure.get(
            'icon_name'
        )

    @property
    def gui_icon_file(self):
        return bsc_resource.RscExtendIcon.get(
            self.gui_icon_name
        )

    def get_is_visible(self):
        return True


class AbsSsnEnvironmentBaseDef(object):
    def _init_environment_base_def_(self):
        # self._rez_beta = bsc_core.EnvBaseMtd.get('REZ_BETA')
        pass

    @classmethod
    def get_is_td_enable(cls):
        return bsc_core.EnvExtraMtd.get_is_td_enable()

    @classmethod
    def get_is_beta_enable(cls):
        return bsc_core.EnvExtraMtd.get_is_beta_enable()


class AbsSsnGener(
    AbsSsnConfigureBaseDef,
    AbsSsnEnvironmentBaseDef,
):
    Platform = bsc_core.BscPlatform
    Application = bsc_core.BscApplication

    def __init__(self, *args, **kwargs):
        if 'type' in kwargs:
            self.__type = kwargs['type']
        else:
            self.__type = None
        #
        if 'hook' in kwargs:
            self.__key = kwargs['hook']
        else:
            self.__key = None
        #
        if 'name' in kwargs:
            self.__name = kwargs['name']
        else:
            self.__name = str(self.__key).split('/')[-1]
        #
        if 'configure' in kwargs:
            self._configure = kwargs['configure']
        else:
            raise KeyError()
        #
        if 'variants' in kwargs:
            self._configure.set(
                'variants', kwargs['variants']
            )
            self._variants = kwargs['variants']
        else:
            self._variants = {}
        #
        self._configure.do_flatten()
        #
        self._user = bsc_core.BscSystem.get_user_name()
        self._host = bsc_core.BscSystem.get_host()
        self._platform = bsc_core.BscSystem.get_platform()
        self._application = bsc_core.BscSystem.get_application()
        self._system = bsc_core.BscSystem.get_current()
        self._system_includes = bsc_core.BscSystem.get_system_includes(
            self._configure.get(
                'option.systems'
            ) or []
        )
        self._variants['user'] = self._user
        self._variants['host'] = self._host
        self._variants['platform'] = self._platform
        self._variants['application'] = self._application
        #
        self._hook_yaml_file_path = None
        self._hook_python_file_path = None
        self._hook_shell_file_path = None

        self._gui_widget = None
        self._prx_window = None

        self._init_environment_base_def_()
        self._init_configure_base_def_()

    def get_type(self):
        return self.__type

    type = property(get_type)

    def get_name(self):
        if self.__name:
            return self.__name
        return self.__key

    name = property(get_name)

    def get_key(self):
        return self.__key

    key = property(get_key)

    def get_hook(self):
        return self.__key

    hook = property(get_hook)

    def get_group(self):
        return self.get_type()

    group = property(get_group)

    def get_configure(self):
        return self._configure

    configure = property(get_configure)

    def reload_configure(self):
        self._configure.reload()

    #
    def get_platform(self):
        return self._platform

    platform = property(get_platform)

    def get_application(self):
        return self._application

    application = property(get_application)

    def get_user(self):
        return self._user

    user = property(get_user)

    def get_gui_window_name(self):
        language = bsc_core.EnvExtraMtd.get_ui_language()
        gui_name = self.get_gui_name_(language)
        gui_name = bsc_core.auto_string(gui_name)
        if self.get_is_td_enable() is True:
            return '[ALPHA] {} - {}'.format(
                    gui_name, str(self.application).capitalize()
                )
        elif self.get_is_beta_enable() is True:
            return '[BETA] {} - {}'.format(
                    gui_name, str(self.application).capitalize()
                )
        return '{} - {}'.format(
                gui_name, str(self.application).capitalize()
            )

    @property
    def system(self):
        return self._system

    @property
    def system_includes(self):
        return self._system_includes

    @property
    def variants(self):
        return self._variants

    def get_is_loadable(self):
        return self.system in self.system_includes

    def get_is_executable(self):
        return True

    def set_run(self):
        if self.get_is_loadable():
            if self.get_is_executable():
                self.pre_run_fnc()
                self.execute()
                self.post_run_fnc()

    def pre_run_fnc(self):
        pass

    def execute(self):
        if self._hook_python_file_path:
            self.execute_python_file(
                self._hook_python_file_path, session=self
            )

    def post_run_fnc(self):
        pass

    @staticmethod
    def execute_python_file(file_path, **kwargs):
        # use for python 3
        # with open(file_path, 'r') as f:
        #     exec (f.read())
        # use for python 2
        bsc_log.Log.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        kwargs['__name__'] = '__main__'
        execfile(file_path, kwargs)
        bsc_log.Log.trace_method_result(
            'option-hook', 'complete for: "{}"'.format(
                file_path
            )
        )

    @staticmethod
    def execute_python_script(cmd, **kwargs):
        # noinspection PyUnusedLocal
        session = kwargs['session']
        exec cmd

    @staticmethod
    def execute_shell_file_use_terminal(file_path, **kwargs):
        bsc_log.Log.trace_method_result(
            'option-hook', 'start for : "{}"'.format(
                file_path
            )
        )
        session = kwargs['session']
        if bsc_core.BasPlatform.get_is_linux():
            cmds = [
                'gnome-terminal',
                '-t "{}-{}"'.format(
                    session.get_name(), bsc_core.BscSystem.get_time_tag()
                ),
                '-e "bash -l {}"'.format(file_path)
            ]
            bsc_core.BscProcess.execute_as_trace_use_thread(
                ' '.join(cmds)
            )
        elif bsc_core.BasPlatform.get_is_windows():
            # when process finish use /c for auto close terminal, /k not
            cmds = ['start', 'cmd', '/c', file_path]
            bsc_core.BscProcess.execute_as_trace_use_thread(
                ' '.join(cmds)
            )

        bsc_log.Log.trace_method_result(
            'option-hook', 'complete for: "{}"'.format(
                file_path
            )
        )

    @staticmethod
    def execute_shell_script_use_terminal(cmd, **kwargs):
        session = kwargs['session']
        if bsc_core.BasPlatform.get_is_linux():
            cmds = [
                'gnome-terminal',
                '-t "{}-{}"'.format(
                    session.get_name(), bsc_core.BscSystem.get_time_tag()
                ),
                '--', 'bash', '-l', '-c', cmd
            ]
            bsc_core.BscProcess.execute_as_trace_use_thread(
                ' '.join(cmds)
            )
        elif bsc_core.BasPlatform.get_is_windows():
            cmds = ['start', 'cmd', '/c', cmd]
            bsc_core.BscProcess.execute_as_trace_use_thread(
                ' '.join(cmds)
            )

    @staticmethod
    def execute_shell_script(cmd, use_thread=True):
        if use_thread is True:
            bsc_core.BscProcess.execute_use_thread(cmd)
        else:
            bsc_core.BscProcess.execute(cmd)

    def set_gui(self, widget):
        self._gui_widget = widget

    def set_prx_window(self, prx_window):
        self._prx_window = prx_window

    def get_prx_window(self):
        return self._prx_window

    def gui_execute_shell_script(self, cmd):
        if self._gui_widget is not None:
            self._gui_widget._run_fnc_use_thread_(
                functools.partial(
                    bsc_core.BscProcess.execute, cmd
                )
            )
        else:
            bsc_core.BscProcess.execute_use_thread(cmd)

    def get_is_system_matched(self, system_key):
        return self.system in bsc_core.BscSystem.get_system_includes([system_key])

    @classmethod
    def _get_choice_scheme_matched_(cls, choice_scheme, choice_scheme_includes):
        for i_choice_scheme in choice_scheme_includes:
            if fnmatch.filter(
                    [choice_scheme], i_choice_scheme
            ):
                return True
        return False

    def set_execute_fnc(self, fnc):
        pass

    def set_configure_yaml_file(self, file_path):
        self._hook_yaml_file_path = file_path

    def get_configure_yaml_file(self):
        return self._hook_yaml_file_path

    def set_python_script_file(self, file_path):
        self._hook_python_file_path = file_path

    def get_python_script_file(self):
        return self._hook_python_file_path

    def get_python_script(self):
        if self._hook_python_file_path:
            return bsc_storage.StgFileOpt(self._hook_python_file_path).set_read()

    def set_shell_script_file(self, file_path):
        self._hook_shell_file_path = file_path

    def get_shell_script_file(self):
        return self._hook_shell_file_path

    def get_shell_script(self):
        pass

    def open_configure_file(self):
        if self._hook_yaml_file_path:
            bsc_etr_methods.EtrBase.open_ide(
                self._hook_yaml_file_path
            )

    def open_configure_directory(self):
        if self._hook_yaml_file_path:
            bsc_storage.StgFileOpt(self._hook_yaml_file_path).open_in_system()

    def open_python_script_file(self):
        if self._hook_python_file_path:
            bsc_etr_methods.EtrBase.open_ide(
                self._hook_python_file_path
            )

    def open_execute_file(self):
        pass

    def set_reload(self):
        self._configure.reload()
        self._configure.do_flatten()

    def get_engine(self):
        return self._configure.get(
            'hook_option.engine'
        )

    def get_packages_extend(self):
        return self._configure.get(
            'hook_option.rez.extend_packages'
        ) or []

    def get_environs_extend(self):
        return self._configure.get(
            'hook_option.rez.extend_environs'
        ) or []

    def get_is_match_condition(self, match_dict):
        condition_string = self._configure.get(
            'rsv-match-condition'
        )
        if condition_string:
            return self._match_fnc_(condition_string, match_dict)
        return True

    @classmethod
    def _match_fnc_(cls, condition_string, match_dict):
        if condition_string:
            for i in condition_string.split('&'):
                i_key, i_condition = i.split('=')
                if i_key not in match_dict:
                    continue
                #
                i_input = match_dict[i_key]
                #
                if not i_input:
                    return False
                #
                if '+' in i_condition:
                    i_values = i_condition.split('+')
                    if i_input not in i_values:
                        return False
                else:
                    if i_condition != i_input:
                        return False
        return True

    @classmethod
    def open_url(cls, url):
        bsc_core.UrlMtd.open_in_chrome(url)

    def open_file(self, path):
        pass

    def open_directory(self, path):
        pass

    def __str__(self):
        return '{}(type="{}", key={})'.format(
            self.__class__.__name__,
            self.get_type(),
            self.get_key()
        )

    def __repr__(self):
        return self.__str__()


class AbsSsnCommand(AbsSsnGener):
    def __init__(self, *args, **kwargs):
        super(AbsSsnCommand, self).__init__(*args, **kwargs)

    def execute(self):
        type_ = self.basic_configure.get('type')
        if type_ == 'shell-script':
            shell_file_path = self.get_shell_script_file()
            if shell_file_path:
                self.execute_shell_file_use_terminal(shell_file_path, session=self)
            else:
                command = self.basic_configure.get('command')
                if command:
                    self.execute_shell_script_use_terminal(command, session=self)
        elif type_ == 'python-script':
            python_file_path = self.get_python_script_file()
            if python_file_path:
                self.execute_python_file(python_file_path, session=self)
            else:
                command = self.basic_configure.get('command')
                self.execute_python_script(command, session=self)


class AbsSsnOptionGener(AbsSsnGener):
    def __init__(self, *args, **kwargs):
        super(AbsSsnOptionGener, self).__init__(*args, **kwargs)
        self._init_option_def(kwargs['option'])

    def _init_option_def(self, option):
        self._option_opt = bsc_core.ArgDictStringOpt(
            option
        )
        self._completion_option_by_script()

    def _completion_option_by_script(self):
        option_opt = self.get_option_opt()
        #
        # inherit_keys = option_opt.get('inherit_keys')
        script_dict = self.configure.get('hook_option.script') or {}
        for k, v in script_dict.items():
            if option_opt.get_key_is_exists(k) is False:
                if isinstance(v, dict):
                    pass
                else:
                    option_opt.set(
                        k, v
                    )

    def get_option_opt(self):
        return self._option_opt

    option_opt = property(get_option_opt)

    def get_option(self):
        return self._option_opt.to_string()

    option = property(get_option)

    def get_extra_hook_options(self):
        lis = []
        script_dict = self.configure.get('hook_option.script') or {}
        extra_dict = self.configure.get('hook_option.extra') or {}
        for k, v in extra_dict.items():
            i_script_dict = v['script']
            for i_k, i_v in script_dict.items():
                if i_k not in i_script_dict:
                    i_script_dict[i_k] = i_v
            #
            i_hook_option_opt = bsc_core.ArgDictStringOpt(i_script_dict)
            i_hook_option_opt.set(
                'option_hook_key', self.option_opt.get('option_hook_key')
            )
            lis.append(
                i_hook_option_opt.to_string()
            )
        return lis

    def __str__(self):
        return '{}(type="{}", key={}, option="{}")'.format(
            self.__class__.__name__,
            self.get_type(),
            self.get_key(),
            self.get_option()
        )

    def __repr__(self):
        return self.__str__()


class GenerSession(AbsSsnGener):
    def __init__(self, *args, **kwargs):
        super(GenerSession, self).__init__(*args, **kwargs)


class ScriptSession(AbsSsnCommand):
    def __init__(self, *args, **kwargs):
        super(ScriptSession, self).__init__(*args, **kwargs)


class GenerOptionSession(AbsSsnOptionGener):
    def __init__(self, *args, **kwargs):
        super(GenerOptionSession, self).__init__(*args, **kwargs)
