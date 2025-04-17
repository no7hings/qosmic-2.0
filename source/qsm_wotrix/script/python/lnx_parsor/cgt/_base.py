# coding:utf-8
import json

import lxbasic.core as bsc_core

from ..core import base as _cor_base


class AbsEntity(_cor_base.AbsEntityBase):
    Type = None

    StepCls = None
    TaskCls = None
    
    class CgtEntityTypes:
        Project = 'project'
        Role = 'asset_type'
        Asset = 'asset'
        Episode = 'eps'
        Sequence = 'seq'
        Shot = 'shot'

        Step = 'pipeline'

    ResourceTypeMap = {
        CgtEntityTypes.Project: _cor_base.ResourceTypes.Project,
        CgtEntityTypes.Asset: _cor_base.ResourceTypes.Asset,
        CgtEntityTypes.Episode: _cor_base.ResourceTypes.Episode,
        CgtEntityTypes.Sequence: _cor_base.ResourceTypes.Sequence,
        CgtEntityTypes.Shot: _cor_base.ResourceTypes.Shot,
    }
    ResourceTypeQuery = {
        v: k for k, v in ResourceTypeMap.items()
    }

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
            bsc_core.ensure_string(json.dumps(self._variants, indent=4, ensure_ascii=False))
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

    def _new_step_fnc(self, variants, dtb_variants):
        variants = _cor_base.EntityVariantKeyFnc.clean_fnc(variants)

        path = self.to_step_path(variants)
        return self.StepCls(
            self, path, variants, dtb_variants=dtb_variants
        )

    def _new_task_fnc(self, variants, dtb_variants):
        variants = _cor_base.EntityVariantKeyFnc.clean_fnc(variants)

        path = self.to_task_path(variants)
        return self.TaskCls(
            self, path, variants, dtb_variants=dtb_variants
        )

    def tasks(self, **kwargs):
        raise NotImplementedError()
    
    def task(self, name):
        raise NotImplementedError()


class AbsResourceType(_cor_base.AbsResourceTypeBase):
    def __init__(self, *args, **kwargs):
        super(AbsResourceType, self).__init__(*args, **kwargs)
        self._dtb_variants = kwargs.get('dtb_variants', {})

    @property
    def dtb_variants(self):
        return self._dtb_variants


class AbsStep(_cor_base.AbsStepBase):
    def __init__(self, *args, **kwargs):
        super(AbsStep, self).__init__(*args, **kwargs)
        self._dtb_variants = kwargs.get('dtb_variants', {})

    @property
    def dtb_variants(self):
        return self._dtb_variants


class AbsTask(_cor_base.AbsTaskBase):

    def __init__(self, *args, **kwargs):
        super(AbsTask, self).__init__(*args, **kwargs)
        self._dtb_variants = kwargs.get('dtb_variants', {})

    @property
    def dtb_variants(self):
        return self._dtb_variants

    @property
    def step_name(self):
        return self._dtb_variants.get('pipeline.entity')
