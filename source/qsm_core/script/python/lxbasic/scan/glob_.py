# coding:utf-8
import re

import fnmatch

import sys

import time

import six

import os

import scandir

import platform


class Filter:
    FILTER_CACHE = dict()
    FILTER_CACHE_MAXIMUM = 1000

    @classmethod
    def is_match(cls, text, p):
        try:
            re_pat = cls.FILTER_CACHE[p]
        except KeyError:
            res = fnmatch.translate(p)
            if len(cls.FILTER_CACHE) >= cls.FILTER_CACHE_MAXIMUM:
                cls.FILTER_CACHE.clear()
            cls.FILTER_CACHE[p] = re_pat = re.compile(res, re.IGNORECASE)
        return bool(re_pat.match(text))


class ScanGlob(object):
    MAGIC_CHECK = re.compile('[*?[]')

    @staticmethod
    def ensure_unicode(s):
        if isinstance(s, six.text_type):
            return s
        elif isinstance(s, bytes):
            return s.decode('utf-8')
        else:
            return s

    @classmethod
    def has_magic_fnc(cls, s):
        return cls.MAGIC_CHECK.search(s) is not None

    @classmethod
    def scan_fnc(cls, path):
        if cls.check_dir_fnc(path):
            list_ = []
            path = cls.ensure_unicode(path)
            for i in scandir.scandir(path):
                i_path = i.path.replace('\\', '/')
                list_.append(i_path)
            return list_
        return []

    @classmethod
    def check_exists_fnc(cls, path):
        return os.access(path, os.F_OK)

    @classmethod
    def check_dir_exists_fnc(cls, path):
        return os.access(path, os.F_OK) and os.path.isdir(path)

    @classmethod
    def check_dir_fnc(cls, path):
        return os.path.isdir(path)

    @classmethod
    def glob(cls, path_regex):
        def _rcs_fnc(path_, depth_, is_root_=False, flag_=False):
            path_ = cls.ensure_unicode(path_)
            _depth = depth_+1
            if _depth <= depth_maximum:
                _filter_name = cls.ensure_unicode(filter_names[_depth])
                if is_root_ is True:
                    if flag_ is True:
                        _filter_path = six.u('{}/{}').format(
                            path_, _filter_name
                        )
                    else:
                        _filter_path = six.u('{}{}').format(
                            path_, _filter_name
                        )
                else:
                    _filter_path = six.u('{}/{}').format(
                        path_, _filter_name
                    )

                if not cls.has_magic_fnc(_filter_path):
                    if cls.check_exists_fnc(_filter_path):
                        _paths_matched = [_filter_path]
                    else:
                        _paths_matched = []
                else:
                    _paths = cls.scan_fnc(path_)

                    _paths_matched = fnmatch.filter(
                        _paths, _filter_path
                    )

                if _paths_matched:
                    for _i_path in _paths_matched:
                        if _depth == depth_maximum:
                            list_.append(_i_path)
                        _rcs_fnc(_i_path, _depth)

        list_ = []

        path_regex = cls.ensure_unicode(path_regex)

        filter_names = path_regex.split('/')
        depth_maximum = len(filter_names)-1
        if platform.system() == 'Linux':
            # etc. /production
            root = '/'+filter_names[1]
            start_index = 1
            flag = True
        elif platform.system() == 'Windows':
            # etc. //shared
            if path_regex.startswith('//'):
                root = '//' + filter_names[2]
                start_index = 2
                flag = True
            # etc. Z:/
            else:
                root = filter_names[0]+'/'
                start_index = 0
                flag = False
        else:
            raise SystemError()

        if cls.check_dir_exists_fnc(root) is True:
            _rcs_fnc(root, start_index, is_root_=True, flag_=flag)
        return list_

    @classmethod
    def generate_glob_executor(cls, path_regex, fnc):
        def rcs_fnc_(path_, depth_, is_root_=False, flag_=False):
            path_ = cls.ensure_unicode(path_)
            _depth = depth_+1
            if _depth <= depth_maximum:
                _filter_name = cls.ensure_unicode(filter_names[_depth])
                if is_root_ is True:
                    if flag_ is True:
                        _filter_path = six.u('{}/{}').format(
                            path_, _filter_name
                        )
                    else:
                        _filter_path = six.u('{}{}').format(
                            path_, _filter_name
                        )
                else:
                    _filter_path = six.u('{}/{}').format(
                        path_, _filter_name
                    )

                if not cls.has_magic_fnc(_filter_path):
                    if cls.check_exists_fnc(_filter_path):
                        _paths_matched = [_filter_path]
                    else:
                        _paths_matched = []
                else:
                    _paths = cls.scan_fnc(path_)

                    _paths_matched = fnmatch.filter(
                        _paths, _filter_path
                    )

                if _paths_matched:
                    for _i_path in _paths_matched:
                        if _depth == depth_maximum:
                            fnc(_i_path)

                        executor.submit(rcs_fnc_, _i_path, _depth)

        from concurrent.futures import ThreadPoolExecutor

        executor = ThreadPoolExecutor(max_workers=5)

        path_regex = cls.ensure_unicode(path_regex)

        filter_names = path_regex.split('/')
        depth_maximum = len(filter_names)-1
        if platform.system() == 'Linux':
            root = '/'+filter_names[1]
            start_index = 1
            flag = True
        elif platform.system() == 'Windows':
            if path_regex.startswith('//'):
                root = '//' + filter_names[2]
                start_index = 2
                flag = True
            else:
                root = filter_names[0]+'/'
                start_index = 0
                flag = False
        else:
            raise SystemError()

        rcs_fnc_(root, start_index, is_root_=True, flag_=flag)

        executor.submit(rcs_fnc_, root, start_index, is_root_=True, flag_=flag)
        return executor

    @classmethod
    def name_match_fnc(cls, path, name_regex):
        name = os.path.basename(path)
        return Filter.is_match(name, name_regex)

    @classmethod
    def filter_all_files_from(cls, location, name_regex):
        def rcs_fnc_(path_):
            _paths = cls.scan_fnc(path_)
            for _i_path in _paths:
                if cls.check_dir_fnc(_i_path):
                    rcs_fnc_(_i_path)
                else:
                    if cls.name_match_fnc(_i_path, name_regex):
                        list_.append(_i_path)

        list_ = []

        if cls.check_dir_exists_fnc(location) is True:
            rcs_fnc_(location)

        return list_
    
    @classmethod
    def glob_all_files(cls, path_regex):
        path_regex = cls.ensure_unicode(path_regex)

        if '//' in path_regex:
            _s = path_regex.split('//')
            if len(_s) > 2:
                raise RuntimeError(u'more then 2 "//" in "{}", please check item'.format(path_regex))

            list_ = []

            paths = cls.glob(_s[0])

            for i_path in paths:
                if cls.check_dir_fnc(i_path):
                    i_results = cls.filter_all_files_from(i_path, _s[1])
                    list_.extend(i_results)

            return list_
        return cls.glob(path_regex)

