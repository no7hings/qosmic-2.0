# coding:utf-8
import re

import fnmatch

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
    def _has_magic_fnc(cls, s):
        return cls.MAGIC_CHECK.search(s) is not None

    @classmethod
    def _scan_fnc(cls, path):
        if cls._check_dir_fnc(path):
            list_ = []
            path = cls.ensure_unicode(path)
            for i in scandir.scandir(path):
                i_path = i.path.replace('\\', '/')
                list_.append(i_path)
            return list_
        return []

    @classmethod
    def _exists_fnc(cls, path):
        return os.access(path, os.F_OK)

    @classmethod
    def _directory_exists_fnc(cls, path):
        return os.access(path, os.F_OK) and os.path.isdir(path)

    @classmethod
    def _file_exists_fnc(cls, path):
        return os.access(path, os.F_OK) and os.path.isfile(path)

    @classmethod
    def _check_dir_fnc(cls, path):
        return os.path.isdir(path)

    @classmethod
    def _match_name_fnc(cls, path, name_regex):
        name = os.path.basename(path)
        return Filter.is_match(name, name_regex)

    @classmethod
    def _filter_files_fnc(cls, location, name_regex):
        def rcs_fnc_(path_):
            _next_paths = cls._scan_fnc(path_)
            for _i_path in _next_paths:
                if cls._check_dir_fnc(_i_path):
                    rcs_fnc_(_i_path)
                else:
                    if cls._match_name_fnc(_i_path, name_regex):
                        list_.append(_i_path)

        list_ = []

        if cls._directory_exists_fnc(location) is True:
            rcs_fnc_(location)

        return list_

    @classmethod
    def _get_glob_args(cls, path_regex):
        path_regex = cls.ensure_unicode(path_regex)

        filter_names = path_regex.split('/')
        depth_maximum = len(filter_names)-1
        if platform.system() == 'Linux':
            location = '/'+filter_names[1]
            start_index = 1
            flag = True
        elif platform.system() == 'Windows':
            if path_regex.startswith('//'):
                location = '//'+filter_names[2]
                start_index = 2
                flag = True
            else:
                location = filter_names[0]+'/'
                start_index = 0
                flag = False
        else:
            raise SystemError()

        return path_regex, location, filter_names, start_index, depth_maximum, flag

    @classmethod
    def glob(cls, path_regex):
        def _rcs_fnc(path_, depth_, is_root_=False, is_drive_letter_=False):
            path_ = cls.ensure_unicode(path_)
            _depth = depth_+1
            if _depth <= depth_maximum:
                _filter_name = cls.ensure_unicode(filter_names[_depth])
                if is_root_ is True:
                    if is_drive_letter_ is True:
                        _filter_path = u'{}/{}'.format(
                            path_, _filter_name
                        )
                    else:
                        _filter_path = u'{}{}'.format(
                            path_, _filter_name
                        )
                else:
                    _filter_path = u'{}/{}'.format(
                        path_, _filter_name
                    )

                if not cls._has_magic_fnc(_filter_path):
                    if cls._exists_fnc(_filter_path):
                        _paths_matched = [_filter_path]
                    else:
                        _paths_matched = []
                else:
                    _next_paths = cls._scan_fnc(path_)

                    _paths_matched = fnmatch.filter(
                        _next_paths, _filter_path
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
            location = '/'+filter_names[1]
            start_index = 1
            flag = True
        elif platform.system() == 'Windows':
            # etc. //shared
            if path_regex.startswith('//'):
                location = '//' + filter_names[2]
                start_index = 2
                flag = True
            # etc. Z:/
            else:
                location = filter_names[0]+'/'
                start_index = 0
                flag = False
        else:
            raise SystemError()

        if cls._directory_exists_fnc(location) is True:
            _rcs_fnc(location, start_index, is_root_=True, is_drive_letter_=flag)
        return list_
    
    @classmethod
    def glob_files(cls, file_regex):
        file_regex = cls.ensure_unicode(file_regex)

        if '//' in file_regex:
            _s = file_regex.split('//')
            if len(_s) > 2:
                raise RuntimeError(u'more then 2 "//" in "{}", please check item'.format(file_regex))

            list_ = []

            locations = cls.glob(_s[0])

            for i_path in locations:
                if cls._check_dir_fnc(i_path):
                    i_results = cls._filter_files_fnc(i_path, _s[1])
                    list_.extend(i_results)

            return list_
        return cls.glob(file_regex)

    @classmethod
    def concurrent_glob(cls, path_regex, result_fnc, finish_fnc=None):
        def rcs_fnc_(path_, depth_, is_root_=False, is_drive_letter_=False):
            path_ = cls.ensure_unicode(path_)

            _depth = depth_+1

            # scan to depth maximum
            if _depth <= depth_maximum:
                _filter_name = cls.ensure_unicode(filter_names[_depth])
                if is_root_ is True:
                    if is_drive_letter_ is True:
                        _filter_path = u'{}/{}'.format(
                            path_, _filter_name
                        )
                    else:
                        _filter_path = u'{}{}'.format(
                            path_, _filter_name
                        )
                else:
                    _filter_path = u'{}/{}'.format(
                        path_, _filter_name
                    )

                # when is not magic, use current exists path
                if not cls._has_magic_fnc(_filter_path):
                    if cls._exists_fnc(_filter_path):
                        _paths_matched = [_filter_path]
                    else:
                        _paths_matched = []
                else:
                    _next_paths = cls._scan_fnc(path_)

                    _paths_matched = fnmatch.filter(_next_paths, _filter_path)

                if _paths_matched:
                    _index_maximum = len(_paths_matched)-1

                    for _i_idx, _i_path in enumerate(_paths_matched):
                        # when is match maximum depth, finish recursion
                        if _depth == depth_maximum:
                            result_fnc(_i_path)
                        else:
                            task_dict[_i_path] = False
                            executor.submit(
                                rcs_fnc_,
                                path_=_i_path, depth_=_depth
                            )

            task_dict[path_] = True

            # check finish
            if finish_fnc is not None:
                is_finished = sum(task_dict.values()) == len(task_dict.values())
                if is_finished is True:
                    finish_fnc()

        from concurrent.futures import ThreadPoolExecutor

        executor = ThreadPoolExecutor(max_workers=32)

        task_dict = {}

        path_regex, location, filter_names, start_index, depth_maximum, flag = cls._get_glob_args(path_regex)

        if cls._directory_exists_fnc(location) is True:
            task_dict[location] = False
            executor.submit(
                rcs_fnc_,
                path_=location,
                depth_=start_index,
                is_root_=True, is_drive_letter_=flag
            )
        return executor

    @classmethod
    def _concurrent_filter_files_fnc(cls, executor, location, name_regex, result_fnc, finish_fnc=None):
        def rcs_fnc_(path_):
            _next_paths = cls._scan_fnc(path_)

            for _i_path in _next_paths:
                # do not check exists
                if cls._check_dir_fnc(_i_path):
                    task_dict[_i_path] = False

                    executor.submit(rcs_fnc_, _i_path)
                # when is file then finish
                else:
                    if cls._match_name_fnc(_i_path, name_regex):
                        result_fnc(_i_path)

            task_dict[path_] = True

            # check finish
            if finish_fnc is not None:
                is_finished = sum(task_dict.values()) == len(task_dict.values())
                if is_finished is True:
                    finish_fnc()

        task_dict = {}

        if cls._directory_exists_fnc(location) is True:
            task_dict[location] = False
            executor.submit(rcs_fnc_, location)

    @classmethod
    def concurrent_glob_file(cls, file_regex, result_fnc, finish_fnc=None):
        # ensure path is unicode
        file_regex = cls.ensure_unicode(file_regex)

        if '//' in file_regex:
            _s = file_regex.split('//')
            if len(_s) > 2:
                raise RuntimeError(u'more then 2 "//" in "{}", please check it.'.format(file_regex))

            locations = cls.glob(_s[0])

            from concurrent.futures import ThreadPoolExecutor

            executor = ThreadPoolExecutor(max_workers=32)

            for i_path in locations:
                if cls._check_dir_fnc(i_path):
                    cls._concurrent_filter_files_fnc(executor, i_path, _s[1], result_fnc, finish_fnc)
            return executor
        return cls.concurrent_glob(file_regex, result_fnc, finish_fnc)

