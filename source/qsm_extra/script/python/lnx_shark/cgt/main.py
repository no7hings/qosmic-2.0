# coding:utf-8
import json

import six

from .wrap import *

from ..core import base as _cor_base

__all__ = [
    'Stage',
]


class AbsEntity(object):
    Type = None

    def __init__(self, root, variants, cgt_variants=None):
        self._root = root
        self._stage = root._stage

        self._variants = _cor_base.Variants(**variants)

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


class User(AbsEntity):
    Type = _cor_base.EntityTypes.User

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)


class Asset(AbsEntity):
    Type = _cor_base.EntityTypes.Asset

    def __init__(self, *args, **kwargs):
        super(Asset, self).__init__(*args, **kwargs)


class Shot(AbsEntity):
    Type = _cor_base.EntityTypes.Shot

    def __init__(self, *args, **kwargs):
        super(Shot, self).__init__(*args, **kwargs)


class Sequence(AbsEntity):
    Type = _cor_base.EntityTypes.Sequence

    def __init__(self, *args, **kwargs):
        super(Sequence, self).__init__(*args, **kwargs)
        
    def shots(self, **kwargs):
        return self._root.project(
            self._variants['project']
        ).shots(
            episode=self._variants['episode'], 
            sequence=self._variants['sequence'], 
            **kwargs
        )


class Episode(AbsEntity):
    Type = _cor_base.EntityTypes.Episode

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


class Project(AbsEntity):
    Type = _cor_base.EntityTypes.Project

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    # asset
    def assets(self, **kwargs):
        """
        @param kwargs: role = str or list
        @return: list
        """
        t_tw = self._stage._tw

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

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'asset'

        for i_cgt_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                Asset(
                    self._root,
                    dict(
                        project=self._variants['project'],
                        role=i_cgt_variants['asset_type.entity'],
                        asset=i_cgt_variants['asset.entity']
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def asset(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['asset.entity', '=', name]]

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'asset'

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            cgt_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            return Asset(
                self._root,
                dict(
                    project=self._variants['project'],
                    role=cgt_variants['asset_type.entity'],
                    asset=cgt_variants['asset.entity']
                ),
                cgt_variants
            )

    # episode
    def episodes(self, **kwargs):
        t_tw = self._stage._tw

        list_ = []

        filters = []

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'eps'

        for i_cgt_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                Episode(
                    self._root,
                    dict(
                        project=self._variants['project'],
                        episode=i_cgt_variants['eps.entity'],
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def episode(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['eps.entity', '=', name]]

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'eps'

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            cgt_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            return Episode(
                self._root,
                dict(
                    project=self._variants['project'],
                    episode=cgt_variants.get('eps.entity'),
                ),
                cgt_variants
            )

    # sequence
    def sequences(self, **kwargs):
        t_tw = self._stage._tw

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

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'seq'

        for i_cgt_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                Sequence(
                    self._root,
                    dict(
                        project=self._variants['project'],
                        episode=i_cgt_variants['eps.entity'],
                        sequence=i_cgt_variants['seq.entity']
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def sequence(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['seq.entity', '=', name]]

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'seq'

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            cgt_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            return Sequence(
                self._root,
                dict(
                    project=self._variants['project'],
                    episode=cgt_variants.get('eps.entity'),
                    sequence=cgt_variants.get('seq.entity')
                ),
                cgt_variants
            )

    # shot
    def shots(self, **kwargs):
        t_tw = self._stage._tw

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

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'shot'

        for i_cgt_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                Shot(
                    self._root,
                    dict(
                        project=self._variants['project'],
                        # may non exists.
                        episode=i_cgt_variants.get('eps.entity'),
                        sequence=i_cgt_variants.get('seq.entity'),
                        shot=i_cgt_variants['shot.entity']
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def shot(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['shot.entity', '=', name]]

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'shot'

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            cgt_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            return Shot(
                self._root,
                dict(
                    project=self._variants['project'],
                    episode=cgt_variants.get('eps.entity'),
                    sequence=cgt_variants.get('seq.entity'),
                    shot=cgt_variants['shot.entity']
                ),
                cgt_variants
            )


class Root(AbsEntity):
    Type = _cor_base.EntityTypes.Root

    def __init__(self, stage, location='X:'):
        self._stage = stage
        # create before super
        self._root_entity_stack = _cor_base.EntityStack()

        super(Root, self).__init__(
            # root is self
            self,
            dict(root=location),
            {}
        )

    @property
    def entity_stack(self):
        return self._root_entity_stack

    def current_user(self):
        t_tw = self._stage._tw
        return self.user(name=t_tw.login.account())

    def user(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['account.entity', '=', name]]
        id_list = t_tw.account.get_id(
            filters
        )
        if id_list:
            cgt_variants = t_tw.account.get(id_list, t_tw.account.fields())[0]
            return User(
                self,
                dict(
                    cgt_user=name,
                    user=None
                ),
                cgt_variants
            )

    def users(self, **kwargs):
        t_tw = self._stage._tw

        list_ = []

        filters = []
        if 'active' in kwargs:
            filters.append(['account.status', '=', 'Y'])

        for i_cgt_variants in t_tw.account.get(
            t_tw.account.get_id(filters),
            t_tw.account.fields()
        ):
            list_.append(
                User(
                    self,
                    dict(
                        cgt_user=i_cgt_variants['account.entity'],
                        # todo: add field to save login user name
                        user=None,
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def project(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['project.entity', '=', name]]
        id_list = t_tw.project.get_id(filters)
        if id_list:
            cgt_variants = t_tw.project.get(id_list, t_tw.project.fields())[0]
            return Project(
                self._root,
                dict(
                    project=name
                ),
                cgt_variants
            )

    def projects(self, **kwargs):
        t_tw = self._stage._tw

        list_ = []

        filters = []
        if 'active' in kwargs:
            filters.append(['project.status', '=', 'Active'])

        for i_cgt_variants in t_tw.project.get(
            t_tw.project.get_id(filters),
            t_tw.project.fields()
        ):
            list_.append(
                Project(
                    self._root,
                    dict(
                        project=i_cgt_variants['project.entity']
                    ),
                    i_cgt_variants
                )
            )
        return list_


class Stage(object):
    INSTANCE = None

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(Stage, cls).__new__(cls)
        if CGT_FLAG is True:
            # noinspection PyUnresolvedReferences
            self._tw = cgtw2.tw("192.168.15.180:8383")
        else:
            raise RuntimeError()

        self._root_dict = dict()
        cls.INSTANCE = self
        return self

    def root(self, location='X:'):
        if location in self._root_dict:
            return self._root_dict[location]

        instance = Root(self, location)
        self._root_dict[location] = instance
        return instance
