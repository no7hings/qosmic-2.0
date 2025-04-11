# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _people

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

    def _new_entity_fnc(self, entity_cls, variants, dtb_variants):
        variants = _cor_base.EntityVariantKeyFnc.clean_fnc(variants)

        path = self.to_entity_path(entity_cls.Type, variants)
        if self._root_entity_stack.exists(path):
            return self._root_entity_stack.get(path)

        entity = entity_cls(
            self._root, path, variants, dtb_variants
        )
        self._root_entity_stack.register(path, entity)
        return entity

    def current_user(self):
        t_tw = self._stage._api
        return self.user(
            name=t_tw.login.account()
        )

    def department(self, name, **kwargs):
        pass

    def departments(self, **kwargs):
        pass

    def users(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []
        if 'active' in kwargs:
            filters.append(['account.status', '=', 'Y'])

        for i_dtb_variants in t_tw.account.get(
            t_tw.account.get_id(filters),
            t_tw.account.fields()
        ):
            list_.append(
                self._root._new_entity_fnc(
                    _people.User,
                    dict(
                        cgt_user=i_dtb_variants['account.entity'],
                        # todo: add field to save login
                        user=i_dtb_variants.get('account.login'),
                        #
                        entity_name=i_dtb_variants['account.entity'],
                        entity_gui_name=i_dtb_variants['account.name'],
                    ),
                    i_dtb_variants
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
            dtb_variants = t_tw.account.get(id_list, t_tw.account.fields())[0]
            return self._root._new_entity_fnc(
                _people.User,
                dict(
                    user=name,
                    # todo: add field to save login
                    login=dtb_variants.get('account.login'),
                    #
                    entity_name=dtb_variants['account.entity'],
                    entity_gui_name=dtb_variants['account.name'],
                ),
                dtb_variants
            )

    def projects(self, **kwargs):
        t_tw = self._stage._api

        list_ = []

        filters = []
        if 'active' in kwargs:
            filters.append(['project.status', '=', 'Active'])

        for i_dtb_variants in t_tw.project.get(
            t_tw.project.get_id(filters),
            t_tw.project.fields()
        ):
            list_.append(
                self._root._new_entity_fnc(
                    _project.Project,
                    dict(
                        root=self._variants['root'],
                        project=i_dtb_variants['project.entity'],
                        #
                        entity_name=i_dtb_variants['project.entity'],
                        entity_gui_name=i_dtb_variants.get('project.full_name')
                    ),
                    i_dtb_variants
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
            dtb_variants = t_tw.project.get(id_list, t_tw.project.fields())[0]
            return self._root._new_entity_fnc(
                entity_cls,
                dict(
                    root=self._variants['root'],
                    project=name,
                    #
                    entity_name=dtb_variants['project.entity'],
                    entity_gui_name=dtb_variants.get('project.full_name')
                ),
                dtb_variants
            )
