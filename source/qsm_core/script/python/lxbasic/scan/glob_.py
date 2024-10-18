# coding:utf-8
import re

import fnmatch

import sys

import time

import six

import os

import scandir

import platform


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
        list_ = []
        if cls.check_dir_exists_fnc(path):
            path = cls.ensure_unicode(path)
            for i in scandir.scandir(path):
                i_path = i.path.replace('\\', '/')
                list_.append(i_path)
        return list_

    @classmethod
    def check_exists_fnc(cls, path):
        return os.access(path, os.F_OK)

    @classmethod
    def check_dir_exists_fnc(cls, path):
        return os.access(path, os.F_OK) and os.path.isdir(path)

    @classmethod
    def glob(cls, regex):
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
                    if path_ in cache_dict:
                        _paths = cache_dict[path_]
                    else:
                        _paths = cls.scan_fnc(path_)
                        cache_dict[path_] = _paths

                    _paths_matched = fnmatch.filter(
                        _paths, _filter_path
                    )

                if _paths_matched:
                    for _i_path in _paths_matched:
                        if _depth == depth_maximum:
                            list_.append(_i_path)
                        _rcs_fnc(_i_path, _depth)

        cache_dict = {}
        list_ = []

        regex = cls.ensure_unicode(regex)

        filter_names = regex.split('/')
        depth_maximum = len(filter_names)-1
        if platform.system() == 'Linux':
            root = '/'+filter_names[1]
            start_depth = 1
            flag = True
        elif platform.system() == 'Windows':
            if regex.startswith('//'):
                root = '//' + filter_names[2]
                start_depth = 2
                flag = True
            else:
                root = filter_names[0]+'/'
                start_depth = 0
                flag = False
        else:
            raise SystemError()

        start_time = time.time()

        _rcs_fnc(root, start_depth, is_root_=True, flag_=flag)

        finish_time = time.time()
        sys.stdout.write(
            u'scan glob: "{}", {} items is found, cost time {}s\n'.format(
                regex,
                len(list_),
                round(finish_time-start_time, 4)
            )
        )
        return list_

    @classmethod
    def concurrent_glob(cls, regex):
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
                    if path_ in cache_dict:
                        _paths = cache_dict[path_]
                    else:
                        _paths = cls.scan_fnc(path_)
                        cache_dict[path_] = _paths

                    _paths_matched = fnmatch.filter(
                        _paths, _filter_path
                    )

                if _paths_matched:
                    for _i_path in _paths_matched:
                        if _depth == depth_maximum:
                            list_.append(_i_path)

                        # _rcs_fnc(_i_path, _depth)
                        _future = executor.submit(_rcs_fnc, _i_path, _depth)
                return True
            return False

        from concurrent.futures import ThreadPoolExecutor

        import threading

        lock = threading.Lock()

        executor = ThreadPoolExecutor(max_workers=5)

        cache_dict = {}
        list_ = []

        regex = cls.ensure_unicode(regex)

        filter_names = regex.split('/')
        depth_maximum = len(filter_names)-1
        if platform.system() == 'Linux':
            root = '/'+filter_names[1]
            start_depth = 1
            flag = True
        elif platform.system() == 'Windows':
            if regex.startswith('//'):
                root = '//' + filter_names[2]
                start_depth = 2
                flag = True
            else:
                root = filter_names[0]+'/'
                start_depth = 0
                flag = False
        else:
            raise SystemError()

        start_time = time.time()

        _rcs_fnc(root, start_depth, is_root_=True, flag_=flag)

        future = executor.submit(_rcs_fnc, root, start_depth, is_root_=True, flag_=flag)

        if future.result():
            finish_time = time.time()
            sys.stdout.write(u'scan glob: "{}", cost time {}s\n'.format(regex, round(finish_time-start_time, 4)))
            return list_
        return []
