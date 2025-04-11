# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _account

from . import _project


class Root(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Root
    VariantKey = _cor_base.EntityVariantKeys.Root

    def __init__(self, stage, location='X:'):
        self._stage = stage

        # create before super
        self._root_entity_stack = _cor_base.EntityStack()

        super(Root, self).__init__(
            # root is self
            self,
            '/',
            dict(root=location),
            {}
        )

    @property
    def entity_stack(self):
        return self._root_entity_stack

    def get_entity(self, path):
        return self._root_entity_stack.get(path)

    @classmethod
    def _to_resource_filter_opt_fnc(cls, variant_key):
        if variant_key in _cor_base.DisorderConfig()._entity_variant_cleanup_keys:
            return 'start'
        return '='

    def _new_entity_fnc(self, entity_cls, variants, cgt_variants):
        variants = _cor_base.EntityVariantKeyFnc.clean_fnc(variants)

        path = self.to_entity_path(entity_cls.Type, variants)
        if self._root_entity_stack.exists(path):
            return self._root_entity_stack.get(path)

        entity = entity_cls(
            self._root, path, variants, cgt_variants
        )
        self._root_entity_stack.register(path, entity)
        return entity

    def current_user(self):
        t_tw = self._stage._api
        return self.user(name=t_tw.login.account())

    def users(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []
        if 'active' in kwargs:
            filters.append(['account.status', '=', 'Y'])

        for i_cgt_variants in t_tw.account.get(
            t_tw.account.get_id(filters),
            t_tw.account.fields()
        ):
            list_.append(
                self._root._new_entity_fnc(
                    _account.User,
                    dict(
                        cgt_user=i_cgt_variants['account.entity'],
                        # todo: add field to save login
                        user=i_cgt_variants['account.login'],
                        #
                        entity_name=i_cgt_variants['account.entity'],
                        entity_name_chs=i_cgt_variants['account.name'],
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def user(self, name, **kwargs):
        t_tw = self._stage._api

        filters = [['account.entity', '=', name]]
        id_list = t_tw.account.get_id(
            filters
        )
        if id_list:
            cgt_variants = t_tw.account.get(id_list, t_tw.account.fields())[0]
            return self._root._new_entity_fnc(
                _account.User,
                dict(
                    cgt_user=name,
                    # todo: add field to save login
                    user=cgt_variants['account.login'],
                    #
                    entity_name=cgt_variants['account.entity'],
                    entity_name_chs=cgt_variants['account.name'],
                ),
                cgt_variants
            )

    def projects(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []
        if 'active' in kwargs:
            filters.append(['project.status', '=', 'Active'])

        for i_cgt_variants in t_tw.project.get(
            t_tw.project.get_id(filters),
            t_tw.project.fields()
        ):
            list_.append(
                self._root._new_entity_fnc(
                    _project.Project,
                    dict(
                        root=self._variants['root'],
                        project=i_cgt_variants['project.entity'],
                        #
                        entity_name=i_cgt_variants['project.entity'],
                        entity_name_chs=i_cgt_variants.get('project.full_name')
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def project(self, name, **kwargs):
        t_tw = self._stage._api

        entity_cls = _project.Project
        
        opt = self._root._to_resource_filter_opt_fnc(entity_cls.VariantKey)

        filters = [['project.entity', opt, name]]
        id_list = t_tw.project.get_id(filters)
        if id_list:
            cgt_variants = t_tw.project.get(id_list, t_tw.project.fields())[0]
            return self._root._new_entity_fnc(
                entity_cls,
                dict(
                    root=self._variants['root'],
                    project=name,
                    #
                    entity_name=cgt_variants['project.entity'],
                    entity_name_chs=cgt_variants.get('project.full_name')
                ),
                cgt_variants
            )
