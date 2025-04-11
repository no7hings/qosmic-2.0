# coding:utf-8
import lxbasic.pinyin as bsc_pinyin

from ..core import base as _cor_base

from . import _base


class Sequence(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Sequence
    VariantKey = _cor_base.EntityVariantKeys.Sequence

    def __init__(self, *args, **kwargs):
        super(Sequence, self).__init__(*args, **kwargs)

    def shots(self, **kwargs):
        return self._root.project(
            self._variants['project']
        ).shots(
            episode=self._cgt_variants['eps.entity'],
            sequence=self._cgt_variants['seq.entity'],
            **kwargs
        )
