# coding:utf-8
import fnmatch

import collections

import json


class AbsProperties(object):
    PATHSEP = None

    def __init__(self, obj, raw):
        self._obj = obj
        if isinstance(raw, dict):
            self._value = raw
        else:
            raise TypeError()

    @property
    def obj(self):
        return self._obj

    @property
    def value(self):
        return self._value

    def get_all_keys(self):
        def _rcs_fnc(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = '{}.{}'.format(k_, _k)
                else:
                    _key = _k
                lis.append(_key)
                if isinstance(_v, dict):
                    _rcs_fnc(_key, _v)

        lis = []
        _rcs_fnc(None, self._value)
        return lis

    def get_all_leaf_keys(self):
        def _rcs_fnc(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = '{}.{}'.format(k_, _k)
                else:
                    _key = _k
                #
                if isinstance(_v, dict):
                    _rcs_fnc(_key, _v)
                else:
                    lis.append(_key)

        lis = []
        _rcs_fnc(None, self._value)
        return lis

    def get_keys(self, regex=None):
        _ = self.get_all_keys()
        if regex is not None:
            return fnmatch.filter(_, regex)
        return _

    def get(self, key_path, default_value=None):
        ks = key_path.split(self.PATHSEP)
        v = self._value
        for k in ks:
            if isinstance(v, dict):
                if k in v:
                    v = v[k]
                else:
                    return default_value
            else:
                return default_value
        return v

    def get_key_names_at(self, key_path):
        value = self.get(key_path)
        if isinstance(value, dict):
            return value.keys()
        return []

    def set(self, key_path, value):
        ks = key_path.split(self.PATHSEP)
        v = self._value
        seq_last = len(ks)-1
        for seq, k in enumerate(ks):
            if seq == seq_last:
                v[k] = value
            else:
                if k not in v:
                    v[k] = collections.OrderedDict()
                v = v[k]

    def __str__(self):
        return json.dumps(
            self.value,
            indent=4
        )
