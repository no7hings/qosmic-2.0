# coding:utf-8
import copy

import threading

import functools

import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# resolver
from .. import core as rsv_core


class AbsRsvAppDef(object):
    Applications = rsv_core.RsvApplications
    CACHE = dict()
    BIN = None

    def __init__(self, rsv_project, application, configure):
        self._rsv_project = rsv_project
        #
        self._project = rsv_project.get_name()
        self._platform = bsc_core.SysBaseMtd.get_platform()
        #
        if application == 'python':
            self._application = 'maya'
        elif application == 'shotgun':
            self._application = 'maya'
        elif application == 'usd':
            self._application = 'maya'
        elif application == 'gui':
            self._application = 'maya'
        elif application == 'rv':
            self._application = 'maya'
        elif application == 'rv-movie-convert':
            self._application = 'maya'
        else:
            self._application = application
        #
        self._configure = configure
        #
        self._variants = dict(
            home=bsc_core.SysBaseMtd.get_home_directory(),
            project=self._project,
            platfrom=self._platform,
            application=self._application
        )

    def get_key(self):
        return '{}.{}'.format(
            self._project,
            self._application
        )

    def get_project(self):
        return self._project

    project = property(get_project)

    def get_application(self):
        return self._application

    application = property(get_application)

    def get_configure(self):
        return self._configure

    configure = property(get_configure)

    def get_user_package_roots(self):
        list_ = []
        for i_p in self._configure.get('package-user-root-patterns.{}'.format(self._platform)) or []:
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.update_variants(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_pre_release_package_roots(self):
        list_ = []
        for i_p in self._configure.get('package-pre_release-root-patterns.{}'.format(self._platform)) or []:
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.update_variants(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_release_package_roots(self):
        list_ = []
        for i_p in self._configure.get('package-release-root-patterns.{}'.format(self._platform)) or []:
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.update_variants(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def _get_package_file_patterns(self):
        return self._configure.get('package-file-patterns') or []

    def _get_configure_root_patterns(self):
        platform = bsc_core.SysBaseMtd.get_platform()
        return self._configure.get('configure-root-patterns.{}'.format(platform)) or []

    def _get_configure_file_patterns(self):
        return self._configure.get('configure-file-patterns') or []

    def _get_configure_directory(self):
        for i_p in self._get_configure_root_patterns():
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.update_variants(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                i_results = bsc_core.RawTextsMtd.sort_by_number(i_results)
                return i_results[-1]

    def _get_configure_file(self):
        d = self._get_configure_directory()
        variants = dict(
            root=d,
            project=self._project,
            application=self._application
        )
        for i_p in self._get_configure_file_patterns():
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.update_variants(**variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                i_results = bsc_core.RawTextsMtd.sort_by_number(i_results)
                return i_results[-1]

    def get_package(self, package_name):
        pass

    def get_args(self, packages_extend=None):
        raise NotImplementedError()

    def get_packages(self):
        pass

    def get_command(self, args_execute=None, args_extend=None, packages_extend=None):
        raise NotImplementedError()

    def execute_command(self, args_execute=None, args_extend=None, packages_extend=None, **sub_progress_kwargs):
        cmd = self.get_command(
            args_execute=args_execute,
            args_extend=args_extend,
            packages_extend=packages_extend
        )
        if cmd:
            bsc_log.Log.trace_method_result(
                'execute app',
                'command=`{}` is started'.format(cmd)
            )
            bsc_core.PrcBaseMtd.execute_with_result(
                cmd,
                **sub_progress_kwargs
            )

    @classmethod
    def execute_with_result(cls, command, **sub_progress_kwargs):
        bsc_log.Log.trace_method_result(
            'execute app',
            'command=`{}` is started'.format(command)
        )
        bsc_core.PrcBaseMtd.execute_with_result(
            command,
            **sub_progress_kwargs
        )

    @classmethod
    def execute_with_result_use_thread(cls, command, **sub_progress_kwargs):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute_with_result,
                cmd=command,
                **sub_progress_kwargs
            )
        )
        t_0.start()
        # t_0.join()

    def _test_(self):
        print self.get_package('pglauncher')

    def __str__(self):
        return str(self._configure)


class AbsRsvAppDefault(AbsRsvAppDef):
    BIN = 'rez-env'

    def __init__(self, *args, **kwargs):
        super(AbsRsvAppDefault, self).__init__(*args, **kwargs)

    def get_args(self, packages_extend=None):
        if self._application == self.Applications.Lynxi:
            return ['lxdcc']

        key = self.get_key()
        if key in self.__class__.CACHE:
            return self.__class__.CACHE[key]
        #
        list_ = []
        configure_file_path = self._get_configure_file()
        if configure_file_path:
            bsc_log.Log.trace_method_result(
                'app resolved',
                'app="{project}.{application}"'.format(
                    **dict(project=self._project, application=self._application)
                )
            )
            configure = ctt_core.Content(value=configure_file_path)
            keys = configure.get_all_leaf_keys()
            for i_key in keys:
                i_args = configure.get(i_key)
                list_.extend(i_args)
        if list_:
            self.__class__.CACHE[key] = list_
            #
            _ = copy.copy(list_)
            if isinstance(packages_extend, (set, tuple, list)):
                _.extend(list(packages_extend))
            return _
        return []

    def get_command(self, args_execute=None, args_extend=None, packages_extend=None):
        args = self.get_args(packages_extend)
        if args:
            if isinstance(args_execute, (set, tuple, list)):
                args.extend(args_execute)
            if isinstance(args_extend, (set, tuple, list)):
                args.extend(args_extend)
            return ' '.join([self.BIN]+list(args))

    def _test_(self):
        pass


class AbsRsvAppNew(AbsRsvAppDef):
    BIN_SOURCE = '/job/PLE/support/wrappers/paper-bin'
    BIN = '/job/PLE/support/wrappers/paper-bin'

    def __init__(self, *args, **kwargs):
        super(AbsRsvAppNew, self).__init__(*args, **kwargs)
        self._bin_source = bsc_storage.PkgContextNew.get_bin_source()

    def get_args(self, packages_extend=None):
        if self._application == self.Applications.Lynxi:
            return ['lxdcc', 'lxdcc_lib', 'lxdcc_gui', 'lxdcc_rsc']
        #
        key = self.get_key()
        if key in self.__class__.CACHE:
            return self.__class__.CACHE[key]
        #
        list_ = []
        configure_file_path = self._get_configure_file()
        if configure_file_path:
            bsc_log.Log.trace_method_result(
                'app resolved',
                'app="{project}.{application}"'.format(
                    **dict(project=self._project, application=self._application)
                )
            )
            data = bsc_storage.StgFileOpt(configure_file_path).set_read()
            key = self._application
            if data:
                if key in data:
                    app_data = data[key]
                    p_args = app_data['pipeline']
                    p_c = bsc_storage.PkgContextNew(
                        p_args
                    )
                    args = p_c.get_args(packages_extend)
                    list_.extend(args)
        if list_:
            self.__class__.CACHE[key] = list_
            #
            _ = copy.copy(list_)
            return _
        return []

    def get_command(self, args_execute=None, args_extend=None, packages_extend=None):
        if isinstance(args_execute, (set, tuple, list)):
            args_execute = bsc_storage.PkgContextNew.convert_args_execute(args_execute)
        #
        args = self.get_args(packages_extend)
        if args:
            if isinstance(args_execute, (set, tuple, list)):
                args.extend(args_execute)
            if isinstance(args_extend, (set, tuple, list)):
                args.extend(args_extend)
            return ' '.join([self._bin_source]+list(args))

    def _test_(self):
        pass
