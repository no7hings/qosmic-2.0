# coding:utf-8
from ..core import base as _cor_base

from . import _base


class Shot(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Shot
    VariantKey = _cor_base.EntityVariantKeys.Shot

    def __init__(self, *args, **kwargs):
        super(Shot, self).__init__(*args, **kwargs)
