# coding:utf-8
# resource
from . import base as _base

import platform


class BscExe(object):
    BRANCH = 'executes'

    @classmethod
    def get(cls, key):
        platform_key = platform.system().lower()
        result = _base.BscResource.get(
            '{}/{}/{}'.format(cls.BRANCH, platform_key, key)
        )
        if result is not None:
            return result
