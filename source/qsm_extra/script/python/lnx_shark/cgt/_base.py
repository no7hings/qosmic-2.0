# coding:utf-8
import json

import lxbasic.core as bsc_core

from ..core import base as _cor_base


class AbsEntity(_cor_base.AbsEntityBase):
    Type = None

    def __init__(self, root, path, variants, cgt_variants=None):
        self._root = root
        self._stage = root._stage

        self._path = path
        self._path_opt = bsc_core.BscNodePathOpt(self._path)

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
    def type(self):
        return self.Type

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._path_opt.get_name()

    @property
    def path_opt(self):
        return self._path_opt

    @property
    def variants(self):
        return self._variants

    @property
    def cgt_variants(self):
        return self._cgt_variants


