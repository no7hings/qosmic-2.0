# coding:utf-8
from . import base as _base

from . import task as _task


class Asset(_base.AbsEntity):
    Type = _base.EntityTypes.Asset
    VariantKey = _base.VariantKeys.Asset

    TaskQueryClass = _task.TaskQuery

    def __init__(self, *args, **kwargs):
        super(Asset, self).__init__(*args, **kwargs)


class AssetQuery(_base.AbsEntityQuery):
    EntityClass = Asset

    def __init__(self, *args, **kwargs):
        super(AssetQuery, self).__init__(*args, **kwargs)
