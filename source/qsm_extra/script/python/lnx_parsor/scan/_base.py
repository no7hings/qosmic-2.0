# coding:utf-8
import copy

import json

import six

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from ..core import base as _cor_base


class AbsEntity(_cor_base.AbsEntityBase):
    NextEntitiesGeneratorClsDict = dict()

    TasksGeneratorCls = None

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return True

    @classmethod
    def _generate_next_entities_cache_key(cls, entity_type, variants, variants_extend=None):
        variants = copy.copy(variants)
        variants['entity_type'] = entity_type
        if variants_extend:
            variants.update(variants_extend)
        return bsc_core.BscHash.to_hash_key(variants)

    @classmethod
    def _generate_next_entities_cache_path(cls, cache_key):
        location = bsc_core.BscEnviron.get_cache_qosmic_root()
        return '{}/scan/{}.json'.format(location, cache_key)

    @classmethod
    def _pull_next_entities_sync_cache(cls, cache_key):
        cache_path = cls._generate_next_entities_cache_path(cache_key)
        data = bsc_storage.StgFileOpt(cache_path).set_read()
        if data:
            return data.get('next_entities', [])
        return []

    def _push_next_entities_sync_cache(self, cache_key, variants_list):
        data = dict(
            entity=self._variants,
            next_entities=variants_list
        )
        cache_path = self._generate_next_entities_cache_path(cache_key)
        bsc_storage.StgFileOpt(cache_path).set_write(data)

    def _generate_next_entities_generator(self, entity_type, variants_extend=None, cache_flag=True):
        # generate key by scan variant, when variants is changed, generate new variant
        variants = copy.copy(self._variants)

        cache_key = self._generate_next_entities_cache_key(entity_type, variants, variants_extend)

        # cache flag, when is True, use cache from dict
        if cache_flag is True:
            # when is created use exists
            if cache_key in self._next_entities_generator_dict:
                entities_cache_opt = self._next_entities_generator_dict[cache_key]
                return entities_cache_opt

        # sync cache flag, when is True, use cache from json
        if _cor_base.GlobalVar.SYNC_CACHE_FLAG is True:
            # when file cache is exists, use file cache
            variants_list = self._pull_next_entities_sync_cache(cache_key)
            if variants_list:
                entities_cache_opt = self.NextEntitiesGeneratorClsDict[entity_type](self._root, variants)
                entities_cache_opt.update_from_cache(variants_list)
                return entities_cache_opt

        entities_cache_opt = self.NextEntitiesGeneratorClsDict[entity_type](self._root, variants)
        variants_list = entities_cache_opt.update_from_storage(variants_extend, cache_flag)

        self._push_next_entities_sync_cache(cache_key, variants_list)

        bsc_log.Log.trace_result(
            'scan {} for: {}'.format(entity_type, bsc_core.ensure_string(self._entity_path))
        )

        self._next_entities_generator_dict[cache_key] = entities_cache_opt
        return entities_cache_opt

    def _find_next_entities(self, entity_type, variants_extend=None, cache_flag=True):
        entities_cache_opt = self._generate_next_entities_generator(entity_type, variants_extend, cache_flag)
        if variants_extend:
            return entities_cache_opt.find_all(variants_extend)
        return entities_cache_opt.get_all()

    def _find_next_entity(self, name, entity_type, variants_extend=None, cache_flag=True):
        entities_cache_opt = self._generate_next_entities_generator(entity_type, variants_extend, cache_flag)
        return entities_cache_opt.get(name)

    # evey entity has task, either project, asset, sequence, shot
    def _generate_tasks_cache_opt(self, variants_extend=None, cache_flag=True):
        if self._tasks_cache_opt is not None:
            return self._tasks_cache_opt

        variants = copy.copy(self._variants)
        _ = self.TasksGeneratorCls(self, variants)
        _.update_from_storage(variants_extend, cache_flag)
        self._tasks_cache_opt = _
        return _

    def __init__(self, root, path, variants, dtb_variants=None):
        self._root = root
        self._stage = self._root._stage
        self._root_entity_stack = root.entity_stack
        self._entity_path = path
        self._path_opt = bsc_core.BscNodePathOpt(self._entity_path)
        self._name = self._path_opt.get_name()
        self._variants = variants

        self._properties = _cor_base.EntityProperties(**variants)

        self._entity_type = self.Type
        self._variants['entity_type'] = self._entity_type
        self._variants['entity_path'] = self._entity_path

        self._dtb_variants = dtb_variants or {}

        self._next_entities_generator_dict = dict()
        self._tasks_cache_opt = None

    def __str__(self):
        return 'Entity({})'.format(
            json.dumps(self._variants, indent=4),
        )

    def __repr__(self):
        return self.__str__()

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
    def properties(self):
        return self._properties

    @property
    def variants(self):
        return self._variants

    @property
    def tasks(self):
        _ = self._generate_tasks_cache_opt()
        return _.get_all()

    def task(self, name):
        _ = self._generate_tasks_cache_opt()
        return _.get(name)


