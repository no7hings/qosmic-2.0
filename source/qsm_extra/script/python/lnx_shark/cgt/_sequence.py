# coding:utf-8
from ..core import base as _cor_base

from . import _base


class Sequence(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Sequence

    def __init__(self, *args, **kwargs):
        super(Sequence, self).__init__(*args, **kwargs)

    def shots(self, **kwargs):
        return self._root.project(
            self._variants['project']
        ).shots(
            episode=self._variants['episode'],
            sequence=self._variants['sequence'],
            **kwargs
        )