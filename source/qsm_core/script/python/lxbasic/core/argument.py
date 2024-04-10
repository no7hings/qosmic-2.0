# coding:utf-8
import six

import json

import collections

import re

from . import raw as bsc_cor_raw


class ArgDictStringMtd(object):
    ARGUMENT_SEP = '&'

    @classmethod
    def to_string(cls, **kwargs):
        vars_ = []
        keys = kwargs.keys()
        keys.sort()
        for k in keys:
            v = kwargs[k]
            if isinstance(v, (tuple, list)):
                # must convert to str
                vars_.append('{}={}'.format(k, '+'.join(map(str, v))))
            else:
                vars_.append('{}={}'.format(k, v))
        return cls.ARGUMENT_SEP.join(vars_)


class ArgDictStringOpt(object):
    #  =%20
    # "=%22
    # #=%23
    # %=%25
    # &=%26
    # (=%28
    # )=%29
    # +=%2B
    # ,=%2C
    # /=%2F
    # :=%3A
    # ;=%3B
    # <=%3C
    # ==%3D
    # >=%3E
    # ?=%3F
    # @=%40
    # \=%5C
    # |=%7C
    ARGUMENT_SEP = '&'

    def __init__(self, option, default_option=None):
        dict_ = collections.OrderedDict()
        if isinstance(default_option, six.string_types):
            self._update_by_string_(dict_, default_option)
        elif isinstance(default_option, dict):
            dict_.update(default_option)

        if isinstance(option, six.string_types):
            self._update_by_string_(dict_, option)
        elif isinstance(option, dict):
            dict_.update(option)
        else:
            raise TypeError()

        self.__dict = dict_

        self._string_dict = {
            'key': self.to_string()
        }

    @classmethod
    def _update_by_string_(cls, dict_, option_string):
        ks = [i.lstrip().rstrip() for i in option_string.split(cls.ARGUMENT_SEP)]
        for k in ks:
            key, value = k.split('=')
            value = value.lstrip().rstrip()

            value = cls._set_value_convert_by_string_(value)
            dict_[key.lstrip().rstrip()] = value

    @classmethod
    def _set_value_convert_by_string_(cls, value_string):
        if isinstance(value_string, six.string_types):
            if value_string in ['None']:
                return None
            elif value_string in ['True', 'False']:
                return eval(value_string)
            elif value_string in ['true', 'false']:
                return [True, False][['true', 'false'].index(value_string)]
            elif value_string in ['()', '[]', '{}']:
                return eval(value_string)
            elif '+' in value_string:
                return value_string.split('+')
            else:
                return value_string

    def get_value(self):
        return self.__dict

    value = property(get_value)

    def get(self, key, as_array=False, as_integer=False, as_float=False):
        if key in self.__dict:
            _ = self.__dict[key]
            if as_integer is True:
                if isinstance(_, int):
                    return _
                elif isinstance(_, float):
                    return int(_)
                elif isinstance(_, six.string_types):
                    if _:
                        if str(_).isdigit():
                            return int(_)
                        elif bsc_cor_raw.RawTextOpt(_).get_is_float():
                            return int(float(_))
                        return 0
                    return 0
                return 0
            elif as_float is True:
                if isinstance(_, int):
                    return float(_)
                elif isinstance(_, float):
                    return _
                elif isinstance(_, six.string_types):
                    if _:
                        if str(_).isdigit():
                            return float(_)
                        elif bsc_cor_raw.RawTextOpt(_).get_is_float():
                            return float(_)
                        return 0.0
                    return 0.0
                return 0.0
            if as_array is True:
                if isinstance(_, (tuple, list)):
                    return _
                if _:
                    return [_]
                return []
            return self.__dict[key]

    def get_as_path(self, key):
        pass

    def get_as_array(self, key):
        return self.get(key, as_array=True)

    def get_as_boolean(self, key):
        return self.get(key) or False

    def get_as_integer(self, key):
        return self.get(key, as_integer=True)

    def get_as_float(self, key):
        return self.get(key, as_float=True)

    def pop(self, key):
        if key in self.__dict:
            return self.__dict.pop(
                key
            )

    def get_as(self, key, type_):
        pass

    def set(self, key, value):
        self.__dict[key] = value

    def update_from(self, dict_, override=True):
        if override is False:
            [dict_.pop(k) for k in dict_ if k in self.__dict]

        self.__dict.update(dict_)

    def set_update_by_string(self, option):
        self.__dict.update(
            self.__class__(option).get_value()
        )

    def get_key_is_exists(self, key):
        return key in self.__dict

    def get_raw(self):
        return self.__dict

    def to_option(self):
        return self.to_string()

    def to_string(self):
        return ArgDictStringMtd.to_string(
            **self.__dict
        )

    def to_dict(self):
        return self.__dict

    def __str__(self):
        return json.dumps(
            self.__dict,
            indent=4,
            skipkeys=True,
            sort_keys=True
        )
    
    def __contains__(self, item):
        return item in self.__dict

    def __getitem__(self, item):
        return self.__dict[item]
    

class ArgListStringOpt(object):
    PATTERN = r'[\[](.*?)[\]]'

    def __init__(self, arguments):
        self._arguments = re.findall(re.compile(self.PATTERN, re.S), arguments) or []

    def get_value(self):
        return self._arguments

    value = property(get_value)
