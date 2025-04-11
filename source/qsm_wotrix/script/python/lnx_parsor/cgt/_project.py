# coding:utf-8
import six

from ..core import base as _cor_base

from . import _base

from . import _role

from . import _asset

from . import _episode

from . import _sequence

from . import _shot


class Project(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Project
    VariantKey = _cor_base.EntityVariantKeys.Project

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    # role
    def roles(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []

        cgt_dtb = self._dtb_variants['project.database']
        cgt_type = 'asset_type'

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
        cgt_type = 'asset_type'

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
        cgt_type = 'asset'

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
                        role=i_dtb_variants['asset_type.entity'],
                        asset=i_dtb_variants['asset.entity'],
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
        cgt_type = 'asset'

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
                    role=dtb_variants['asset_type.entity'],
                    asset=dtb_variants['asset.entity'],
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
        cgt_type = 'eps'

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
        cgt_type = 'eps'

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
        cgt_type = 'seq'

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
                        episode=i_dtb_variants['eps.entity'],
                        sequence=i_dtb_variants['seq.entity'],
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
        cgt_type = 'seq'

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
                    sequence=dtb_variants.get('seq.entity'),
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
        cgt_type = 'shot'

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
        cgt_type = 'shot'

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
                    episode=dtb_variants.get('eps.entity'),
                    sequence=dtb_variants.get('seq.entity'),
                    shot=dtb_variants['shot.entity'],
                    #
                    entity_name=dtb_variants['shot.entity'],
                    entity_gui_name=dtb_variants.get('shot.cn_name')
                ),
                dtb_variants
            )
