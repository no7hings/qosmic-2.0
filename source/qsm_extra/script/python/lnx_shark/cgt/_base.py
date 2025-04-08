# coding:utf-8
import json

from ..core import base as _cor_base


class AbsEntity(object):
    Type = None

    def __init__(self, root, variants, cgt_variants=None):
        self._root = root
        self._stage = root._stage

        self._variants = _cor_base.EntityVariants(**variants)

        self._entity_type = self.Type
        self._variants['entity_type'] = self._entity_type

        self._cgt_variants = cgt_variants or {}

    def __str__(self):
        return '{}({})'.format(
            self._entity_type, json.dumps(self._cgt_variants, indent=4)
        )

    def __repr__(self):
        return '\n'+self.__str__()

    @property
    def variants(self):
        return self._variants

    @property
    def cgt_variants(self):
        return self._cgt_variants


