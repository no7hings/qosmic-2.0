# coding:utf-8
from ..core import base as _cor_base

from . import _base


class Episode(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Episode
    VariantKey = _cor_base.EntityVariantKeys.Episode

    def __init__(self, *args, **kwargs):
        super(Episode, self).__init__(*args, **kwargs)

    def sequences(self, **kwargs):
        return self._root.project(
            self._variants['project']
        ).sequences(
            episode=self._variants['episode'],
            **kwargs
        )

    def shots(self, **kwargs):
        return self._root.project(
            self._variants['project']
        ).shots(
            episode=self._variants['episode'],
            **kwargs
        )
