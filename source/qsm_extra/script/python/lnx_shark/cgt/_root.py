# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _user

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

    def _new_entity_fnc(self, entity_class, variants, cgt_variants):
        variants = _cor_base.EntityVariantKeyFnc.clean_fnc(variants)

        entity_type = entity_class.Type
        path = self.to_entity_path(entity_type, variants)
        if self._root_entity_stack.exists(path):
            return self._root_entity_stack.get(path)

        entity = entity_class(
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
                self._new_entity_fnc(
                    _user.User,
                    dict(
                        cgt_user=i_cgt_variants['account.entity'],
                        # todo: add field to save login user name
                        user=i_cgt_variants['account.entity'],
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
            return self._new_entity_fnc(
                _user.User,
                dict(
                    cgt_user=name,
                    user=None
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
                self._new_entity_fnc(
                    _project.Project,
                    dict(
                        project=i_cgt_variants['project.entity']
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def project(self, name, **kwargs):
        t_tw = self._stage._api

        filters = [['project.entity', '=', name]]
        id_list = t_tw.project.get_id(filters)
        if id_list:
            cgt_variants = t_tw.project.get(id_list, t_tw.project.fields())[0]
            return self._new_entity_fnc(
                _project.Project,
                dict(
                    project=name
                ),
                cgt_variants
            )
