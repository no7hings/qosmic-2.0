# coding:utf-8
from ..core import base as _cor_base

from . import _base


class User(_base.AbsEntity):
    Type = _cor_base.EntityTypes.User
    VariantKey = _cor_base.EntityVariantKeys.User

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
