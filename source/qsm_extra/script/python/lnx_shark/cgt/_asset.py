# coding:utf-8
from ..core import base as _cor_base

from . import _base


class Asset(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Asset

    def __init__(self, *args, **kwargs):
        super(Asset, self).__init__(*args, **kwargs)
