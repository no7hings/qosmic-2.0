# coding:utf-8
import json

import hashlib

import collections

import lxbasic.resource as bsc_resource

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin

import _abc


class Entity(_abc.AbsEntity):
    def __init__(self, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)


class Stage(_abc.AbsBase):

    INSTANCE_DICT = dict()

    ENTITY_DICT = dict()
    NEXT_ENTITIES_DICT = dict()

    def __new__(cls, *args, **kwargs):
        scheme = kwargs.get('scheme', 'default')
        if scheme in cls.INSTANCE_DICT:
            return cls.INSTANCE_DICT[scheme]

        self = super(Stage, cls).__new__(cls, *args, **kwargs)
        self._scheme = scheme
        self._platform = bsc_core.BscPlatform.get_current()
        self._configure = bsc_resource.RscExtendConfigure.get_as_content('wsp_task/parse/{}'.format(self._scheme))
        self._configure.do_flatten()
        self._variants = dict(
            scheme=self._scheme,
            platform=self._platform
        )
        for k, v in self._configure.get('roots').items():
            i_location = v[self._platform]
            self._variants['root_{}'.format(k)] = i_location

        self._entity_key = '{{"stage": "{}"}}'.format(scheme)
        self._cleanup_variant_keys = self._configure.get('variants.cleanup_keys')

        cls.INSTANCE_DICT[scheme] = self
        return self

    @property
    def scheme(self):
        return self._scheme

    @property
    def platform(self):
        return self._platform

    @property
    def variants(self):
        return self._variants

    def _get_variant_regex_dict(self):
        return self._configure.get(
            'variants.regex'
        )

    def _get_entity_unique_variant_keys(self, entity_type):
        return self._configure.get(
            'entities.unique_variant_keys.{}'.format(entity_type)
        )

    def _get_entity_variant_key(self, entity_type):
        return self._configure.get(
            'entities.variant_key.{}'.format(entity_type)
        )

    def _get_entity_path_pattern(self, entity_type):
        return self._configure.get(
            'entities.path_pattern.{}'.format(entity_type)
        )

    def _get_entity_resolve_patterns(self, entity_type, space_key):
        return self._configure.get(
            'entities.resolve_patterns.{}.{}'.format(entity_type, space_key)
        )

    def _get_entity_next_method_data(self, entity_type):
        return self._configure.get(
            'entities.next_methods.{}'.format(entity_type)
        ) or {}

    def _get_entity_pattern(self, entity_type, space_key):
        variant_key = self._get_entity_variant_key(entity_type)
        return self._configure.get(
            'patterns.{}.{}.dir'.format(variant_key, space_key)
        )

    # clear up items chinese word
    def _variant_cleanup_fnc(self, variants):
        for k, v in variants.items():
            if k in self._cleanup_variant_keys:
                variants[k] = bsc_pinyin.Text.cleanup(v)
        return variants

    def _to_space(self, space_key):
        return self._configure.get(
            'spaces.{}'.format(space_key)
        )

    # task
    def _get_entity_task_pattern(self, resource_branch, space_key):
        return self._configure.get(
            'patterns.{}.{}.task-dir'.format(resource_branch, space_key)
        )

    # version
    def _get_entity_version_pattern(self, resource_branch, space_key):
        return self._configure.get(
            'patterns.{}.{}.version-dir'.format(resource_branch, space_key)
        )

    def _to_entity_key(self, entity_type, variants):
        keys = self._get_entity_unique_variant_keys(entity_type)
        keys_unpack = []
        ss = []
        for i_key in keys:
            i_value = variants[i_key]
            if i_key == 'entity_key':
                # keep order
                i_dict = json.loads(i_value, object_pairs_hook=collections.OrderedDict)
                i_keys = i_dict.keys()
                keys_unpack.extend(i_keys)
            else:
                keys_unpack.append(i_key)

        for i_key in keys_unpack:
            i_value = variants[i_key]
            i_s = u'"{}": "{}"'.format(i_key, self.ensure_unicode(i_value))
            ss.append(i_s)

        return u'{{{}}}'.format(
            u', '.join(ss)
        )

    def _to_entity_path(self, entity_type, variants):
        pattern = self._get_entity_path_pattern(entity_type)
        pattern = self.ensure_unicode(pattern)
        if pattern is None:
            raise RuntimeError(
                self.stderr(
                    'path pattern is not found: {}.'.format(entity_type)
                )
            )
        return pattern.format(
            **variants
        )

    def _to_entity_variants(self, entity_pre, entity_type, name, **variants):
        variant_key = self._get_entity_variant_key(entity_type)
        variants_new = dict(**entity_pre._variants)
        variants_new.update(variants)
        variants_new[variant_key] = name
        return variants_new

    def _generate_entity_args(self, entity_pre, entity_type, name, **variants):
        entity_variants = self._to_entity_variants(entity_pre, entity_type, name, **variants)
        entity_key = self._to_entity_key(entity_type, entity_variants)
        return entity_key, entity_variants

    # find entity
    def _find_entity(self, entity_pre, entity_type, name, **variants):
        entity_key, entity_variants = self._generate_entity_args(
            entity_pre, entity_type, name, **variants
        )
        if entity_key in self.ENTITY_DICT:
            return self.ENTITY_DICT[entity_key]

        if entity_type == self.EntityTypes.Task:
            flag, entity_variants_new = self._resolve_entity_task_from_storage(entity_pre, entity_variants)
        elif entity_type == self.EntityTypes.Version:
            flag, entity_variants_new = self._resolve_entity_version_from_storage(entity_pre, entity_variants)
        else:
            flag, entity_variants_new = self._resolve_entity_from_storage(entity_type, entity_variants)

        if flag is True:
            entity_variants.update(entity_variants_new)
            instance = Entity(self, entity_type, entity_variants)
            self.ENTITY_DICT[entity_key] = instance
            return instance

    def _resolve_entity_from_storage(self, entity_type, entity_variants):
        # default is source
        space_key = entity_variants.get('space_key', self.SpaceKeys.Source)
        entity_variants['space'] = self._to_space(space_key)
        patterns = self._get_entity_resolve_patterns(entity_type, space_key)
        if patterns:
            variant_key = self._get_entity_variant_key(entity_type)
            regex_dict = self._get_variant_regex_dict()
            for i_p in patterns:
                i_p_opt = bsc_core.BscStgParseOpt(i_p)
                i_p_opt.set_regex_dict(regex_dict)
                i_p_opt.update_variants(**entity_variants)
                i_matches = i_p_opt.find_matches()
                if i_matches:
                    i_entity_variants = i_matches[0]
                    i_entity_variants.pop('result')
                    i_entity_variants.pop('pattern')
                    i_entity_variants['resource_branch'] = variant_key
                    return True, i_entity_variants
        else:
            if patterns is None:
                self.stderr('resolve pattern is not found for: {} at {}.'.format(entity_type, space_key))
                return False, {}
            return True, {}
        return False, {}

    def _resolve_entity_task_from_storage(self, entity_pre, entity_variants):
        resource_branch = entity_pre.variants.resource_branch
        # default is source
        space_key = entity_variants.get('space_key', self.SpaceKeys.Source)
        # override space variant
        entity_variants['space'] = self._to_space(space_key)
        pattern = self._get_entity_task_pattern(resource_branch, space_key)
        if pattern:
            patterns = [pattern]
            regex_dict = self._get_variant_regex_dict()
            for i_p in patterns:
                i_p_opt = bsc_core.BscStgParseOpt(i_p)
                i_p_opt.set_regex_dict(regex_dict)
                i_p_opt.update_variants(**entity_variants)
                i_matches = i_p_opt.find_matches()
                if i_matches:
                    i_entity_variants = i_matches[0]
                    i_entity_variants.pop('result')
                    i_entity_variants.pop('pattern')
                    return True, i_entity_variants
        return False, {}

    def _resolve_entity_version_from_storage(self, entity_pre, entity_variants):
        resource_branch = entity_pre.variants.resource_branch
        # default is release
        space_key = entity_variants.get('space_key', self.SpaceKeys.Release)
        # override space variant
        entity_variants['space'] = self._to_space(space_key)
        pattern = self._get_entity_version_pattern(resource_branch, space_key)
        if pattern:
            patterns = [pattern]
            regex_dict = self._get_variant_regex_dict()
            for i_p in patterns:
                i_p_opt = bsc_core.BscStgParseOpt(i_p)
                i_p_opt.set_regex_dict(regex_dict)
                i_p_opt.update_variants(**entity_variants)
                i_matches = i_p_opt.find_matches()
                if i_matches:
                    i_entity_variants = i_matches[0]
                    i_entity_variants.pop('result')
                    i_entity_variants.pop('pattern')
                    return True, i_entity_variants
        return False, {}

    def _to_entity_variants_many(self, entity_pre, entity_type, **variants):
        variant_key = self._get_entity_variant_key(entity_type)
        variants_new = dict(**entity_pre._variants)
        variants_new.update(**variants)
        if variant_key in variants_new:
            variants_new.pop(variant_key)
        return variants_new

    # find entity task
    def _find_entity_task(self, entity, task):
        pass

    def _generate_next_entities_cache_key(self, entity_key, entity_type):
        return

    @classmethod
    def _generate_next_entities_cache_path(cls, entity_key, entity_type):
        location = bsc_core.BscEnviron.get_cache_qosmic_root()
        # keep order
        data = json.loads(entity_key, object_pairs_hook=collections.OrderedDict)
        key = '/'.join(['{}={}'.format(k, v) for k, v in data.items()])
        return '{}/parse/{}/{}.json'.format(location, key, entity_type)

    @classmethod
    def _pull_next_entities_sync_cache(cls, entity_pre, entity_type):
        cache_path = cls._generate_next_entities_cache_path(entity_pre._entity_key, entity_type)
        data = bsc_storage.StgFileOpt(cache_path).set_read()
        if data:
            return data.get('next_entities', [])
        return []

    def _push_next_entities_sync_cache(self, entity_pre, entity_type, variants_list):
        data = dict(
            entity=entity_pre._variants,
            next_entities=variants_list
        )
        cache_path = self._generate_next_entities_cache_path(entity_pre._entity_key, entity_type)
        bsc_storage.StgFileOpt(cache_path).set_write(data)

    # find entities
    def _find_entities(self, entity_pre, entity_type, **variants):
        list_ = []
        
        cache_flag = variants.get('cache_flag', True)

        sync_cache_flag = variants.get('sync_cache_flag', True)
        if sync_cache_flag is True:
            entity_variants_list = self._pull_next_entities_sync_cache(entity_pre, entity_type)
        else:
            entity_variants = self._to_entity_variants_many(entity_pre, entity_type, **variants)
            if entity_type == self.EntityTypes.Task:
                entity_variants_list = self._resolve_entity_tasks_from_storage(entity_pre, entity_variants)
            elif entity_type == self.EntityTypes.Version:
                entity_variants_list = self._resolve_entity_versions_from_storage(entity_pre, entity_variants)
            else:
                entity_variants_list = self._resolve_entities_from_storage(entity_type, entity_variants)

            self._push_next_entities_sync_cache(entity_pre, entity_type, entity_variants_list)

        for i_entity_variants in entity_variants_list:
            i_entity_variants = self._variant_cleanup_fnc(i_entity_variants)
            i_entity_key = self._to_entity_key(entity_type, i_entity_variants)
            if i_entity_key in self.ENTITY_DICT:
                list_.append(self.ENTITY_DICT[i_entity_key])
                continue

            i_instance = Entity(self, entity_type, i_entity_variants)
            self.ENTITY_DICT[i_entity_key] = i_instance
            list_.append(i_instance)
        return list_

    def _resolve_entities_from_storage(self, entity_type, entity_variants):
        list_ = []
        # default is source
        space_key = entity_variants.get('space_key', self.SpaceKeys.Source)
        entity_variants['space'] = self._to_space(space_key)
        patterns = self._get_entity_resolve_patterns(entity_type, space_key)
        if patterns:
            variant_key = self._get_entity_variant_key(entity_type)
            regex_dict = self._get_variant_regex_dict()
            for i_p in patterns:
                i_p_opt = bsc_core.BscStgParseOpt(i_p)
                i_p_opt.set_regex_dict(regex_dict)
                i_p_opt.update_variants(**entity_variants)
                i_matches = i_p_opt.find_matches(sort=True)
                if i_matches:
                    for i_match in i_matches:
                        i_entity_varints = dict(entity_variants)
                        i_match.pop('result')
                        i_match.pop('pattern')
                        i_entity_varints.update(i_match)
                        i_entity_varints['resource_branch'] = variant_key
                        list_.append(i_entity_varints)
        else:
            if patterns is None:
                self.stderr('resolve pattern is not found: {}.'.format(entity_type))
        return list_

    def _resolve_entity_tasks_from_storage(self, entity_pre, entity_variants):
        list_ = []
        resource_branch = entity_pre.variants.resource_branch
        # default is source
        space_key = entity_variants.get('space_key', self.SpaceKeys.Source)
        # override space variant
        entity_variants['space'] = self._to_space(space_key)
        pattern = self._get_entity_task_pattern(resource_branch, space_key)
        if pattern:
            patterns = [pattern]
            regex_dict = self._get_variant_regex_dict()
            for i_p in patterns:
                i_p_opt = bsc_core.BscStgParseOpt(i_p)
                i_p_opt.set_regex_dict(regex_dict)
                i_p_opt.update_variants(**entity_variants)
                i_matches = i_p_opt.find_matches(sort=True)
                for i_match in i_matches:
                    i_entity_varints = dict(entity_variants)
                    i_match.pop('result')
                    i_match.pop('pattern')
                    i_entity_varints.update(i_match)
                    list_.append(i_entity_varints)
        return list_

    def _resolve_entity_versions_from_storage(self, entity_pre, entity_variants):
        list_ = []
        resource_branch = entity_pre.variants.resource_branch
        # default is release
        space_key = entity_variants.get('space_key', self.SpaceKeys.Release)
        # override space variant
        entity_variants['space'] = self._to_space(space_key)
        pattern = self._get_entity_version_pattern(resource_branch, space_key)
        if pattern:
            patterns = [pattern]
            regex_dict = self._get_variant_regex_dict()
            for i_p in patterns:
                i_p_opt = bsc_core.BscStgParseOpt(i_p)
                i_p_opt.set_regex_dict(regex_dict)
                i_p_opt.update_variants(**entity_variants)
                i_matches = i_p_opt.find_matches(sort=True)
                for i_match in i_matches:
                    i_entity_varints = dict(entity_variants)
                    i_match.pop('result')
                    i_match.pop('pattern')
                    i_entity_varints.update(i_match)
                    list_.append(i_entity_varints)
        return list_

    # project
    def project(self, name):
        return self._find_entity(
            self, self.EntityTypes.Project, name
        )

    def projects(self, **variants):
        return self._find_entities(
            self, self.EntityTypes.Project, **variants
        )

    # general
    def find_one(self, entity_type, name, **kwargs):
        return self._find_entity(
            self, entity_type, name, **kwargs
        )

    def find_all(self, entity_type, **kwargs):
        return self._find_entities(
            self, entity_type, **kwargs
        )

    def all(self):
        return self.ENTITY_DICT.values()

    def get_one(self, entity_key):
        return self.ENTITY_DICT.get(entity_key)

    def restore(self):
        return self.ENTITY_DICT.clear()
