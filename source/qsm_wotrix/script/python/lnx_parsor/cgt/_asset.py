# coding:utf-8
import six

from ..core import base as _cor_base

from . import _base

from . import _task


class Asset(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Asset
    VariantKey = _cor_base.EntityVariantKeys.Asset

    TaskCls = _task.Task

    @classmethod
    def _to_task_variants(cls, variants, dtb_variants):
        return dict(
            entity_path=variants['entity_path'],
            #
            root=variants['root'],
            project=variants['project'],
            role=variants['role'],
            asset=variants['asset'],
            #
            step=dtb_variants['task.pipeline'],
            task=dtb_variants['task.entity'],
        )

    def __init__(self, *args, **kwargs):
        super(Asset, self).__init__(*args, **kwargs)

    def tasks(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = [
            ['asset.entity', '=', self._dtb_variants['asset.entity']],
        ]
        if 'account' in kwargs:
            vs = kwargs['account']
            if isinstance(vs, six.string_types):
                opt = '='
            elif isinstance(vs, list):
                opt = 'in'
            else:
                raise RuntimeError()
            filters.append(
                ['task.account', opt, vs]
            )

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = 'asset'

        for i_dtb_variants in t_tw.task.get(
            cgt_dtb, cgt_type,
            t_tw.task.get_id(cgt_dtb, cgt_type, filters),
            t_tw.task.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                self._new_task_fnc(
                    dict(
                        entity_path=self._variants['entity_path'],
                        #
                        root=self._variants['root'],
                        project=self._variants['project'],
                        role=self._variants['role'],
                        asset=self._variants['asset'],
                        #
                        step=i_dtb_variants['task.pipeline'],
                        task=i_dtb_variants['task.entity'],
                    ),
                    i_dtb_variants
                )
            )
        return list_

    def task(self, name):
        t_tw = self._stage._api

        filters = [
            ['asset.entity', '=', self._dtb_variants['asset.entity']],
            ['task.entity', '=', name]
        ]

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = 'asset'

        id_list = t_tw.task.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            dtb_variants = t_tw.task.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.task.fields(cgt_dtb, cgt_type)
            )[0]
            return self._new_task_fnc(
                dict(
                    entity_path=self._variants['entity_path'],
                    #
                    root=self._variants['root'],
                    project=self._variants['project'],
                    role=self._variants['role'],
                    asset=self._variants['asset'],
                    #
                    step=dtb_variants['task.pipeline'],
                    task=dtb_variants['task.entity'],
                ),
                dtb_variants
            )
