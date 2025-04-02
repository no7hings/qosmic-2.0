# coding:utf-8
import os

import copy

import json

import collections

import six

import lxbasic.resource as bsc_resource

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin

from . import _abc_


class _Entity(_abc_.AbsEntity):
    def __init__(self, *args, **kwargs):
        super(_Entity, self).__init__(*args, **kwargs)


class Stage(_abc_.AbsBase):
    class Roots:
        """
        virtual value, real value is from configure.
        """
        disorder = None
        source = None
        release = None
        temporary = None
        all = []

    class Spaces:
        """
        virtual value, real value is from configure.
        """
        disorder = None
        source = None
        release = None
        temporary = None
        all = []

    class Steps:
        """
        virtual value, real value is from configure.
        """
        general = None
        model = None
        groom = None
        cfx = None
        animation = None
        all = []

    class Tasks:
        """
        virtual value, real value is from configure.
        """
        model = None
        groom = None
        cfx_rig = None
        animation = None
        all = []

    INSTANCE_DICT = dict()

    ENTITY_DICT = dict()
    ENTITY_PATH_QUERY = dict()
    
    SYNC_FLAG = True

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        scheme = kwargs.get('scheme', 'default')
        if scheme in cls.INSTANCE_DICT:
            return cls.INSTANCE_DICT[scheme]

        self = super(Stage, cls).__new__(cls)

        self._scheme = scheme
        self._platform = bsc_core.BscPlatform.get_current()

        self._configure = bsc_resource.BscExtendConfigure.get_as_content('shark/parse/{}'.format(self._scheme))
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

        # load from configure as default, maybe load from database

        # root
        root_dict = self._configure.get('roots')
        self.Roots = type('Roots', (), dict(all=[]))()
        for i_key in self.RootKeys.All:
            if i_key not in root_dict:
                raise RuntimeError()
            i_root = root_dict[i_key][self._platform]
            if i_root not in self.Roots.all:
                self.Roots.all.append(i_root)
            self.Roots.__dict__[i_key] = i_root

        # space
        space_dict = self._configure.get('spaces')
        self.Spaces = type('Spaces', (), dict(all=[]))()
        for i_key in self.SpaceKeys.All:
            if i_key not in space_dict:
                raise RuntimeError()
            i_space = space_dict[i_key]
            if i_space not in self.Spaces.all:
                self.Spaces.all.append(i_space)
            self.Spaces.__dict__[i_key] = i_space

        # step
        step_dict = self._configure.get('steps')
        self.Steps = type('Steps', (), dict(all=[]))()
        for i_key in self.StepKeys.All:
            if i_key not in step_dict:
                raise RuntimeError()
            i_step = step_dict[i_key]
            if i_step not in self.Steps.all:
                self.Steps.all.append(i_step)
            self.Steps.__dict__[i_key] = i_step

        # task
        task_dict = self._configure.get('tasks')
        self.Tasks = type('Tasks', (), dict(all=[]))()
        for i_key in self.TaskKeys.All:
            if i_key not in task_dict:
                raise RuntimeError()
            i_task = task_dict[i_key]
            if i_task not in self.Tasks.all:
                self.Tasks.all.append(i_task)
            self.Tasks.__dict__[i_key] = i_task

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

    @property
    def configure(self):
        return self._configure

    def generate_pattern_opt_for(self, keyword, **kwargs):
        kwargs_new = copy.copy(kwargs)
        _ = keyword.split('-')
        kwargs_new.update(**self._variants)
        resource_type = _[0]
        kwargs_new['resource_type'] = resource_type
        space_key = _[1]
        kwargs_new['space_key'] = space_key
        space = self._to_space(space_key)
        kwargs_new['space'] = space

        key = 'patterns.{}.{}.{}'.format(
            resource_type, space, '-'.join(_[2:])
        )
        ptn = self._configure.get(key)
        if ptn:
            return bsc_core.BscTaskParseOpt(
                ptn
            ).update_variants_to(**kwargs_new)
        else:
            raise RuntimeError(
                'pattern: {} is not found.'.format(keyword)
            )

    def generate_wsp_task_paths(self, resource_type):
        list_ = []
        _ = self._configure.get(
            'workspace.tasks.{}'.format(resource_type)
        )
        step_dict = self._configure.get(
            'steps'
        )
        task_dict = self._configure.get(
            'tasks'
        )
        for i_step_key, i_task_keys in _.items():
            i_step = step_dict[i_step_key]
            for j_task_key in i_task_keys:
                j_task = task_dict[j_task_key]
                list_.append(
                    '/{}/{}'.format(i_step, j_task)
                )
        return list_

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
                variants[k] = bsc_pinyin.Text.cleanup(v, stop_on_chs=True)
        return variants

    def _to_space(self, space_key):
        return self._configure.get(
            'spaces.{}'.format(space_key)
        )

    # task
    def _get_task_pattern(self, resource_type, space_key):
        return self._configure.get(
            'patterns.{}.{}.task-dir'.format(resource_type, space_key)
        )

    # version
    def _get_version_pattern(self, resource_type, space_key):
        return self._configure.get(
            'patterns.{}.{}.version-dir'.format(resource_type, space_key)
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
            i_s = u'"{}": "{}"'.format(i_key, bsc_core.ensure_unicode(i_value))
            ss.append(i_s)

        return u'{{{}}}'.format(
            u', '.join(ss)
        )

    def _to_entity_path(self, entity_type, variants):
        pattern = self._get_entity_path_pattern(entity_type)
        pattern = bsc_core.ensure_unicode(pattern)
        if pattern is None:
            raise RuntimeError(
                self.stderr(
                    'path pattern is not found: {}.'.format(entity_type)
                )
            )
        return pattern.format(
            **variants
        )

    def _to_entity_variants(self, entity_pre, entity_type, name, entity_variants):
        variant_key = self._get_entity_variant_key(entity_type)
        entity_variants_new = dict(**entity_pre._variants)
        entity_variants_new.update(entity_variants)
        entity_variants_new[variant_key] = name
        return entity_variants_new

    def _generate_entity_args(self, entity_pre, entity_type, name, entity_variants):
        entity_variants_new = self._to_entity_variants(entity_pre, entity_type, name, entity_variants)
        entity_key = self._to_entity_key(entity_type, entity_variants_new)
        return entity_key, entity_variants_new

    # find entity
    def _find_entity_fnc(self, entity_pre, entity_type, name, **variants):
        entity_key, entity_variants = self._generate_entity_args(
            entity_pre, entity_type, name, variants
        )
        if entity_key in self.ENTITY_DICT:
            instance = self.ENTITY_DICT[entity_key]
            # kwargs = {}
            # keys = ['space_key']
            # for i in keys:
            #     if i in variants:
            #         kwargs[i] = variants[i]
            # instance.update_variants(
            #     **kwargs
            # )
            return instance

        if entity_type == self.EntityTypes.Task:
            flag, entity_variants_next = self._resolve_task_variants_from_storage(entity_pre, entity_variants)
        elif entity_type == self.EntityTypes.Version:
            flag, entity_variants_next = self._resolve_version_variants_from_storage(entity_pre, entity_variants)
        else:
            flag, entity_variants_next = self._resolve_entity_variants_from_storage(entity_type, entity_variants)

        if flag is True:
            instance = _Entity(self, entity_type, entity_variants_next)
            self.ENTITY_DICT[entity_key] = instance
            self.ENTITY_PATH_QUERY[instance.path] = instance
            return instance

    # entity
    @classmethod
    def _entity_variants_prc(cls, entity_variants, variant_key):
        entity_variants.pop('result')
        entity_variants.pop('pattern')
        entity_variants['resource_type'] = variant_key
        return entity_variants

    def _resolve_entity_variants_from_storage(self, entity_type, entity_variants):
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
                    i_entity_variants = dict(entity_variants)
                    i_entity_variants.update(i_matches[0])
                    return True, self._entity_variants_prc(i_entity_variants, variant_key)
        # when not patterns, may pattern is empty.
        else:
            if patterns is None:
                self.stderr('resolve pattern is not found for: {} at {}.'.format(entity_type, space_key))
                return False, {}
            return True, {}
        return False, {}

    # task
    @classmethod
    def _task_variants_prc(cls, entity_variants, variant_key):
        entity_variants.pop('result')
        entity_variants.pop('pattern')
        # add resource variant here, for version naming
        entity_variants['resource'] = entity_variants[entity_variants['resource_type']]
        return entity_variants

    def _resolve_task_variants_from_storage(self, entity_pre, entity_variants):
        resource_type = entity_pre.variants.resource_type
        # default is source
        space_key = entity_variants.get('space_key', self.SpaceKeys.Source)
        # override space variant
        entity_variants['space'] = self._to_space(space_key)
        pattern = self._get_task_pattern(resource_type, space_key)
        if pattern:
            patterns = [pattern]
            regex_dict = self._get_variant_regex_dict()
            for i_p in patterns:
                i_p_opt = bsc_core.BscStgParseOpt(i_p)
                i_p_opt.set_regex_dict(regex_dict)
                i_p_opt.update_variants(**entity_variants)
                i_matches = i_p_opt.find_matches()
                if i_matches:
                    i_entity_variants = dict(entity_variants)
                    i_entity_variants.update(i_matches[0])
                    return True, self._task_variants_prc(i_entity_variants, None)
        return False, {}

    # version
    @classmethod
    def _version_variants_prc(cls, entity_variants, variant_key):
        entity_variants.pop('result')
        entity_variants.pop('pattern')
        # add resource variant here, for version naming
        entity_variants['resource'] = entity_variants[entity_variants['resource_type']]
        return entity_variants

    def _resolve_version_variants_from_storage(self, entity_pre, entity_variants):
        resource_type = entity_pre.variants.resource_type
        # version space key default is release
        space_key = entity_variants.get('space_key', self.SpaceKeys.Release)
        # override space variant
        entity_variants['space'] = self._to_space(space_key)
        pattern = self._get_version_pattern(resource_type, space_key)
        if pattern:
            patterns = [pattern]
            regex_dict = self._get_variant_regex_dict()
            for i_p in patterns:
                i_p_opt = bsc_core.BscStgParseOpt(i_p)
                i_p_opt.set_regex_dict(regex_dict)
                i_p_opt.update_variants(**entity_variants)
                i_matches = i_p_opt.find_matches()
                if i_matches:
                    i_entity_variants = dict(entity_variants)
                    i_entity_variants.update(i_matches[0])
                    return True, self._version_variants_prc(i_entity_variants, None)
        return False, {}

    def _to_entity_variants_parse(self, entity_pre, entity_type, **variants):
        variant_key = self._get_entity_variant_key(entity_type)
        # copy from pre
        variants_new = dict(**entity_pre._variants)
        variants_new.update(**variants)
        # fixme: remove current entity's key?
        if variant_key in variants_new:
            variant = variants_new[variant_key]
            if isinstance(variant, six.string_types):
                variants_new.pop(variant_key)
        return variants_new

    # find entity task
    def _find_entity_task_fnc(self, entity, task):
        pass

    @classmethod
    def _generate_next_entities_cache_path(cls, entity_key, entity_type):
        location = bsc_core.BscEnviron.get_cache_qosmic_root()
        # keep order
        data = json.loads(entity_key, object_pairs_hook=collections.OrderedDict)
        key = '/'.join(['{}={}'.format(k, v) for k, v in data.items()])
        return '{}/parse/{}/{}.json'.format(location, key, entity_type)

    @classmethod
    def _generate_next_entities_cache_key(cls, entity_type, entity_variants):
        variants = copy.copy(entity_variants)
        variants['entity_type'] = entity_type
        return bsc_core.BscHash.to_hash_key(variants)

    @classmethod
    def _generate_next_entities_cache_path_(cls, cache_key):
        location = bsc_core.BscEnviron.get_cache_qosmic_root()
        return '{}/parse/{}.json'.format(location, cache_key)

    @classmethod
    def _pull_next_entities_sync_cache(cls, entity_type, entity_variants):
        # save cache on server for share
        cache_key = cls._generate_next_entities_cache_key(entity_type, entity_variants)
        cache_path = cls._generate_next_entities_cache_path_(cache_key)
        data = bsc_storage.StgFileOpt(cache_path).set_read()
        if data:
            return data.get(
                'next_entities', []
            )
        return []

    @classmethod
    def _push_next_entities_sync_cache(cls, entity_type, next_entity_variants_list, entity_variants):
        cache_key = cls._generate_next_entities_cache_key(entity_type, entity_variants)
        cache_path = cls._generate_next_entities_cache_path_(cache_key)
        if next_entity_variants_list:
            data = dict(
                entity=entity_variants,
                next_entities=next_entity_variants_list
            )
            bsc_storage.StgFileOpt(cache_path).set_write(data)
        else:
            # when cache is empty, remove exists cache
            if os.path.isfile(cache_path):
                # noinspection PyBroadException
                try:
                    os.remove(cache_path)
                except Exception:
                    pass

    @classmethod
    def _get_sync_flag(cls, **kwargs):
        # flag for sync, default is False
        if 'sync_flag' in kwargs:
            sync_flag = kwargs.pop('sync_flag')
            return sync_flag, kwargs
        return False, kwargs

    def _find_next_entity_variants(self, entity_pre, entity_type, **variants):
        sync_flag, variants = self._get_sync_flag(**variants)

        entity_variants = self._to_entity_variants_parse(entity_pre, entity_type, **variants)

        # task
        if entity_type == self.EntityTypes.Task:
            next_entity_variants_list = self._task_next_entity_variants_list_gain_fnc(
                entity_pre, entity_type, entity_variants, sync_flag
            )
        # version
        elif entity_type == self.EntityTypes.Version:
            next_entity_variants_list = self._version_next_entity_variants_list_gain_fnc(
                entity_pre, entity_type, entity_variants, sync_flag
            )
        # other entity
        else:
            next_entity_variants_list = self._any_entity_next_entity_variants_list_gain_fnc(
                entity_type, entity_variants, sync_flag
            )

        return next_entity_variants_list

    # find entities
    def _find_entities_fnc(self, entity_pre, entity_type, **variants):
        list_ = []
        keys = ['space_key']

        next_entity_variants_list = self._find_next_entity_variants(entity_pre, entity_type, **variants)

        for i_entity_variants in next_entity_variants_list:
            i_entity_variants = self._variant_cleanup_fnc(i_entity_variants)
            i_entity_key = self._to_entity_key(entity_type, i_entity_variants)
            # todo: when variants is changed, update variants?
            if i_entity_key in self.ENTITY_DICT:
                i_instance = self.ENTITY_DICT[i_entity_key]
                # i_kwargs = {}
                # for j in keys:
                #     if j in variants:
                #         i_kwargs[j] = variants[j]
                list_.append(i_instance)
                continue

            i_instance = _Entity(self, entity_type, i_entity_variants)
            self.ENTITY_DICT[i_entity_key] = i_instance
            self.ENTITY_PATH_QUERY[i_instance.path] = i_instance
            list_.append(i_instance)
        return list_

    @classmethod
    def _next_entity_variants_list_sync_fnc(
        cls,
        pattern,
        entity_type, entity_variants,
        variant_key, regex_dict,
        entity_variant_prc,
        sync_flag
    ):
        if sync_flag is False:
            next_entity_variants_list = cls._pull_next_entities_sync_cache(entity_type, entity_variants)
            # when has results, ignore scan
            if next_entity_variants_list:
                return next_entity_variants_list

        next_entity_variants_list = []

        p_opt = bsc_core.BscStgParseOpt(pattern)
        p_opt.set_regex_dict(regex_dict)
        p_opt.update_variants(**entity_variants)
        matches = p_opt.find_matches(sort=True)
        for i_match in matches:
            i_entity_variants_next = dict(entity_variants)
            i_entity_variants_next.update(i_match)
            next_entity_variants_list.append(entity_variant_prc(i_entity_variants_next, variant_key))

        cls._push_next_entities_sync_cache(entity_type, next_entity_variants_list, entity_variants)
        return next_entity_variants_list

    # any entities
    def _any_entity_next_entity_variants_list_gain_fnc(self, entity_type, entity_variants, sync_flag):
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
                i_entity_variants_list = i_p_opt.generate_combination_variants(entity_variants)
                for j_entity_variants in i_entity_variants_list:
                    j_next_entity_variants_list = self._next_entity_variants_list_sync_fnc(
                        i_p,
                        entity_type, j_entity_variants,
                        variant_key, regex_dict,
                        self._entity_variants_prc,
                        sync_flag
                    )
                    list_.extend(j_next_entity_variants_list)
        else:
            if patterns is None:
                self.stderr('resolve pattern is not found: {}.'.format(entity_type))
        return list_

    # tasks
    def _task_next_entity_variants_list_gain_fnc(self, entity_pre, entity_type, entity_variants, sync_flag):
        list_ = []
        resource_type = entity_pre.variants.resource_type
        # default is source
        space_key = entity_variants.get('space_key', self.SpaceKeys.Source)
        # override space variant
        entity_variants['space'] = self._to_space(space_key)
        pattern = self._get_task_pattern(resource_type, space_key)
        if pattern:
            patterns = [pattern]
            variant_key = self._get_entity_variant_key(entity_type)
            regex_dict = self._get_variant_regex_dict()
            for i_p in patterns:
                i_p_opt = bsc_core.BscStgParseOpt(i_p)
                i_p_opt.set_regex_dict(regex_dict)
                i_entity_variants_list = i_p_opt.generate_combination_variants(entity_variants)
                for j_entity_variants in i_entity_variants_list:
                    j_next_entity_variants_list = self._next_entity_variants_list_sync_fnc(
                        i_p,
                        entity_type, j_entity_variants,
                        variant_key, regex_dict,
                        self._task_variants_prc,
                        sync_flag
                    )
                    list_.extend(j_next_entity_variants_list)
        return list_

    # versions
    def _version_next_entity_variants_list_gain_fnc(self, entity_pre, entity_type, entity_variants, sync_flag):
        list_ = []
        resource_type = entity_pre.variants.resource_type
        # default is release
        space_key = entity_variants.get('space_key', self.SpaceKeys.Release)
        # override space variant
        entity_variants['space'] = self._to_space(space_key)
        pattern = self._get_version_pattern(resource_type, space_key)
        if pattern:
            patterns = [pattern]
            variant_key = self._get_entity_variant_key(entity_type)
            regex_dict = self._get_variant_regex_dict()
            for i_p in patterns:
                i_p_opt = bsc_core.BscStgParseOpt(i_p)
                i_p_opt.set_regex_dict(regex_dict)
                # support for variant is multiply, etc. project=["QSM_TST", "QSM_TST_NEW"]
                i_entity_variants_list = i_p_opt.generate_combination_variants(entity_variants)
                for j_entity_variants in i_entity_variants_list:
                    j_next_entity_variants_list = self._next_entity_variants_list_sync_fnc(
                        i_p,
                        entity_type, j_entity_variants,
                        variant_key, regex_dict,
                        self._version_variants_prc,
                        sync_flag
                    )
                    list_.extend(j_next_entity_variants_list)
        return list_

    # any entity
    def find_entity(self, entity_type, name, **kwargs):
        """
        entity_type includes see self.EntityTypes, kwargs is variants
        """
        return self._find_entity_fnc(
            self, entity_type, name, **kwargs
        )

    def find_entities(self, entity_type, **kwargs):
        """
        entity_type includes see self.EntityTypes
        """
        return self._find_entities_fnc(
            self, entity_type, **kwargs
        )

    # project
    def project(self, name, **kwargs):
        return self.find_entity(
            self.EntityTypes.Project, name, **kwargs
        )

    def projects(self, **variants):
        return self.find_entities(
            self.EntityTypes.Project, **variants
        )

    def all(self):
        return self.ENTITY_DICT.values()

    def get_one(self, entity_key):
        return self.ENTITY_DICT.get(entity_key)

    def get_entity(self, path):
        return self.ENTITY_PATH_QUERY.get(path)

    def restore(self):
        return self.ENTITY_DICT.clear()
