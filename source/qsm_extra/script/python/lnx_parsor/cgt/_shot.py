# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _task


class Shot(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Shot
    VariantKey = _cor_base.EntityVariantKeys.Shot

    TaskCls = _task.Task

    def __init__(self, *args, **kwargs):
        super(Shot, self).__init__(*args, **kwargs)

    def tasks(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = [
            ['shot.entity', '=', self._dtb_variants['shot.entity']],
        ]

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = 'shot'

        for i_dtb_variants in t_tw.task.get(
            cgt_dtb, cgt_type,
            t_tw.task.get_id(cgt_dtb, cgt_type, filters),
            t_tw.task.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                self._new_task_fnc(
                    dict(
                        root=self._variants['root'],
                        project=self._variants['project'],
                        episode=self._variants.get('episode'),
                        sequence=self._variants.get('sequence'),
                        shot=self._variants['shot'],

                        task=i_dtb_variants['task.entity'],
                    ),
                    i_dtb_variants
                )
            )
        return list_

    def task(self, name):
        t_tw = self._stage._api

        filters = [
            ['shot.entity', '=', self._dtb_variants['shot.entity']],
            ['task.entity', '=', name]
        ]

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = 'shot'

        id_list = t_tw.task.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            dtb_variants = t_tw.task.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.task.fields(cgt_dtb, cgt_type)
            )[0]
            return self._new_task_fnc(
                dict(
                    root=self._variants['root'],
                    project=self._variants['project'],
                    episode=self._variants.get('episode'),
                    sequence=self._variants.get('sequence'),
                    shot=self._variants['shot'],

                    task=dtb_variants['task.entity'],
                ),
                dtb_variants
            )
