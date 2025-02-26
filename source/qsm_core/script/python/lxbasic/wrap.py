# coding:utf-8
import six as _six

import platform as _platform

import getpass as _getpass


def ensure_string(s):
    if isinstance(s, _six.text_type):
        if _six.PY2:
            return s.encode('utf-8')
    elif isinstance(s, _six.binary_type):
        if _six.PY3:
            return s.decode('utf-8')
    return s


def ensure_unicode(s):
    if isinstance(s, _six.text_type):
        return s
    elif isinstance(s, _six.binary_type):
        return s.decode('utf-8')
    else:
        return s


def ensure_mbcs(s):
    if isinstance(s, _six.text_type):
        if _six.PY2:
            return s.encode('mbcs')
    return s


def is_linux():
    return _platform.system() == 'Linux'


def is_windows():
    return _platform.system() == 'Windows'


def get_user_name():
    return _getpass.getuser()
