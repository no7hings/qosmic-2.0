# coding:utf-8
import fnmatch

import lxbasic.log as bsc_log

from lxbasic.core import base as bsc_cor_base

from lxbasic.core import raw as bsc_cor_raw

from lxbasic.core import pattern as bsc_cor_pattern

from lxbasic.core import process as bsc_cor_process

from . import base as bsc_stg_base


class PkgContextNew(object):
    KEY = 'package context'

    BIN_SOURCE = dict(
        windows='X:/PLE/support/wrappers/windows/paper',
        linux='/job/PLE/support/wrappers/paper-bin'
    )

    USER_ROOT_PATTERNS = dict(
        windows=['{home}/packages'],
        linux=['{home}/packages']
    )
    PRE_RELEASE_PATTERNS = dict(
        windows=['X:/PLE/workspace/pre_release/packages'],
        linux=['/job/PLE/workspace/pre_release/packages']
    )
    RELEASE_PATTERNS = dict(
        windows=['X:/PLE/bundle/internal', 'X:/PLE/bundle/thirdparty'],
        linux=['/job/PLE/bundle/internal', '/job/PLE/bundle/thirdparty']
    )
    FILE_PATTERNS = dict(
        windows=['{root}/{package_name}/{version}/paper_configure_bundle.py'],
        linux=['{root}/{package_name}/{version}/paper_configure_bundle.py']
    )

    @classmethod
    def get_bin_source(cls):
        return cls.BIN_SOURCE[bsc_cor_base.SysPlatformMtd.get_current()]

    def __init__(self, *args):
        self._platform = bsc_cor_base.SysPlatformMtd.get_current()
        self._bin_source = self.get_bin_source()
        if args:
            self._args = args[0]
        else:
            self._args = None

        self._variants = dict(
            home=bsc_cor_base.SysBaseMtd.get_home_directory(),
            platfrom=self._platform,
        )

        self._exclude_packages = []

    def get_user_package_roots(self):
        list_ = []
        for i_p in self.USER_ROOT_PATTERNS.get(self._platform) or []:
            i_p_opt = bsc_cor_pattern.PtnParseOpt(
                i_p
            )
            i_p_opt.update_variants(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_pre_release_package_roots(self):
        list_ = []
        for i_p in self.PRE_RELEASE_PATTERNS.get(self._platform) or []:
            i_p_opt = bsc_cor_pattern.PtnParseOpt(
                i_p
            )
            i_p_opt.update_variants(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_release_package_roots(self):
        list_ = []
        for i_p in self.RELEASE_PATTERNS.get(self._platform) or []:
            i_p_opt = bsc_cor_pattern.PtnParseOpt(
                i_p
            )
            i_p_opt.update_variants(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_resolved_packages_data(self):
        if self._args:
            results = bsc_cor_process.PrcBaseMtd.execute_as_block(
                '{} {} -v'.format(self._bin_source, self._args)
            )
            if not results:
                return self._args.split(' ')

            package_start_index = None
            package_end_index = None
            index_maximum = len(results)-1
            index = 0
            while True:
                index += 1
                result = results[index]
                if result == 'It simplifies to:':
                    package_start_index = index+1
                elif result == 'Which resolves to:':
                    package_end_index = index-1
                if index >= index_maximum:
                    break
            #
            if package_start_index is not None and package_end_index is not None:
                args = map(lambda x: x.strip(), results[package_start_index:package_end_index])
                return args
        return []

    def _get_package_file_patterns(self):
        return self.FILE_PATTERNS.get(self._platform) or []

    @classmethod
    def _get_virtual_version(cls, version):
        """
        etc. convert master-1 to 0.0.1
        :param version:
        :return:
        """
        if fnmatch.filter([version], 'master-[0-9]*'):
            _ = version.split('-')
            return '0.{}'.format(float(_[-1]))
        return version

    def _get_replace_package(self, package, use_beta=False):
        if '@' not in package:
            return None
        package_name, package_version = package.split('@')
        package_virtual_version = self._get_virtual_version(package_version)
        package_data = {}
        user_package_roots = self.get_user_package_roots()
        pre_release_package_roots = self.get_pre_release_package_roots()
        package_roots = user_package_roots
        if use_beta is True:
            package_roots += pre_release_package_roots
        package_file_patterns = self._get_package_file_patterns()
        for i_index, i_package_root in enumerate(package_roots):
            if bsc_stg_base.StgPathMtd.get_is_exists(i_package_root):
                i_variants = dict(
                    root=i_package_root,
                    package_name=package_name
                )
                for j_p in package_file_patterns:
                    j_p_opt = bsc_cor_pattern.PtnParseOpt(j_p)
                    j_p_opt.update_variants(**i_variants)
                    j_results = j_p_opt.get_exists_results()
                    if j_results:
                        for k_package_file in j_results:
                            k_package_directory = bsc_stg_base.StgFileMtd.get_directory(k_package_file)
                            k_package_variants = j_p_opt.get_variants(k_package_file)
                            if 'version' not in k_package_variants:
                                continue
                            k_package_version = k_package_variants['version']
                            k_package_virtual_version = self._get_virtual_version(k_package_version)
                            k_key = '{}.{}'.format(k_package_virtual_version, i_index)
                            k_package = '{}@{}'.format(package_name, k_package_directory)
                            package_data[k_key] = k_package
        #
        if package_data:
            package_data[package_virtual_version] = package
            keys = package_data.keys()
            keys = bsc_cor_raw.RawTextsMtd.sort_by_number(keys)
            package_latest = package_data[keys[-1]]
            return package_latest

    def _completed_package_to(self, package, use_beta=False):
        if '@' not in package:
            package_name = package
            package_data = {}
            user_package_roots = self.get_user_package_roots()
            pre_release_package_roots = self.get_pre_release_package_roots()
            package_roots = user_package_roots
            if use_beta is True:
                package_roots += pre_release_package_roots
            #
            release_package_roots = self.get_release_package_roots()
            package_roots += release_package_roots
            package_file_patterns = self._get_package_file_patterns()
            #
            for i_index, i_package_root in enumerate(package_roots):
                if bsc_stg_base.StgPathMtd.get_is_exists(i_package_root):
                    i_variants = dict(
                        root=i_package_root,
                        package_name=package_name
                    )
                    for j_p in package_file_patterns:
                        j_p_opt = bsc_cor_pattern.PtnParseOpt(j_p)
                        j_p_opt.update_variants(**i_variants)
                        j_results = j_p_opt.get_exists_results()
                        if j_results:
                            for k_package_file in j_results:
                                k_package_directory = bsc_stg_base.StgFileMtd.get_directory(k_package_file)
                                k_package_variants = j_p_opt.get_variants(k_package_file)
                                if 'version' not in k_package_variants:
                                    continue
                                k_package_version = k_package_variants['version']
                                k_package_virtual_version = self._get_virtual_version(k_package_version)
                                k_key = '{}.{}'.format(k_package_virtual_version, i_index)
                                if i_package_root in release_package_roots:
                                    k_package = '{}@{}'.format(package_name, k_package_version)
                                else:
                                    k_package = '{}@{}'.format(package_name, k_package_directory)
                                package_data[k_key] = k_package
            #
            if package_data:
                keys = package_data.keys()
                keys = bsc_cor_raw.RawTextsMtd.sort_by_number(keys)
                package_latest = package_data[keys[-1]]
                return package_latest
        return package

    def _completed_packages_to(self, packages, use_beta=False):
        list_ = []
        for i_p in packages:
            i_package = self._completed_package_to(i_p, use_beta=use_beta)
            if i_package is not None:
                bsc_log.Log.trace_method_result(
                    self.KEY,
                    'resolve package: "{}"'.format(i_package)
                )
                list_.append(i_package)
            else:
                bsc_log.Log.trace_method_warning(
                    self.KEY,
                    'package: "{}" is invalid'
                )
        return list_

    def _get_packages(self, packages_extend=None, use_beta=False):
        list_ = []
        # package from configure
        resolved_packages = self.get_resolved_packages_data()
        #
        for i_p in resolved_packages:
            i_replace_package = self._get_replace_package(i_p, use_beta=use_beta)
            if i_replace_package is not None:
                bsc_log.Log.trace_method_result(
                    self.KEY,
                    'replace package: "{}"'.format(i_replace_package)
                )
                list_.append(i_replace_package)
            else:
                list_.append(i_p)
        # package from extend
        list_.extend(
            self._completed_packages_to(packages_extend or [])
        )
        return list_

    def get_args(self, packages_extend=None, use_beta=False):
        return self._get_packages(packages_extend, use_beta)

    @classmethod
    def convert_args_execute(cls, args_execute=None):
        if isinstance(args_execute, (set, tuple, list)):
            # replace first argument to "--join-cmd", etc. "-- maya", "-c maya" to "--join-cmd maya"
            if bsc_cor_base.SysBaseMtd.get_is_linux():
                j_key = '--join-cmd'
            elif bsc_cor_base.SysBaseMtd.get_is_windows():
                j_key = '&&'
            else:
                raise SystemError()

            args_execute = [
                j_key if x_seq == 0 and y_seq == 0 and y in {'--', '-c'} else y
                for x_seq, x in enumerate(args_execute)
                for y_seq, y in enumerate(x.split(' '))
            ]
        return args_execute

    def get_command(self, args_execute=None, packages_extend=None, use_beta=False):
        if isinstance(args_execute, (set, tuple, list)):
            args_execute = self.convert_args_execute(args_execute)
        #
        args = self.get_args(packages_extend, use_beta)
        if args:
            if isinstance(args_execute, (set, tuple, list)):
                args.extend(args_execute)
            return ' '.join([self._bin_source]+list(args))
