# coding:utf-8
import re

import fnmatch

import lxbasic.core as bsc_core


class Selection(object):
    MAGIC_CHECK = re.compile('[*?[]')

    PATHSEP = '/'

    FILTER_CACHE = bsc_core.LRUCache(1024)

    @classmethod
    def filter(cls, texts, regex):
        list_ = []

        re_pat = cls.FILTER_CACHE[regex]
        if re_pat is None:
            cls.FILTER_CACHE[regex] = re_pat = re.compile(fnmatch.translate(regex), re.IGNORECASE)

        match = re_pat.match
        for i in texts:
            if match(i):
                list_.append(i)
        return list_

    @classmethod
    def match(cls, s, regex):
        re_pat = cls.FILTER_CACHE[regex]
        if re_pat is None:
            cls.FILTER_CACHE[regex] = re_pat = re.compile(fnmatch.translate(regex), re.IGNORECASE)
        return bool(re_pat.match(s))

    @classmethod
    def exist(cls, paths, path):
        return path in set(paths)

    @classmethod
    def has_magic(cls, s):
        return cls.MAGIC_CHECK.search(s) is not None

    @classmethod
    def next_fnc(cls, paths, path):
        list_ = []
        if path == '/':
            ptn = r'/[^/]*'
        else:
            ptn = r'{}/[^/]*'.format(path)

        for i in paths:
            if i == '/':
                continue

            _ = re.match(ptn, i)
            if _ is not None:
                if _.group() == i:
                    list_.append(i)
        return list_

    @classmethod
    def glob(cls, paths, pattern):
        def _rcs_fnc(location_, depth_):
            _depth = depth_+1
            if _depth <= depth_maximum:
                _name = names[_depth]
                _pattern = '{}/{}'.format(
                    location_, _name
                )
                if cls.has_magic(_pattern):
                    _matches = cls.filter(cls.next_fnc(paths, location_), _pattern)
                else:
                    if cls.exist(paths, _pattern):
                        _matches = [_pattern]
                    else:
                        _matches = []

                if _matches:
                    for _i_path in _matches:
                        if _depth == depth_maximum:
                            list_.append(_i_path)
                        _rcs_fnc(_i_path, _depth)

        if cls.exist(paths, pattern):
            return [pattern]

        list_ = []

        names = pattern.split('/')
        depth_maximum = len(names)-1
        root = '/'+names[1]
        start_index = 1

        _rcs_fnc(root, start_index)
        return list_

    @classmethod
    def fetchall(cls, paths, pattern):
        if '//' in pattern:
            _s = pattern.split('//')
            if len(_s) > 2:
                raise RuntimeError()

            s_0, s_1 = _s

            # ignore etc. '//abc*' or '/root//'
            if not s_0:
                return []

            if not s_1:
                return []

            list_ = []
            results = cls.glob(paths, s_0)
            for i in results:
                i_paths = cls.filter(paths, '{}/*'.format(i))
                for j in i_paths:
                    if cls.match(j.split('/')[-1], s_1):
                        list_.append(j)
            return list_
        return cls.glob(paths, pattern)


class PathOpt(str):
    PATHSEP = '/'

    @classmethod
    def _to_args(cls, path, pathsep):
        if path == pathsep:
            return [pathsep, ]
        return path.split(pathsep)

    def __init__(self, path):
        super(PathOpt, self).__init__(path)
        self._args = self._to_args(path, self.PATHSEP)

    def get_parent(self):
        if len(self._args) == 1:
            return None
        elif len(self._args) == 2:
            return self.__class__(self.PATHSEP)
        return self.__class__(self.PATHSEP.join(self._args[:-1]))

    def get_ancestors(self):
        return self.to_components()[1:]

    def to_components(self):
        def _rcs_fnc(path_):
            _parent = path_.get_parent()
            if _parent:
                list_.append(_parent)
                _rcs_fnc(_parent)

        list_ = [self]
        _rcs_fnc(self)
        return list_
