# coding:utf-8
from ..core import base as _cor_base

from . import _base


class Role(_base.AbsEntity):
    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)

    def assets(self, **kwargs):
        return self._root.project(
            self._variants['project']
        ).assets(
            role=self._variants['role'],
            **kwargs
        )