class AbsEntitiesGenerator(object):
    EntityClass = None

    def _generate_stg_ptn_opts(self):
        _ = _cor_base.DisorderConfig()._entity_resolve_pattern_dict[self.EntityClass.Type]
        if isinstance(_, list):
            ps = _
        else:
            ps = [_]

        list_ = []
        for i_p in ps:
            i_p_opt = bsc_core.BscStgParseOpt(i_p)
            i_p_opt.update_variants(**self._variants)
            list_.append(i_p_opt)
        return list_

    def __init__(self, root, variants):
        self._root = root
        self._root_entity_stack = root.entity_stack

        self._variants = {}
        self._variants.update(variants)

        # storage
        self._stg_ptn_opt_for_scan = bsc_core.BscStgParseOpt(
            _cor_base.DisorderConfig()._entity_resolve_pattern_dict[self.EntityClass.Type]
        )
        self._stg_ptn_opt_for_scan.update_variants(**self._variants)
        # path
        self._dcc_ptn_opt = bsc_core.BscDccParseOpt(
            _cor_base.DisorderConfig()._entity_path_pattern_dict[self.EntityClass.Type]
        )

        self._variants_list = []
        self._entity_variant_key = self.EntityClass.VariantKey

        self._entity_dict = {}

    def __str__(self):
        return str(self._entity_dict.values())

    def update_from_storage(self, variants_extend=None, cache_flag=True):
        if variants_extend:
            for k, v in variants_extend.items():
                # variant is one
                if isinstance(v, six.string_types):
                    i_variants = copy.copy(self._variants)
                    i_variants[k] = v
                    i_matchers = self.scan_fnc(i_variants)
                    for k_variant in i_matchers:
                        self._new_entity_fnc(k_variant)
                # variant is many
                elif isinstance(v, list):
                    for j in v:
                        j_variants = copy.copy(self._variants)
                        j_variants[k] = j
                        j_matchers = self.scan_fnc(j_variants)
                        for k_variant in j_matchers:
                            self._new_entity_fnc(k_variant)
                else:
                    raise RuntimeError()
        else:
            variants = copy.copy(self._variants)
            matches = self.scan_fnc(variants)
            for i_variants in matches:
                self._new_entity_fnc(i_variants)

        return self._variants_list

    def scan_fnc(self, variants):
        pth_opt = bsc_core.BscStgParseOpt(
            _cor_base.DisorderConfig()._entity_resolve_pattern_dict[self.EntityClass.Type]
        )
        pth_opt.update_variants(**variants)
        matchers = pth_opt.find_matches(sort=True)
        return matchers

    def _new_entity_fnc(self, variants):
        variants = _cor_base.EntityVariantKeyFnc.clean_fnc(variants)
        path = self._dcc_ptn_opt.update_variants_to(**variants).get_value()
        if path in self._entity_dict:
            return self._entity_dict[path]

        if self.EntityClass._variant_validation_fnc(variants) is True:
            variants['entity_name'] = variants[self.EntityClass.VariantKey]
            variants['entity_gui_name'] = None

            entity = self.EntityClass(self._root, path, variants)
            self._root_entity_stack.register(path, entity)
            self._variants_list.append(variants)
            self._entity_dict[path] = entity
            return entity

    def to_entity_path(self, name):
        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        return self._dcc_ptn_opt.update_variants_to(**variants).get_value()

    def update_from_cache(self, data):
        for i_variants in data:
            self._new_entity_fnc(i_variants)

    def get_all(self):
        return self._entity_dict.values()

    def find_all(self, variants_extend):
        list_ = []
        _ = self.get_all()
        for i in _:
            i_enables = []
            for j_k, j_v in variants_extend.items():
                if i.properties.get(j_k) in j_v:
                    i_enables.append(True)
                else:
                    i_enables.append(False)

            if sum(i_enables) == len(i_enables):
                list_.append(i)
        return list_

    def get(self, name):
        path = self.to_entity_path(name)
        if path in self._entity_dict:
            return self._entity_dict[path]

        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        ptn_opt = self._stg_ptn_opt_for_scan.update_variants_to(
            **variants
        )
        matches = ptn_opt.find_matches()
        if matches:
            variants_new = matches[0]
            return self._new_entity_fnc(variants_new)

    def exist(self, name):
        path = self.to_entity_path(name)
        return path in self._entity_dict


