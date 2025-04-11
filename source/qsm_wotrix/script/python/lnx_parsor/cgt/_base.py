# coding:utf-8
import json

import lxbasic.core as bsc_core

from ..core import base as _cor_base


class AbsEntity(_cor_base.AbsEntityBase):
    Type = None

    TaskCls = None

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return True

    def __init__(self, root, path, variants, dtb_variants=None):
        self._root = root
        self._stage = root._stage

        self._entity_path = path
        self._path_opt = bsc_core.BscNodePathOpt(self._entity_path)

        self._variants = variants

        self._properties = _cor_base.EntityProperties(**variants)

        self._entity_type = self.Type
        self._variants['entity_type'] = self._entity_type
        self._variants['entity_path'] = self._entity_path

        self._dtb_variants = dtb_variants or {}

        self._task_dict = {}

    def __str__(self):
        return 'Entity({})'.format(
            json.dumps(self._variants, indent=4)
        )

    def __repr__(self):
        return '\n'+self.__str__()

    @property
    def stage(self):
        return self._stage

    @property
    def type(self):
        return self.Type

    @property
    def path(self):
        return self._entity_path

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
    def properties(self):
        return self._properties

    @property
    def dtb_variants(self):
        return self._dtb_variants

    def _new_task_fnc(self, variants, dtb_variants):
        variants = _cor_base.EntityVariantKeyFnc.clean_fnc(variants)

        path = self.to_task_path(self.Type, variants)
        return self.TaskCls(
            self, path, variants, dtb_variants=dtb_variants
        )

    def tasks(self, **kwargs):
        raise NotImplementedError()
    
    def task(self, name):
        raise NotImplementedError()


class AbsTask(_cor_base.AbsTaskBase):

    def __init__(self, *args, **kwargs):
        super(AbsTask, self).__init__(*args, **kwargs)
        self._dtb_variants = kwargs.get('dtb_variants', {})
