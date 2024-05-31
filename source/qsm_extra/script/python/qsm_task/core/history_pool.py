# coding:utf-8
from . import base as _base

from . import history as _history


class HistoryPool(_base.AbsEntityPool):
    LOCATION_PTN = 'Z:/caches/database/prc-task/{user_name}/history_pool'

    CACHE = None

    CACHE_CLS = _history.HistoriesCache

    def __init__(self, location):
        super(HistoryPool, self).__init__(location)

    def __str__(self):
        return '{}(location="{}")'.format(
            self.__class__.__name__, self._location
        )

    def __repr__(self):
        return self.__str__()
