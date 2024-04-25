# coding:utf-8
import re

import fnmatch

import six

import os

import scandir


class ScanGlob(object):
    MAGIC_CHECK = re.compile('[*?[]')

    @classmethod
    def auto_unicode(cls, path):
        if not isinstance(path, six.text_type):
            return path.decode('utf-8')
        return path

    @classmethod
    def auto_string(cls, path):
        if isinstance(path, six.text_type):
            return path.encode('utf-8')
        return path

    @classmethod
    def has_magic(cls, s):
        return cls.MAGIC_CHECK.search(s) is not None

    @classmethod
    def scan_fnc(cls, path):
        list_ = []
        path = cls.auto_unicode(path)
        for i in scandir.scandir(path):
            i_path = i.path.replace('\\', '/')
            list_.append(i_path)
        return list_

    @classmethod
    def glob(cls, regex):
        def _rcs_fnc(path_, depth_, is_root=False):
            path_ = cls.auto_unicode(path_)
            _depth = depth_+1
            if _depth <= depth_maximum:
                _filter_name = cls.auto_unicode(filter_names[_depth])
                if is_root is True:
                    _filter_path = six.u('{}{}').format(
                        path_, _filter_name
                    )
                else:
                    _filter_path = six.u('{}/{}').format(
                        path_, _filter_name
                    )

                if not cls.has_magic(_filter_path):
                    if os.path.exists(_filter_path):
                        _match_paths = [_filter_path]
                    else:
                        _match_paths = []
                else:
                    if path_ in cache_dict:
                        _paths = cache_dict[path_]
                    else:
                        _paths = cls.scan_fnc(path_)
                        cache_dict[path_] = _paths

                    _match_paths = fnmatch.filter(
                        _paths, _filter_path
                    )

                if _match_paths:
                    for _i_path in _match_paths:
                        if _depth == depth_maximum:
                            list_.append(_i_path)
                        _rcs_fnc(_i_path, _depth)

        cache_dict = {}
        list_ = []
        #
        regex = cls.auto_unicode(regex)
        #
        filter_names = regex.split('/')
        depth_maximum = len(filter_names)-1

        root = filter_names[0]+'/'
        _rcs_fnc(root, 0, is_root=True)
        return list_
