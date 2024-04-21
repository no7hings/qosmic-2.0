# coding:utf-8
# resource
from . import base as rsc_cor_base

import platform


class RscExtendExe(object):
    BRANCH = 'executes'

    @classmethod
    def get(cls, key):
        platform_key = platform.system().lower()
        result = rsc_cor_base.ExtendResource.get(
            '{}/{}/{}'.format(cls.BRANCH, platform_key, key)
        )
        if result is not None:
            return result
