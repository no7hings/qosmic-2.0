# coding:utf-8
import six

from ..core import base as _cor_base

from . import _base

from . import _role

from . import _asset

from . import _episode

from . import _sequence

from . import _shot

from . import _step

from . import _task


class Project(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Project
    VariantKey = _cor_base.EntityVariantKeys.Project

    StepCls = _step.Step
    TaskCls = _task.Task

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    # step
    def steps(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []
        if 'resource_type' in kwargs:
            filters.append(['module', '=', self.ResourceTypeQuery[kwargs['resource_type']]])

        cgt_dtb = self._dtb_variants['project.database']

        for i_dtb_variants in t_tw.pipeline.get(
            cgt_dtb,
            t_tw.pipeline.get_id(cgt_dtb, filters),
            t_tw.pipeline.fields()
        ):
            list_.append(
                self._new_step_fnc(
                    dict(
                        root=self._variants['root'],
                        project=self._variants['project'],
                        #
                        resource_type=self.ResourceTypeMap.get(i_dtb_variants['module']),
                        #
                        step=i_dtb_variants['entity'],
                    ),
                    i_dtb_variants
                )
            )
        return list_

    def step(self, name, **kwargs):
        t_tw = self._stage._api

        filters = [['entity', '=', name]]

        cgt_dtb = self._dtb_variants['project.database']

        id_list = t_tw.pipeline.get_id(cgt_dtb, filters)
        if id_list:
            dtb_variants = t_tw.pipeline.get(
                cgt_dtb,
                id_list, t_tw.pipeline.fields()
            )[0]
            dtb_variants['project.database'] = cgt_dtb
            return self._new_step_fnc(
                dict(
                    root=self._variants['root'],
                    project=self._variants['project'],
                    #
                    resource_type=self.ResourceTypeMap[dtb_variants['module']],
                    #
                    step=dtb_variants['entity'],
                ),
                dtb_variants
            )

    # role
    def roles(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = self.CgtEntityTypes.Role

        for i_dtb_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            i_dtb_variants['project.database'] = cgt_dtb
            list_.append(
                self._root._new_entity_fnc(
                    _role.Role,
                    dict(
                        root=self._variants['root'],
                        project=self._variants['project'],
                        role=i_dtb_variants['asset_type.entity'],
                        #
                        entity_name=i_dtb_variants['asset_type.entity'],
                        entity_gui_name=i_dtb_variants.get('asset_type.cn_name'),
                    ),
                    i_dtb_variants
                )
            )
        return list_

    def role(self, name, **kwargs):
        t_tw = self._stage._api

        filters = [['asset_type.entity', '=', name]]

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = self.CgtEntityTypes.Role

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            dtb_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            dtb_variants['project.database'] = cgt_dtb
            return self._root._new_entity_fnc(
                _role.Role,
                dict(
                    root=self._variants['root'],
                    project=self._variants['project'],
                    role=dtb_variants['asset_type.entity'],
                    #
                    entity_name=dtb_variants['asset_type.entity'],
                    entity_gui_name=dtb_variants.get('asset_type.cn_name'),
                ),
                dtb_variants
            )

    # asset
    def assets(self, **kwargs):
        """
        @param kwargs: role = str or list
        @return: list
        """
        t_tw = self._stage._api

        list_ = []

        filters = []
        if 'role' in kwargs:
            vs = kwargs['role']
            if isinstance(vs, six.string_types):
                opt = '='
            elif isinstance(vs, list):
                opt = 'in'
            else:
                raise RuntimeError()
            filters.append(['asset_type.entity', opt, vs])

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = self.CgtEntityTypes.Asset

        for i_dtb_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            i_dtb_variants['project.database'] = cgt_dtb
            list_.append(
                self._root._new_entity_fnc(
                    _asset.Asset,
                    dict(
                        root=self._variants['root'],
                        project=self._variants['project'],
                        #
                        role=i_dtb_variants['asset_type.entity'],
                        asset=i_dtb_variants['asset.entity'],
                        #
                        resource_type=self.ResourceTypeMap[cgt_type],
                        #
                        entity_name=i_dtb_variants['asset.entity'],
                        entity_gui_name=i_dtb_variants.get('asset.cn_name')
                    ),
                    i_dtb_variants
                )
            )
        return list_

    def asset(self, name, **kwargs):
        t_tw = self._stage._api

        filters = [['asset.entity', '=', name]]

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = self.CgtEntityTypes.Asset

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            dtb_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            dtb_variants['project.database'] = cgt_dtb
            return self._root._new_entity_fnc(
                _asset.Asset,
                dict(
                    root=self._variants['root'],
                    project=self._variants['project'],
                    #
                    role=dtb_variants['asset_type.entity'],
                    asset=dtb_variants['asset.entity'],
                    #
                    resource_type=self.ResourceTypeMap[cgt_type],
                    #
                    entity_name=dtb_variants['asset.entity'],
                    entity_gui_name=dtb_variants.get('asset.cn_name')
                ),
                dtb_variants
            )

    # episode
    def episodes(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = self.CgtEntityTypes.Episode

        for i_dtb_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            i_dtb_variants['project.database'] = cgt_dtb
            list_.append(
                self._root._new_entity_fnc(
                    _episode.Episode,
                    dict(
                        root=self._variants['root'],
                        project=self._variants['project'],
                        episode=i_dtb_variants['eps.entity'],
                        #
                        entity_name=i_dtb_variants['eps.entity'],
                        entity_gui_name=i_dtb_variants.get('eps.cn_name')
                    ),
                    i_dtb_variants
                )
            )
        return list_

    def episode(self, name, **kwargs):
        t_tw = self._stage._api

        entity_cls = _episode.Episode

        opt = self._root._to_resource_filter_opt_fnc(entity_cls.VariantKey)
        filters = [['eps.entity', opt, name]]

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = self.CgtEntityTypes.Episode

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            dtb_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            dtb_variants['project.database'] = cgt_dtb
            return self._root._new_entity_fnc(
                entity_cls,
                dict(
                    root=self._variants['root'],
                    project=self._variants['project'],
                    episode=dtb_variants.get('eps.entity'),
                    #
                    entity_name=dtb_variants['eps.entity'],
                    entity_gui_name=dtb_variants.get('eps.cn_name')
                ),
                dtb_variants
            )

    # sequence
    def sequences(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []
        if 'episode' in kwargs:
            vs = kwargs['episode']
            if isinstance(vs, six.string_types):
                opt = '='
            elif isinstance(vs, list):
                opt = 'in'
            else:
                raise RuntimeError()
            filters.append(['eps.entity', opt, vs])

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = self.CgtEntityTypes.Sequence

        for i_dtb_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            i_dtb_variants['project.database'] = cgt_dtb
            list_.append(
                self._root._new_entity_fnc(
                    _sequence.Sequence,
                    dict(
                        root=self._variants['root'],
                        project=self._variants['project'],
                        #
                        episode=i_dtb_variants['eps.entity'],
                        sequence=i_dtb_variants['seq.entity'],
                        #
                        resource_type=self.ResourceTypeMap[cgt_type],
                        #
                        entity_name=i_dtb_variants['seq.entity'],
                        entity_gui_name=i_dtb_variants.get('seq.cn_name')
                    ),
                    i_dtb_variants
                )
            )
        return list_

    def sequence(self, name, **kwargs):
        t_tw = self._stage._api

        entity_cls = _sequence.Sequence

        opt = self._root._to_resource_filter_opt_fnc(entity_cls.VariantKey)
        filters = [['seq.entity', opt, name]]

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = self.CgtEntityTypes.Sequence

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            dtb_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            dtb_variants['project.database'] = cgt_dtb
            return self._root._new_entity_fnc(
                entity_cls,
                dict(
                    root=self._variants['root'],
                    project=self._variants['project'],
                    #
                    episode=dtb_variants.get('eps.entity'),
                    sequence=dtb_variants.get('seq.entity'),
                    #
                    resource_type=self.ResourceTypeMap[cgt_type],
                    #
                    entity_name=dtb_variants['seq.entity'],
                    entity_gui_name=dtb_variants.get('seq.cn_name')
                ),
                dtb_variants
            )

    # shot
    def shots(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []
        if 'episode' in kwargs:
            vs = kwargs['episode']
            if isinstance(vs, six.string_types):
                opt = '='
            elif isinstance(vs, list):
                opt = 'in'
            else:
                raise RuntimeError()
            filters.append(['eps.entity', opt, vs])
        if 'sequence' in kwargs:
            vs = kwargs['sequence']
            if isinstance(vs, six.string_types):
                opt = '='
            elif isinstance(vs, list):
                opt = 'in'
            else:
                raise RuntimeError()
            filters.append(['seq.entity', opt, vs])

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = self.CgtEntityTypes.Shot

        for i_dtb_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            i_dtb_variants['project.database'] = cgt_dtb
            list_.append(
                self._root._new_entity_fnc(
                    _shot.Shot,
                    dict(
                        root=self._variants['root'],
                        project=self._variants['project'],
                        # may no episode?
                        episode=i_dtb_variants.get('eps.entity'),
                        sequence=i_dtb_variants.get('seq.entity'),
                        shot=i_dtb_variants['shot.entity'],
                        #
                        resource_type=self.ResourceTypeMap[cgt_type],
                        #
                        entity_name=i_dtb_variants['shot.entity'],
                        entity_gui_name=i_dtb_variants.get('shot.cn_name')
                    ),
                    i_dtb_variants
                )
            )
        return list_

    def shot(self, name, **kwargs):
        t_tw = self._stage._api

        entity_cls = _shot.Shot

        opt = self._root._to_resource_filter_opt_fnc(entity_cls.VariantKey)
        filters = [['shot.entity', opt, name]]

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = self.CgtEntityTypes.Shot

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            dtb_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            dtb_variants['project.database'] = cgt_dtb
            return self._root._new_entity_fnc(
                _shot.Shot,
                dict(
                    root=self._variants['root'],
                    project=self._variants['project'],
                    #
                    episode=dtb_variants.get('eps.entity'),
                    sequence=dtb_variants.get('seq.entity'),
                    shot=dtb_variants['shot.entity'],
                    #
                    resource_type=self.ResourceTypeMap[cgt_type],
                    #
                    entity_name=dtb_variants['shot.entity'],
                    entity_gui_name=dtb_variants.get('shot.cn_name')
                ),
                dtb_variants
            )

    # task
    def all_project_tasks(self, **kwargs):
        return []

    def all_asset_tasks(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []
        # for user
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
        cgt_type = self.CgtEntityTypes.Asset

        for i_dtb_variants in t_tw.task.get(
            cgt_dtb, cgt_type,
            # fixme: limit to 1000?
            t_tw.task.get_id(cgt_dtb, cgt_type, filters)[:1000],
            t_tw.task.fields(cgt_dtb, cgt_type)
        ):
            i_variants = dict(
                root=self._variants['root'],
                project=self._variants['project'],
                #
                role=i_dtb_variants['asset_type.entity'],
                asset=i_dtb_variants['asset.entity'],
                #
                resource_type=self.ResourceTypeMap[cgt_type],
            )
            i_entity_path = self.to_entity_path(self.EntityTypes.Asset, i_variants)
            i_variants.update(
                dict(
                    entity_path=i_entity_path,
                    #
                    step=i_dtb_variants['task.pipeline'],
                    task=i_dtb_variants['task.entity'],
                )
            )
            list_.append(
                self._new_task_fnc(
                    i_variants,
                    i_dtb_variants
                )
            )
        return list_

    def all_episode_tasks(self, **kwargs):
        return []

    def all_sequence_tasks(self, **kwargs):
        return []

    def all_shot_tasks(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = [
            ['project.entity', '=', self._dtb_variants['project.entity']],
        ]
        # for user
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
        cgt_type = self.CgtEntityTypes.Shot

        for i_dtb_variants in t_tw.task.get(
            cgt_dtb, cgt_type,
            # fixme: limit to 1000?
            t_tw.task.get_id(cgt_dtb, cgt_type, filters)[:1000],
            t_tw.task.fields(cgt_dtb, cgt_type)
        ):
            i_variants = dict(
                root=self._variants['root'],
                project=self._variants['project'],
                #
                episode=i_dtb_variants.get('eps.entity'),
                sequence=i_dtb_variants.get('seq.entity'),
                shot=i_dtb_variants['shot.entity'],
                #
                resource_type=self.ResourceTypeMap[cgt_type],
            )
            i_entity_path = self.to_entity_path(self.EntityTypes.Shot, i_variants)
            i_variants.update(
                dict(
                    entity_path=i_entity_path,
                    #
                    step=i_dtb_variants['task.pipeline'],
                    task=i_dtb_variants['task.entity'],
                )
            )
            list_.append(
                self._new_task_fnc(
                    i_variants,
                    i_dtb_variants
                )
            )
        return list_
