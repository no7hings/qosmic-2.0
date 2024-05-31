# coding:utf-8

from . import base as _base


class History(_base.AbsEntity):
    def __init__(self, entities_cache, entity_id):
        super(History, self).__init__(entities_cache, entity_id)


class HistoriesCache(_base.AbsEntitiesCache):
    ENTITY_CLS = History

    def __init__(self, entity_pool):
        super(HistoriesCache, self).__init__(entity_pool)
