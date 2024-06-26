# coding:utf-8
from . import base as _base

from . import notice as _notice


class NoticePool(_base.AbsEntityPool):
    LOCATION_PTN = 'Z:/caches/database/prc-task/{user_name}/notices'

    CACHE = None

    CACHE_CLS = _notice.NoticesCache

    def __init__(self, location):
        super(NoticePool, self).__init__(location)

    def __str__(self):
        return '{}(location="{}")'.format(
            self.__class__.__name__, self._location
        )

    def __repr__(self):
        return self.__str__()
