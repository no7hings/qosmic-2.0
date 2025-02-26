# coding:utf-8
import os

from ..wrap import *


class UserBase:
    @classmethod
    def get_windows_directory(cls):
        return '{}{}/.qosmic'.format(
            os.environ.get('HOMEDRIVE', 'c:'),
            os.environ.get('HOMEPATH', '/temp')
        ).replace('\\', '/')

    @classmethod
    def get_linux_directory(cls):
        return '{}/.qosmic'.format(
            os.environ.get('HOME', '/home/{}'.format(get_user_name()))
        )

    @classmethod
    def get_directory(cls):
        if is_windows():
            return cls.get_windows_directory()
        elif is_linux():
            return cls.get_linux_directory()
        raise SystemError()