class AbsTask(_cor_base.AbsTaskBase):

    def __init__(self, *args, **kwargs):
        super(AbsTask, self).__init__(*args, **kwargs)


class AbsTasksGenerator(object):
    EntityClass = None

    def _generate_stg_ptn_opts(self):
        _ = _cor_base.DisorderConfig()._entity_resolve_pattern_dict[self.EntityClass.Type]
        if isinstance(_, list):
            ps = _
        else:
            ps = [_]

        list_ = []
        for i_p in ps:
            i_p_opt = bsc_core.BscStgParseOpt(i_p)
            i_p_opt.update_variants(**self._variants)
            list_.append(i_p_opt)
        return list_

    def __init__(self, entity, variants):
        self._entity = entity

        self._variants = {}
        self._variants.update(variants)
        key = '{}{}'.format(self._entity.Type, self.EntityClass.Type)
        self._stg_ptn_opt_for_scan = bsc_core.BscStgParseOpt(
            _cor_base.DisorderConfig()._entity_resolve_pattern_dict[key]
        )
        self._stg_ptn_opt_for_scan.update_variants(**self._variants)
        self._dcc_ptn_opt = bsc_core.BscDccParseOpt(
            _cor_base.DisorderConfig()._entity_path_pattern_dict[key]
        )

        self._entity_variant_key = self.EntityClass.VariantKey

        self._entity_dict = {}

    def update_from_storage(self, variants_extend=None, cache_flag=True):
        matches = self._stg_ptn_opt_for_scan.find_matches(sort=True)
        for i_variants in matches:
            self._new_task_fnc(i_variants)

    def _new_task_fnc(self, variants):
        path = self._dcc_ptn_opt.update_variants_to(**variants).get_value()
        entity = self.EntityClass(self._entity, path, variants)
        self._entity_dict[path] = entity
        return entity

    def to_entity_path(self, name):
        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        return self._dcc_ptn_opt.update_variants_to(**variants).get_value()

    def get_all(self):
        return self._entity_dict.values()

    def get(self, name):
        path = self.to_entity_path(name)
        if path in self._entity_dict:
            return self._entity_dict[path]

        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        ptn_opt = self._stg_ptn_opt_for_scan.update_variants_to(
            **variants
        )
        matches = ptn_opt.find_matches()
        if matches:
            variants_new = matches[0]
            return self._new_task_fnc(variants_new)


class EntityFactory:
    @staticmethod
    def find_all(entity_type):
        def decorator(fnc):
            def wrapper(self, **kwargs):
                # fnc(**kwargs)
                cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
                return self._find_next_entities(entity_type, variants_extend=kwargs, cache_flag=cache_flag)
            return wrapper
        return decorator

    @staticmethod
    def find_one(entity_type):
        def decorator(fnc):
            def wrapper(self, name, **kwargs):
                # fnc(**kwargs)
                cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
                return self._find_next_entity(name, entity_type, variants_extend=kwargs, cache_flag=cache_flag)
            return wrapper
        return decorator
