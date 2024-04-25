# coding:utf-8
import six

import os

import scandir


class ScanBase(object):
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
    def scan_fnc(cls, path):
        return scandir.scandir(cls.auto_unicode(path))

    @classmethod
    def get_directory_paths(cls, location):
        location = cls.auto_unicode(location)
        list_ = []
        # make sure is a directory
        if os.path.isdir(location):
            for i in cls.scan_fnc(location):
                if i.is_dir():
                    i_path = i.path.replace('\\', '/')
                    list_.append(
                        i_path
                    )
        return list_

    @classmethod
    def get_all_directory_paths(cls, location):
        def rcs_fnc_(path_):
            path_ = cls.auto_unicode(path_)
            for _i in cls.scan_fnc(path_):
                if _i.is_dir():
                    _i_path = _i.path.replace('\\', '/')
                    list_.append(_i_path)
                    rcs_fnc_(_i_path)

        location = cls.auto_unicode(location)

        list_ = []
        if os.path.isdir(location):
            rcs_fnc_(location)
        if list_:
            list_.sort()
        return list_

    @classmethod
    def get_file_paths(cls, location, ext_includes=None):
        location = cls.auto_unicode(location)
        list_ = []
        # make sure is a directory
        if os.path.isdir(location):
            for i in cls.scan_fnc(location):
                if i.is_file():
                    i_path = i.path.replace('\\', '/')
                    if isinstance(ext_includes, (tuple, list)):
                        i_base, i_ext = os.path.splitext(i_path)
                        if i_ext not in ext_includes:
                            continue
                    #
                    list_.append(i_path)
        if list_:
            list_.sort()
        return list_

    @classmethod
    def get_all_file_paths(cls, location, ext_includes=None):
        def rcs_fnc_(path_):
            path_ = cls.auto_unicode(path_)
            for _i in scandir.scandir(path_):
                _i_path = _i.path.replace('\\', '/')
                if _i.is_file():
                    if isinstance(ext_includes, (tuple, list)):
                        _i_base, _i_ext = os.path.splitext(_i_path)
                        if _i_ext not in ext_includes:
                            continue
                    #
                    list_.append(_i_path)
                elif _i.is_dir():
                    rcs_fnc_(_i_path)

        location = cls.auto_unicode(location)

        list_ = []
        if os.path.isdir(location):
            rcs_fnc_(location)
        if list_:
            list_.sort()
        return list_

    @classmethod
    def get_all_paths(cls, location):
        def rcs_fnc_(path_):
            path_ = cls.auto_unicode(path_)
            for _i in cls.scan_fnc(path_):
                _i_path = _i.path.replace('\\', '/')
                list_.append(_i_path)
                if _i.is_dir():
                    list_.append(_i_path)
                    rcs_fnc_(_i_path)

        location = cls.auto_unicode(location)

        list_ = []
        if os.path.isdir(location):
            rcs_fnc_(location)
        if list_:
            list_.sort()
        return list_
