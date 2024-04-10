# coding:utf-8
from __future__ import print_function

import six

import os

import re

import glob

import platform

import fnmatch

import parse

import collections

import copy

import threading

import lxcontent.core as ctt_core

import lxresource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxuniverse.abstracts as unr_abstracts
# resolver
from .. import core as rsv_core


class RsvThread(threading.Thread):
    THREAD_MAXIMUM = threading.Semaphore(1024)

    def __init__(self, fnc, *args, **kwargs):
        super(RsvThread, self).__init__()
        self._fnc = fnc
        self._args = args
        self._kwargs = kwargs
        #
        self._data = None

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def run(self):
        RsvThread.THREAD_MAXIMUM.acquire()
        self.set_data(
            self._fnc(*self._args, **self._kwargs)
        )
        RsvThread.THREAD_MAXIMUM.release()


class RsvConfigureOpt(object):
    PATHSEP = '.'

    PATTERN_REF_RE_PATTERN = r'[<](.*?)[>]'

    def __init__(self, dict_):
        self._dict = dict_
        self._keys_exclude = []

    def get_all_keys(self):
        def rcs_fnc_(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = '{}.{}'.format(k_, _k)
                else:
                    _key = _k
                #
                lis.append(_key)
                if isinstance(_v, dict):
                    rcs_fnc_(_key, _v)

        #
        lis = []
        rcs_fnc_(None, self._dict)
        return lis

    def get_keys(self, pattern=None):
        _ = self.get_all_keys()
        if pattern is not None:
            return fnmatch.filter(_, pattern)
        return _

    def get(self, key_path, default_value=None):
        ks = key_path.split(self.PATHSEP)
        v = self._dict
        for k in ks:
            if isinstance(v, dict):
                if k in v:
                    v = v[k]
                else:
                    return default_value
            else:
                return default_value
        return v

    def set(self, key_path, value):
        ks = key_path.split(self.PATHSEP)
        v = self._dict
        #
        maximum = len(ks)-1
        for seq, k in enumerate(ks):
            if seq == maximum:
                v[k] = value
            else:
                if k not in v:
                    v[k] = collections.OrderedDict()
                #
                v = v[k]

    def unfold_value(self, value):
        def rcs_fnc_(v_):
            if isinstance(v_, six.string_types):
                _r = v_
                _ks = re.findall(re.compile(self.PATTERN_REF_RE_PATTERN, re.S), v_)
                if _ks:
                    for _k in set(_ks):
                        if _k not in self._dict:
                            raise KeyError(u'keyword: "{}" is non-registered'.format(_k))
                        #
                        _v = self._dict[_k]
                        #
                        _v = rcs_fnc_(_v)
                        #
                        _r = _r.replace(u'<{}>'.format(_k), _v)
                return _r
            return v_

        return rcs_fnc_(value)

    def get_content_as_unfold(self, key):
        c = ctt_core.Content(value=collections.OrderedDict())
        keys = self.get_keys('{}.*'.format(key))
        for i_key in keys:
            i_value = self.get_as_unfold(i_key)
            i_key_ = i_key[len(key)+1:]
            c.set(i_key_, i_value)
        return c

    def get_as_unfold(self, key):
        keys_all = self.get_all_keys()
        return ctt_core.ContentUtil.unfold_fnc(
            key, keys_all, self._keys_exclude, self.get
        )


# <rev-version>
class AbsRsvVersionKey(object):
    VERSION_ZFILL_COUNT = 3
    VERSION_FNMATCH_PATTERN = 'v{}'.format('[0-9]'*VERSION_ZFILL_COUNT)

    @classmethod
    def _version__validation_fnc(cls, text):
        if not fnmatch.filter([text], cls.VERSION_FNMATCH_PATTERN):
            raise TypeError('version: "{}" is Non-match "{}"'.format(text, cls.VERSION_FNMATCH_PATTERN))

    def __init__(self, text):
        self._version__validation_fnc(text)
        #
        self._text = text
        self._number = int(text[-self.VERSION_ZFILL_COUNT:])

    @property
    def number(self):
        return self._number

    @classmethod
    def valid_fnc(cls, text):
        return not not fnmatch.filter([text], cls.VERSION_FNMATCH_PATTERN)

    def __str__(self):
        return self._text

    def __iadd__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError()
        self._number += int(other)
        self._text = 'v{}'.format(str(self._number).zfill(self.VERSION_ZFILL_COUNT))
        return self

    def __isub__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError()
        if self._number >= other:
            self._number -= int(other)
        else:
            self._number = 0
        self._text = 'v{}'.format(str(self._number).zfill(self.VERSION_ZFILL_COUNT))
        return self


class AbsRsvBaseDef(object):
    PATHSEP = '/'

    Platforms = rsv_core.RsvPlatforms
    Applications = rsv_core.RsvApplications

    EntityCategories = rsv_core.RsvEntityCategories
    EntityTypes = rsv_core.RsvEntityTypes

    VariantCategories = rsv_core.RsvVariantCategories
    VariantTypes = rsv_core.RsvVariantTypes

    WorkspaceKeys = rsv_core.RsvWorkspaceKeys
    WorkspaceMatchKeys = rsv_core.RsvWorkspaceMatchKeys


class AbsRsvEntityBaseDef(AbsRsvBaseDef):

    def _init_entity_base_def_(self):
        self._rsv_properties = None
        self._rsv_path = None
        self._rsv_matcher = None

    def _setup_rsv_entity(self, properties):
        self._rsv_path = properties.get('path')
        self._keyword = properties.get('keyword')
        self._pattern = properties.get('pattern')
        self._rsv_properties = properties

    def get_rsv_matcher(self):
        return self._rsv_matcher

    rsv_matcher = property(get_rsv_matcher)

    def get_properties(self):
        return self._rsv_properties

    properties = property(get_properties)

    def get(self, key):
        return self._rsv_properties.get(key)

    def set(self, key, value):
        self._rsv_properties.set(key, value)

    def get_type(self):
        return self.properties.get('type')

    type = property(get_type)

    def get_type_name(self):
        return self.get_type()

    type_name = property(get_type_name)

    def get_name(self):
        return bsc_core.PthNodeMtd.get_dag_name(self._rsv_path, pathsep=self.PATHSEP)

    name = property(get_name)

    @property
    def pattern(self):
        return self._pattern

    def _get_stack_key_(self):
        return self._rsv_path


class AbsRsvPattern(object):
    PATTERN_KEY_RE_PATTERN = r'[{](.*?)[}]'

    @classmethod
    def _pattern__get_variant_keys(cls, p):
        lis_0 = re.findall(re.compile(cls.PATTERN_KEY_RE_PATTERN, re.S), p)
        lis_1 = list(set(lis_0))
        lis_1.sort(key=lis_0.index)
        return lis_1

    @classmethod
    def _pattern__update_to(cls, p, **kwargs):
        if p is not None:
            keys = cls._pattern__get_variant_keys(p)
            s = p
            if keys:
                for i_key in keys:
                    if i_key in kwargs:
                        i_v = kwargs[i_key]
                        if i_v is not None and i_v != '*':
                            s = s.replace('{{{}}}'.format(i_key), kwargs[i_key])
            return s
        return p

    @classmethod
    def _pattern__get_fnmatch_args(cls, p):
        keys = cls._pattern__get_variant_keys(p)
        s = p
        if keys:
            for i_key in keys:
                s = s.replace('{{{}}}'.format(i_key), '*')
            return True, s
        return False, s

    @classmethod
    def _pattern__to_fnmatch_style(cls, p, **kwargs):
        keys = cls._pattern__get_variant_keys(p)
        s = p
        if keys:
            for i_key in keys:
                if i_key in kwargs:
                    s = s.replace('{{{}}}'.format(i_key), kwargs[i_key])
                else:
                    s = s.replace('{{{}}}'.format(i_key), '*')
            return s
        return s

    @classmethod
    def _pattern__get_result_args(cls, p, trim=None):
        if p is not None:
            enable, p_fnmatch = cls._pattern__get_fnmatch_args(p)
            if enable is True:
                _ = glob.glob(p_fnmatch) or []
                if _:
                    # sort by number
                    _.sort(key=lambda x: bsc_core.RawTextMtd.to_number_embedded_args(x))
                    if trim is not None:
                        _ = _[trim[0]:trim[1]]
                    # fix windows path
                    if platform.system() == 'Windows':
                        _ = [i.replace('\\', '/') for i in _]
                return _
            return [p_fnmatch]
        return []

    def __init__(self, p):
        self.__pattern = p

    @property
    def raw(self):
        return self.__pattern

    def update_variants(self, **kwargs):
        return AbsRsvPattern._pattern__update_to(
            self.__pattern, **kwargs
        )

    def update_variants_to(self, **kwargs):
        self.__pattern = AbsRsvPattern._pattern__update_to(
            self.__pattern, **kwargs
        )

    def get_results(self):
        return self._pattern__get_result_args(
            self.__pattern
        )

    def __str__(self):
        return '{}(raw="{}")'.format(
            self.__class__.__name__,
            self.__pattern
        )

    def __repr__(self):
        return self.__str__()


class AbsRsvMatcher(object):
    PATTERN_REF_RE_PATTERN = r'[<](.*?)[>]'
    PATTERN_KEY_RE_PATTERN = r'[{](.*?)[}]'

    RSV_PATTERN_CLS = None

    RSV_VERSION_KEY_CLS = None

    PROPERTIES_CLS = None

    @classmethod
    def _generate_properties_by_result(cls, pattern, properties, result):
        p = parse.parse(
            pattern, result, case_sensitive=True
        )
        if p:
            dic = copy.copy(properties.value)
            dic.update(p.named)
            return cls.PROPERTIES_CLS(None, dic)

    def __init__(self, rsv_obj, pattern, variants=None):
        if isinstance(rsv_obj, AbsRsvProject):
            self._rsv_project = rsv_obj
        else:
            self._rsv_project = rsv_obj._rsv_project

        self._variants = dict()
        self.__pattern_orig = pattern
        self.__patterns_all = []
        
        self._extend_variants = {}

        self._rsv_properties = self.PROPERTIES_CLS(
            None,
            copy.copy(self._rsv_project.properties.get_value())
        )
        self.__setup_matcher(variants)

    def __setup_matcher(self, format_variant):
        if isinstance(format_variant, dict):
            for k, v in format_variant.items():
                if v is not None:
                    self._rsv_properties.set(k, v)

        variants = self.__completion_match_variants(self._rsv_properties.get_value())
        self._variants = variants

        # add root to parse variants first
        variants_parse = {
            'root': variants['root'],
        }

        self.__pattern_parse = AbsRsvPattern._pattern__update_to(
            self.__pattern_orig, **variants_parse
        )
        # real pattern for match
        self.__patterns_all = self.__generate_all_patterns(
            self._variants
        )

    def __generate_all_patterns(self, variants):
        # variant maybe a list, get all valid patterns
        pattern = self.__pattern_orig
        if pattern is not None:
            patterns = [
                pattern
            ]
            keys = AbsRsvPattern._pattern__get_variant_keys(pattern)
            if keys:
                for i_key in keys:
                    if i_key in variants:
                        i_value = variants[i_key]
                        if isinstance(i_value, six.string_types):
                            c = len(patterns)
                            for j_index in range(c):
                                if i_value != '*':
                                    patterns[j_index] = patterns[j_index].replace('{{{}}}'.format(i_key), i_value)
                        elif isinstance(i_value, (tuple, list)):
                            # update patterns
                            c = len(patterns)
                            v_c = len(i_value)
                            patterns *= v_c
                            for j_index in range(c):
                                for k_seq, k_v in enumerate(i_value):
                                    k_index = c*k_seq+j_index
                                    if k_v != '*':
                                        patterns[k_index] = patterns[k_index].replace('{{{}}}'.format(i_key), k_v)
            # print(patterns)
            return patterns

    def __completion_match_variants(self, kwargs):
        root_choice = self._rsv_project._project__get_root_choice(kwargs)
        root_cur = self._rsv_project._rsv_properties.get(root_choice)
        kwargs['root'] = root_cur
        return kwargs

    def __get_path_by_local_variants(self, format_dict):
        pattern = self.__pattern_orig
        keys = AbsRsvPattern._pattern__get_variant_keys(pattern)
        for i in keys:
            if i not in format_dict:
                raise RuntimeError(
                    bsc_log.Log.trace_method_error(
                        'path resolver',
                        'key "{}" in pattern "{}" is not value assigned'.format(
                            i,
                            pattern
                        )
                    )
                )
        new_result = pattern.format(**format_dict)
        return new_result

    def __generate_fnmatch_args(self, pattern):
        pattern_query = self._rsv_project.get_variant('variant-fnmatch-patterns')
        keys = AbsRsvPattern._pattern__get_variant_keys(pattern)
        s = pattern
        if keys:
            for i_key in keys:
                if i_key in pattern_query:
                    i_pattern = pattern_query[i_key]
                    i_pattern = AbsRsvPattern._pattern__to_fnmatch_style(
                        i_pattern, **self._variants
                    )
                else:
                    i_pattern = '*'

                s = s.replace('{{{}}}'.format(i_key), i_pattern)
            return True, s
        if '*' in s:
            return True, s
        return False, s

    def __generate_result_args(self, pattern, trim=None):
        if pattern is not None:
            enable, glob_pattern = self.__generate_fnmatch_args(pattern)
            if enable is True:
                _ = glob.glob(glob_pattern) or []
                if _:
                    # sort by number
                    _.sort(key=lambda x: bsc_core.RawTextMtd.to_number_embedded_args(x))
                    if trim is not None:
                        _ = _[trim[0]:trim[1]]
                    # fix windows path
                    if platform.system() == 'Windows':
                        _ = [i.replace('\\', '/') for i in _]
                return True, _
            #
            if os.path.exists(glob_pattern):
                return False, [glob_pattern]
        return False, []

    def _generate_default_project_properties_by_result(self, result):
        properties_orig = copy.copy(self._rsv_properties)
        properties_orig.set('project', '*')
        pattern = self.__pattern_parse
        pattern = pattern.replace('default', '{project}')
        return self._generate_properties_by_result(
            pattern,
            properties_orig,
            result
        )

    def _matcher__get_matches(self, trim):
        list_ = []
        for i_pattern in self.__patterns_all:
            i_enable, i_results = self.__generate_result_args(i_pattern)
            if trim is not None:
                i_results = i_results[trim[0]:trim[1]]
            #
            for j_result in i_results:
                j_p = parse.parse(
                    self.__pattern_parse, j_result, case_sensitive=True
                )
                if j_p:
                    j_variants = j_p.named
                    list_.append(
                        (j_result, j_variants)
                    )
        #
        return list_

    def set_extend_variants(self, **kwargs):
        self._extend_variants = kwargs

    def get_results(self, trim=None):
        list_ = []
        for i_pattern in self.__patterns_all:
            _, i_results = self.__generate_result_args(i_pattern, trim)
            list_.extend(i_results)
            return list_

    def get_matches(self, trim=None):
        return self._matcher__get_matches(trim)

    def get_latest(self):
        matches = self._matcher__get_matches(trim=(-1, None))
        if matches:
            result, parameters = matches[-1]
            format_dict = copy.copy(self._variants)
            format_dict.update(parameters)
            return self.__get_path_by_local_variants(format_dict)

    def generate_properties_by_result(self, result):
        return self._generate_properties_by_result(
            self.__pattern_parse,
            self._rsv_properties,
            result
        )

    def get_new(self):
        matches = self.get_matches(trim=(-1, None))
        format_dict = copy.copy(self._variants)
        if matches:
            result, parameters = matches[-1]
            format_dict.update(parameters)
            if 'version' in format_dict:
                version = format_dict['version']
                if self.RSV_VERSION_KEY_CLS.valid_fnc(version):
                    rsv_version_key = self.RSV_VERSION_KEY_CLS(version)
                    rsv_version_key += 1
                    format_dict['version'] = str(rsv_version_key)
                return self.__get_path_by_local_variants(format_dict)
            return result
        #
        if 'version' in format_dict:
            format_dict['version'] = 'v001'
        return self.__get_path_by_local_variants(format_dict)

    def get_current(self):
        format_dict = copy.copy(self._variants)
        return self.__get_path_by_local_variants(format_dict)

    @classmethod
    def _set_rsv_version_key_create_(cls, version):
        return cls.RSV_VERSION_KEY_CLS(version)

    def __str__(self):
        return '{}(pattern="{}")'.format(
            self.__class__.__name__,
            self.__pattern_orig
        )


class AbsRsvEntity(
    AbsRsvEntityBaseDef,
    # dag
    unr_abstracts.AbsObjDagExtraDef,
    # gui
    unr_abstracts.AbsGuiExtraDef
):
    PROPERTIES_CLS = None

    @classmethod
    def _completion_kwargs_from_parent(cls, rsv_parent, kwargs):
        # do not override this keys
        for k, v in rsv_parent.properties.get_value().items():
            if k not in cls.VariantTypes.VariableTypes:
                kwargs[k] = v

    def __init__(self, *args, **kwargs):
        self._init_entity_base_def_()
        #
        rsv_project = args[0]
        #
        self._rsv_project = rsv_project
        #
        self._setup_rsv_entity(
            self.PROPERTIES_CLS(self, bsc_core.DictMtd.sort_key_to(kwargs))
        )
        self._init_obj_dag_extra_def_(self._rsv_path)
        self._init_gui_extra_def_()
        #
        self._rsv_matcher = self._rsv_project._project__generate_rsv_matcher(
            self._rsv_properties.value
        )
        if self.type_name in self.VariantTypes.Trunks:
            self.set_gui_menu_raw(
                [
                    ('{}-directory'.format(self.type_name),),
                    ('Open Directory', 'file/open-folder',
                     (self._get_source_directory_is_enable, self._open_source_directory, False)),
                ]
            )
        elif self.type_name in self.VariantTypes.Branches:
            self.set_gui_menu_raw(
                [
                    [
                        'Open Directory', 'file/open-folder',
                        [
                            ('{}-directory'.format(self.type_name),),
                            ('Source', 'file/open-folder',
                             (self._get_source_directory_is_enable, self._open_source_directory, False)),
                            ('User', 'file/open-folder',
                             (self._get_user_directory_is_enable, self._open_user_directory, False)),
                            ('Release', 'file/open-folder',
                             (self._get_release_directory_is_enable, self._open_release_directory, False)),
                            ('Temporary', 'file/open-folder',
                             (self._get_temporary_directory_is_enable, self._open_temporary_directory, False)),
                        ]
                    ]
                ]
            )
        #
        self.set_description(
            '\n'.join(
                [
                    '{} : {}'.format(k, v)
                    for k, v in bsc_core.DictMtd.sort_key_to(kwargs).items()
                    if k in rsv_core.RsvVariantTypes.Descriptions
                ]
            )
        )

    def _get_valid_rsv_pattern(self, **kwargs):
        entity_type = self.type_name
        if entity_type in self.VariantTypes.Trunks:
            key = '{type}-dir'.format(**kwargs)
            return self._rsv_project.get_pattern(key)
        elif entity_type in self.VariantTypes.Branches:
            key = '{branch}-{workspace_key}-{type}-dir'.format(**kwargs)
            return self._rsv_project.get_pattern(key)
        return self._pattern

    # source
    def _get_source_directory_path(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_source()
        kwargs['workspace_key'] = self.WorkspaceKeys.Source
        p = self._get_valid_rsv_pattern(**kwargs)
        return AbsRsvPattern._pattern__update_to(p, **kwargs)

    def _get_source_directory_is_enable(self):
        directory_path = self._get_source_directory_path()
        return bsc_storage.StgDirectoryOpt(directory_path).get_is_exists()

    def _open_source_directory(self):
        directory_path = self._get_source_directory_path()
        bsc_storage.StgDirectoryOpt(directory_path).open_in_system()

    # user
    def _get_user_directory_path(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_user()
        kwargs['workspace_key'] = self.WorkspaceKeys.User
        kwargs['artist'] = bsc_core.SysBaseMtd.get_user_name()
        p = self._get_valid_rsv_pattern(**kwargs)
        return AbsRsvPattern._pattern__update_to(p, **kwargs)

    def _get_user_directory_is_enable(self):
        directory_path = self._get_user_directory_path()
        return bsc_storage.StgDirectoryOpt(directory_path).get_is_exists()

    def _open_user_directory(self):
        directory_path = self._get_user_directory_path()
        bsc_storage.StgDirectoryOpt(directory_path).open_in_system()

    # release
    def _get_release_directory_path(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_release()
        kwargs['workspace_key'] = self.WorkspaceKeys.Release
        p = self._get_valid_rsv_pattern(**kwargs)
        return AbsRsvPattern._pattern__update_to(p, **kwargs)

    def _get_release_directory_is_enable(self):
        directory_path = self._get_release_directory_path()
        return bsc_storage.StgDirectoryOpt(directory_path).get_is_exists()

    def _open_release_directory(self):
        directory_path = self._get_release_directory_path()
        bsc_storage.StgDirectoryOpt(directory_path).open_in_system()

    # temporary
    def _get_temporary_directory_path(self):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self.rsv_project.get_workspace_temporary()
        kwargs['workspace_key'] = self.WorkspaceKeys.Temporary
        p = self._get_valid_rsv_pattern(**kwargs)
        return AbsRsvPattern._pattern__update_to(p, **kwargs)

    def _get_temporary_directory_is_enable(self):
        directory_path = self._get_temporary_directory_path()
        return bsc_storage.StgDirectoryOpt(directory_path).get_is_exists()

    def _open_temporary_directory(self):
        directory_path = self._get_temporary_directory_path()
        bsc_storage.StgDirectoryOpt(directory_path).open_in_system()

    def get_rsv_project(self):
        return self._rsv_project

    rsv_project = property(get_rsv_project)

    @property
    def icon(self):
        return bsc_resource.RscExtendIcon.get('file/folder')

    def create_dag_fnc(self, path):
        return self.rsv_project.get_rsv_entity(path)

    def _get_child_paths_(self, *args, **kwargs):
        return self.rsv_project._project__find_rsv_entity_child_paths(self._rsv_path)

    def get_descendants(self):
        return self.rsv_project.get_rsv_entities(regex='{}/*'.format(self.path))

    def _get_child_(self, path):
        return self.rsv_project.get_rsv_entity(path)

    def get_location(self):
        return self.properties.get('result')

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()


class AbsRsvUnit(AbsRsvEntity):
    def __init__(self, *args, **kwargs):
        super(AbsRsvUnit, self).__init__(*args, **kwargs)

    def get_result(self, version=None, variants_extend=None, trim=None):
        kwargs = copy.copy(self.properties.value)
        if version is None:
            version = rsv_core.RsvVersion.LATEST
        #
        kwargs['workspace'] = self._rsv_project._project__guess_workspace(**kwargs)
        if variants_extend is not None:
            kwargs.update(variants_extend)
        #
        if version == rsv_core.RsvVersion.LATEST:
            kwargs['version'] = '*'
            rsv_matcher = self.rsv_project._generate_rsv_matcher(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_latest()
        elif version == rsv_core.RsvVersion.NEW:
            kwargs['version'] = '*'
            rsv_matcher = self.rsv_project._generate_rsv_matcher(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_new()
        elif version == rsv_core.RsvVersion.ALL:
            kwargs['version'] = '*'
            rsv_matcher = self.rsv_project._generate_rsv_matcher(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_results(trim=trim)
        #
        kwargs['version'] = version
        rsv_matcher = self.rsv_project._generate_rsv_matcher(
            self._pattern,
            kwargs
        )
        return rsv_matcher.get_current()

    def get_current(self, variants_extend):
        kwargs = copy.copy(self.properties.value)
        kwargs.update(variants_extend)
        rsv_matcher = self.rsv_project._generate_rsv_matcher(
            self._pattern,
            kwargs
        )
        return rsv_matcher.get_current()

    def get_exists_result(self, *args, **kwargs):
        result = self.get_result(*args, **kwargs)
        if result:
            if isinstance(result, six.string_types):
                if bsc_storage.StgPathMtd.get_is_exists(result):
                    return result
            elif isinstance(result, (tuple, list)):
                return result

    def get_results(self, version=None, check_exists=False, trim=None):
        kwargs = copy.copy(self.properties.value)
        if version is None:
            version = self.properties.get('version')
        #
        kwargs['workspace'] = self._rsv_project._project__guess_workspace(**kwargs)
        if version == rsv_core.RsvVersion.LATEST:
            version = self.get_latest_version()
        elif version == rsv_core.RsvVersion.NEW:
            version = self.get_new_version()
        #
        if version is not None:
            kwargs['version'] = version
            kwargs['workspace'] = self._rsv_project._project__guess_workspace(**kwargs)
            rsv_matcher = self.rsv_project._generate_rsv_matcher(
                self._pattern,
                kwargs
            )
            results = rsv_matcher.get_results(trim=trim)
            if check_exists is True:
                return self._filter_exists_results(results)
            return results
        return []

    def get_exists_results(self, *args, **kwargs):
        kwargs['check_exists'] = True
        return self.get_results(*args, **kwargs)

    def _filter_exists_results(self, results):
        keyword = self.properties.get('keyword')
        if keyword.endswith('-file'):
            return [i for i in results if os.path.isfile(i)]
        elif keyword.endswith('-dir'):
            return [i for i in results if os.path.isdir(i)]

    def get_latest_results(self):
        kwargs = copy.copy(self.properties.value)
        version = self.get_latest_version()
        if version is not None:
            kwargs['version'] = version
            kwargs['workspace'] = self._rsv_project._project__guess_workspace(**kwargs)
            rsv_matcher = self.rsv_project._generate_rsv_matcher(
                self._pattern,
                kwargs
            )
            return rsv_matcher.get_results()

    def get_extend_variants(self, file_path):
        variants = self._rsv_properties.value
        pattern = self._pattern
        rsv_matcher = self._rsv_project._generate_rsv_matcher(
            pattern,
            dict(
                type='unit',
                workspace=self._rsv_project.get_workspace_release()
            )
        )
        cur_variants = rsv_matcher.generate_properties_by_result(result=file_path)
        return {k: v for k, v in cur_variants.items() if k not in variants}

    def generate_properties_by_result(self, file_path, override_variants=None):
        kwargs = copy.copy(self.properties.value)
        kwargs['workspace'] = self._rsv_project._project__guess_workspace(**kwargs)
        if override_variants is not None:
            kwargs.update(override_variants)
        #
        rsv_matcher = self.rsv_project._generate_rsv_matcher(
            self._pattern,
            kwargs
        )
        file_properties = rsv_matcher.generate_properties_by_result(
            result=file_path
        )
        return file_properties

    def get_latest_version(self, variants_extend=None):
        kwargs = copy.copy(self.properties.value)
        kwargs['version'] = '*'
        kwargs['workspace'] = self._rsv_project._project__guess_workspace(**kwargs)
        #
        if variants_extend is not None:
            kwargs.update(variants_extend)
        #
        rsv_matcher = self.rsv_project._generate_rsv_matcher(
            self._pattern,
            kwargs
        )
        matches = rsv_matcher.get_matches(trim=(-1, None))
        if matches:
            result, variants = matches[-1]
            version = variants['version']
            return version

    def get_new_version(self, variants_extend=None):
        version = self.get_latest_version(variants_extend)
        if version is not None:
            rsv_version_key = self._rsv_matcher._set_rsv_version_key_create_(version)
            rsv_version_key += 1
            return str(rsv_version_key)
        return 'v001'

    def get_all_exists_matches(self, variants_extend=None):
        kwargs = copy.copy(self.properties.value)
        kwargs['version'] = '*'
        kwargs['workspace'] = self._rsv_project._project__guess_workspace(**kwargs)
        #
        if variants_extend is not None:
            kwargs.update(variants_extend)
        #
        rsv_matcher = self.rsv_project._generate_rsv_matcher(
            self._pattern,
            kwargs
        )
        return rsv_matcher.get_matches()

    def get_all_exists_results(self, variants_extend=None):
        matches = self.get_all_exists_matches(variants_extend)
        list_ = []
        if matches:
            for i in matches:
                i_result, i_variants = i
                list_.append(i_result)
        return list_

    def get_all_exists_versions(self, variants_extend=None):
        matches = self.get_all_exists_matches(variants_extend)
        list_ = []
        if matches:
            for i in matches:
                i_result, i_variants = i
                list_.append(i_variants['version'])
        return list_

    def get_rsv_version(self, **kwargs):
        rsv_version = self.rsv_project._entity__get_rsv_unit_version(
            rsv_obj=self,
            **kwargs
        )
        return rsv_version

    def get_rsv_versions(self, trim=None):
        list_ = []
        results = self.get_result(version='all', trim=trim)
        for i_result in results:
            i_properties = self.generate_properties_by_result(i_result)
            i_properties.set('keyword', self.get('keyword'))
            i_rsv_version = self.get_rsv_version(**i_properties.value)
            list_.append(i_rsv_version)
        return list_

    def get_rsv_task(self):
        return self.get_parent().get_parent()

    def get_rsv_step(self):
        return self.get_parent().get_parent().get_parent()

    def get_rsv_resource(self):
        return self.get_parent().get_parent().get_parent().get_parent()


class AbsRsvUnitVersion(AbsRsvEntity):
    def __init__(self, *args, **kwargs):
        super(AbsRsvUnitVersion, self).__init__(*args, **kwargs)
        self.set_gui_menu_raw(
            [
                ('{}-directory'.format(self.type_name),),
                ('Open Directory', 'file/folder', (True, self._open_source_directory, False)),
            ]
        )

        self._result = None

    def get_rsv_unit(self):
        return self.get_parent()

    def open_directory(self):
        if self._result:
            bsc_storage.StgPathOpt(self._result).open_in_system()


class AbsRsvTaskVersion(AbsRsvEntity):
    def __init__(self, *args, **kwargs):
        super(AbsRsvTaskVersion, self).__init__(*args, **kwargs)

    def get_rsv_task(self):
        return self.get_parent()

    # unit
    def get_rsv_unit(self, **kwargs):
        return self.rsv_project._entity__get_rsv_unit(
            rsv_obj=self,
            **kwargs
        )

    def get_directory_path(self):
        return self.properties.get('result')


# <rsv-task>
class AbsRsvTask(AbsRsvEntity):
    def __init__(self, *args, **kwargs):
        super(AbsRsvTask, self).__init__(*args, **kwargs)
        # self.set_gui_menu_raw_extend(
        #     [
        #         (),
        #         [
        #             'Open Work-scene-src-directory', 'file/open-folder',
        #             self.get_work_scene_src_directory_open_menu_raw()
        #         ]
        #     ]
        # )

    @property
    def icon(self):
        return bsc_resource.RscExtendIcon.get('file/file')

    def get_work_scene_src_directory_open_menu_raw(self):
        def add_fnc_(application_):
            def get_directory_is_exists_fnc_():
                return bsc_storage.StgDirectoryOpt(_directory_path).get_is_exists()

            def set_directory_open_fnc_():
                bsc_storage.StgDirectoryOpt(_directory_path).open_in_system()

            #
            _branch = self.properties.get('branch')
            _keyword = '{}-work-{}-scene-src-dir'.format(_branch, application_)
            _rsv_unit = self.get_rsv_unit(keyword=_keyword)
            _directory_path = _rsv_unit.get_result()
            list_.append(
                (application_, 'application/{}'.format(application_),
                 (get_directory_is_exists_fnc_, set_directory_open_fnc_, False))
            )

        list_ = []
        for i_app in self.Applications.DCCS:
            add_fnc_(i_app)
        return list_

    def get_directory_path(self):
        return self.properties.get('result')

    # todo: remove old fnc, use "get_rsv_scene_properties_by_any_scene_file_path"
    def get_properties_by_work_scene_src_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            pattern_keyword='{branch}-source-{application}-scene-src-file',
            override_variants=dict(workspace=self._rsv_project.get_workspace_source()),
            file_path_keys=['any_scene_file', 'work_scene_src_file', 'work_source_file']
        )

    def get_properties_by_scene_src_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            pattern_keyword='{branch}-{application}-scene-src-file',
            override_variants=dict(workspace=self._rsv_project.get_workspace_release()),
            file_path_keys=['any_scene_file', 'scene_src_file', 'source_file']
        )

    def get_properties_by_scene_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            pattern_keyword='{branch}-{application}-scene-file',
            override_variants=dict(workspace=self._rsv_project.get_workspace_release()),
            file_path_keys=['any_scene_file', 'scene_file']
        )

    def get_properties_by_output_scene_src_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            pattern_keyword='{branch}-temporary-{application}-scene-src-file',
            override_variants=dict(workspace=self._rsv_project.get_workspace_temporary()),
            file_path_keys=['any_scene_file', 'output_scene_src_file']
        )

    def get_properties_by_output_scene_file_path(self, file_path):
        return self._get_properties_by_scene_file_path_(
            file_path,
            pattern_keyword='{branch}-temporary-{application}-scene-file',
            override_variants=dict(workspace=self._rsv_project.get_workspace_temporary()),
            file_path_keys=['any_scene_file', 'output_scene_file']
        )

    def _get_properties_by_scene_file_path_(self, file_path, pattern_keyword, override_variants, file_path_keys):
        if file_path is not None:
            branch = self.properties.get('branch')
            for i_application in self.Applications.DCCS:
                keyword = pattern_keyword.format(
                    **dict(branch=branch, application=i_application)
                )
                rsv_task_unit = self.get_rsv_unit(
                    keyword=keyword,
                    application=i_application
                )
                task_unit_properties = rsv_task_unit.generate_properties_by_result(file_path, override_variants)
                if task_unit_properties:
                    task_unit_properties.set('application', i_application)
                    task_unit_properties.set('user', bsc_core.SysBaseMtd.get_user_name())
                    task_unit_properties.set('time', bsc_core.SysBaseMtd.get_time())
                    task_unit_properties.set('time_tag', bsc_core.SysBaseMtd.get_time_tag())
                    for i_file_path_key in file_path_keys:
                        task_unit_properties.set(i_file_path_key, file_path)
                    #
                    task_unit_properties.set('option.scheme', self._rsv_project.get_workspace_release())
                    task_unit_properties.set('option.version', task_unit_properties.get('version'))
                    #
                    task_unit_properties.set('dcc.root', '/master')
                    task_unit_properties.set('dcc.root_name', 'master')
                    task_unit_properties.set('dcc.sub_root', '/master/hi')
                    #
                    task_unit_properties.set('dcc.pathsep', self.Applications.get_pathsep(i_application))
                    return task_unit_properties

    #
    def get_rsv_scene_properties_by_any_scene_file_path(self, file_path):
        if file_path is not None:
            branch = self.properties.get('branch')
            for i_application in self.Applications.DCCS:
                for j_keyword_format, scene_type in [
                    # source
                    ('{branch}-source-{application}-scene-src-file', 'source-scene-src'),
                    ('{branch}-user-{application}-scene-src-file', 'user-scene-src'),
                    # release
                    ('{branch}-{application}-scene-src-file', 'release-scene-src'),
                    ('{branch}-{application}-scene-file', 'release-scene'),
                    # temporary
                    ('{branch}-temporary-{application}-scene-src-file', 'temporary-scene-src'),
                    ('{branch}-temporary-{application}-scene-file', 'temporary-scene'),
                ]:
                    j_keyword = j_keyword_format.format(
                        **dict(branch=branch, application=i_application)
                    )
                    if self._rsv_project.has_pattern(j_keyword):
                        j_rsv_unit = self.get_rsv_unit(
                            keyword=j_keyword,
                            application=i_application
                        )
                        j_rsv_scene_properties = j_rsv_unit.generate_properties_by_result(file_path)
                        if j_rsv_scene_properties:
                            j_rsv_scene_properties.set('keyword', j_keyword)
                            j_rsv_scene_properties.set('scene_type', scene_type)
                            #
                            j_rsv_scene_properties.set('branch', branch)
                            j_rsv_scene_properties.set('resource', j_rsv_scene_properties.get(branch))
                            j_rsv_scene_properties.set('application', i_application)
                            #
                            j_rsv_scene_properties.set('extra.file', file_path)
                            j_rsv_scene_properties.set('extra.user', bsc_core.SysBaseMtd.get_user_name())
                            j_rsv_scene_properties.set('extra.time_tag', bsc_core.SysBaseMtd.get_time_tag())
                            #
                            j_rsv_scene_properties.set(
                                'dcc', self._rsv_project.get_dcc_data(i_application).get_value()
                            )
                            j_rsv_scene_properties.set(
                                'usd', self._rsv_project.get_dcc_data('usd').get_value()
                            )
                            return j_rsv_scene_properties

    # resource group
    def get_rsv_resource_group(self):
        return self.get_parent().get_parent().get_parent()

    # resource
    def get_rsv_resource(self):
        return self.get_parent().get_parent()

    # step
    def get_rsv_step(self):
        return self.get_parent()

    # version
    def get_rsv_version(self, **kwargs):
        return self.rsv_project._entity__get_rsv_task_version(
            rsv_obj=self,
            **kwargs
        )

    def get_rsv_versions(self, **kwargs):
        kwargs_over = self.properties.get_value_as_copy()
        kwargs_over.update(kwargs)
        return self._rsv_project._project__get_rsv_task_versions_(
            **kwargs_over
        )

    # unit
    def get_rsv_unit(self, **kwargs):
        return self.rsv_project._entity__get_rsv_unit(
            rsv_obj=self,
            **kwargs
        )

    def get_rsv_scene_properties(self):
        properties = self.PROPERTIES_CLS(
            self, self.properties.get_value_as_copy()
        )
        properties.set(
            'user', bsc_core.SysBaseMtd.get_user_name()
        )
        return properties

    def create_directory(self, workspace_key):
        variants = self.properties.get_value_as_copy()
        variants['workspace_key'] = workspace_key
        keyword = '{branch}-{workspace_key}-task-dir'.format(
            **variants
        )
        rsv_unit = self.get_rsv_unit(keyword=keyword)
        # version use new for create
        directory_path = rsv_unit.get_result(version='new')

        bsc_storage.StgPathPermissionMtd.create_directory(
            directory_path
        )
        # bsc_storage.StgPathPermissionMtd.change_owner(
        #
        # )


# <rsv-step>
class AbsRsvStep(AbsRsvEntity):
    def __init__(self, *args, **kwargs):
        super(AbsRsvStep, self).__init__(*args, **kwargs)

    def get_rsv_unit(self, **kwargs):
        return self.rsv_project._entity__get_rsv_unit(
            rsv_obj=self,
            **kwargs
        )

    def get_directory_path(self):
        return self.properties.get('result')

    def get_source_directory_path(self):
        keyword = self._rsv_project._generate_step_keyword(
            self.properties.get('branch'),
            self.WorkspaceKeys.Source
        )
        return self.get_rsv_unit(
            workspace=self._rsv_project.get_workspace_source(),
            keyword=keyword
        ).get_result()

    def get_rsv_tasks(self, **kwargs):
        self._completion_kwargs_from_parent(self, kwargs)
        return self._rsv_project._project__get_rsv_tasks(
            **kwargs
        )

    def get_rsv_task(self, **kwargs):
        rsv_obj = self.rsv_project._entity__get_rsv_task(
            rsv_obj=self,
            **kwargs
        )
        return rsv_obj


class AbsRsvResource(AbsRsvEntity):
    def __init__(self, *args, **kwargs):
        super(AbsRsvResource, self).__init__(*args, **kwargs)

    @property
    def icon(self):
        return bsc_resource.RscExtendIcon.get('resolver/asset')

    def get_rsv_steps(self, **kwargs):
        self._completion_kwargs_from_parent(self, kwargs)
        return self._rsv_project._project__get_rsv_steps(
            **kwargs
        )

    def get_rsv_step(self, **kwargs):
        """
        :param kwargs: step: str(<step-name>)
        :return: instance(<rsv-step>)
        """
        rsv_obj = self.rsv_project._entity__get_rsv_step(
            rsv_obj=self,
            **kwargs
        )
        return rsv_obj

    def get_rsv_tasks(self, **kwargs):
        self._completion_kwargs_from_parent(self, kwargs)
        return self._rsv_project._project__get_rsv_tasks(
            **kwargs
        )

    def get_rsv_task(self, **kwargs):
        rsv_step = self.get_rsv_step(**kwargs)
        if rsv_step is not None:
            return rsv_step.get_rsv_task(**kwargs)

    def get_rsv_unit(self, **kwargs):
        """
        :param kwargs:
            task: str
            keyword: str
        :return:
        """
        return self.rsv_project._entity__get_rsv_unit(
            rsv_obj=self,
            **kwargs
        )

    def get_available_rsv_unit(self, **kwargs):
        """
        :param kwargs:
            task: str / [str, ...]
            keyword: str
        :return:
        """
        rsv_tasks = self.get_rsv_tasks(**kwargs)
        keyword = kwargs['keyword']
        for i_rsv_task in rsv_tasks:
            i_rsv_unit = i_rsv_task.get_rsv_unit(keyword=keyword)
            if i_rsv_unit.get_result(version='latest'):
                return i_rsv_unit


class AbsRsvResourceGroup(AbsRsvEntity):
    def __init__(self, *args, **kwargs):
        super(AbsRsvResourceGroup, self).__init__(*args, **kwargs)

    def get_rsv_resources(self, **kwargs):
        self._rsv_project._project__completion_kwargs_from_parent_(
            self.EntityCategories.Resource, self, kwargs
        )
        kwargs['branch'] = self.get('branch')
        return self._rsv_project._project__get_rsv_resources(
            **kwargs
        )

    def get_rsv_resource(self, **kwargs):
        """
        :param kwargs: asset: str(<asset-name>) / shot: str(<shot-name>)
        :return: instance(<rsv-entity>)
        """
        rsv_obj = self._rsv_project._entity__get_rsv_resource(
            rsv_obj=self,
            **kwargs
        )
        return rsv_obj

    def get_rsv_steps(self, **kwargs):
        self._completion_kwargs_from_parent(self, kwargs)
        return self._rsv_project._project__get_rsv_steps(
            **kwargs
        )

    def get_rsv_tasks(self, **kwargs):
        self._completion_kwargs_from_parent(self, kwargs)
        return self._rsv_project._project__get_rsv_tasks(
            **kwargs
        )


class AbsRsvConfigureExtraDef(AbsRsvBaseDef):
    RSV_PATTERN_CLS = None

    @classmethod
    def _completion_rsv_kwargs(cls, **kwargs):
        # use url
        if 'url' in kwargs:
            url = kwargs['url']
            dict_ = rsv_core.RsvBase.parse_url(url)
        elif 'file' in kwargs:
            dict_ = kwargs
            k = kwargs['file']
            keyword = '{}-file'.format(k)
            if fnmatch.filter([keyword], 'asset-*'):
                branch = 'asset'
            elif fnmatch.filter([keyword], 'shot-*'):
                branch = 'shot'
            else:
                raise TypeError()
            dict_['branch'] = branch
        # use keyword
        elif 'keyword' in kwargs:
            dict_ = kwargs
            keyword = kwargs['keyword']
            if fnmatch.filter([keyword], 'asset-*'):
                branch = cls.EntityTypes.Asset
            elif fnmatch.filter([keyword], 'sequence-*'):
                branch = 'sequence'
            elif fnmatch.filter([keyword], 'shot-*'):
                branch = 'shot'
            else:
                raise TypeError()
            dict_['branch'] = branch
        else:
            dict_ = kwargs
        return dict_

    @classmethod
    def _generate_rsv_configure_opt(cls, raw):
        return RsvConfigureOpt(raw)

    @classmethod
    def _name_validation_fnc(cls, entity_type, name):
        _ = re.findall(
            r'[^a-zA-Z0-9_]',
            name
        )
        if _:
            if rsv_core.WARNING_ENABLE is True:
                bsc_log.Log.trace_method_warning(
                    'name check',
                    u'{}-name="{}" is not available'.format(entity_type, name)
                )
            return False
        return True

    @classmethod
    def _guess_entity_type(cls, **kwargs):
        if 'branch' in kwargs:
            return kwargs['branch']
        # sequence or shot
        elif 'shot' in kwargs:
            return cls.EntityTypes.Shot
        elif 'sequence' in kwargs:
            return cls.EntityTypes.Sequence
        # asset
        elif 'asset' in kwargs:
            return cls.EntityTypes.Asset
        elif 'role' in kwargs:
            return cls.EntityTypes.Asset
        return cls.EntityTypes.Project

    @classmethod
    def _guess_entity_type_force(cls, **kwargs):
        entity_type = cls._guess_entity_type(**kwargs)
        if entity_type is None:
            raise RuntimeError(
                'argument key "branch" must definition in kwargs'
            )
        return entity_type

    @classmethod
    def _generate_step_keyword(cls, branch, workspace_key):
        return '{}-{}-step-dir'.format(branch, workspace_key)

    @classmethod
    def _generate_task_keyword(cls, branch, workspace_key):
        return '{}-{}-task-dir'.format(branch, workspace_key)

    @staticmethod
    def _completion_keyword(variants):
        """
        etc: keyword = '{branch}-component-usd-file'
        :param variants:
        :return:
        """
        keyword = variants.pop('keyword')
        # noinspection PyStatementEffect
        keyword = keyword.format(**variants)
        variants['keyword'] = keyword
        return keyword

    @staticmethod
    def _completion_rsv_entity_extend_create_kwargs(kwargs, result, kwargs_extend):
        update = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
            bsc_storage.StgFileOpt(
                result
            ).get_modify_timestamp(),
            language=1
        )
        user = bsc_storage.StgPathOpt(
            result
        ).get_user()
        #
        kwargs['result'] = result
        kwargs['update'] = update
        kwargs['user'] = user
        kwargs.update(kwargs_extend)

    def _init_configure_extra_def_(self):
        self._raw = collections.OrderedDict()
        self._patterns_dict = collections.OrderedDict()

    def _setup_rsv_configure(self, raw):
        self._raw = raw
        self._raw_opt = RsvConfigureOpt(self._raw)

    def _build_all_patterns(self):
        file_keys = self._raw_opt.get_keys(pattern='*-file')
        directory_keys = self._raw_opt.get_keys(pattern='*-dir')
        for i_key in file_keys+directory_keys:
            self._patterns_dict[i_key] = self._raw_opt.unfold_value(self._raw_opt.get(i_key))

    def _get_path_variant_keys(self, rsv_category):
        return self._raw_opt.get('path-{}-keys'.format(rsv_category))

    def _generate_rsv_entity_path(self, rsv_category, variants):
        var_keys = self._get_path_variant_keys(rsv_category)
        p_values = ['', ]
        for i_key in var_keys:
            if i_key in variants:
                p_values.append(variants[i_key])
        return self.PATHSEP.join(p_values)

    def _generate_rsv_version_path(self, main_path, variants):
        search_keys_extend = self._raw_opt.get('path-version-keys_extend')
        #
        p_values = ['', ]
        for i_key in search_keys_extend:
            if i_key in variants:
                p_values.append(variants[i_key])
            else:
                raise KeyError('key: "{}" is non-exists'.format(i_key))
        #
        return main_path+self.PATHSEP.join(p_values)

    def _generate_rsv_unit_path(self, main_path, variants):
        search_keys_extend = self._raw_opt.get('path-unit-keys_extend')
        #
        p_values = ['', ]
        for i_key in search_keys_extend:
            if i_key in variants:
                p_values.append(variants[i_key])
            else:
                raise KeyError('key: "{}" is non-exists'.format(i_key))
        #
        return main_path+self.PATHSEP.join(p_values)

    def _copy_variants_as_branches_(self, variants):
        kwargs_copy = {}
        var_keys = self._raw_opt.get('path-main-keys')
        for i_key in var_keys:
            if i_key in variants:
                kwargs_copy[i_key] = variants[i_key]
        #
        keys_extend = ['branch', 'workspace']
        for i_key in keys_extend:
            if i_key in variants:
                kwargs_copy[i_key] = variants[i_key]
        return kwargs_copy

    def _generate_rsv_entity_create_kwargs(self, obj_path, kwargs_src, extend_keys=None):
        keyword = kwargs_src['keyword']
        kwargs_tgt = collections.OrderedDict()
        pattern = self.get_pattern(keyword)
        keys = AbsRsvPattern._pattern__get_variant_keys(pattern)
        #
        if isinstance(extend_keys, (tuple, list)):
            keys.extend(list(extend_keys))
        #
        for i_key in keys:
            if i_key in kwargs_src:
                kwargs_tgt[i_key] = kwargs_src[i_key]
        #
        kwargs_tgt['path'] = obj_path
        kwargs_tgt['keyword'] = keyword
        kwargs_tgt['pattern'] = pattern
        return kwargs_tgt

    def _cleanup_rsv_entity_create_kwargs(self, rsv_category, kwargs):
        entity_var_keys = self._raw_opt.get('path-{}-keys'.format(rsv_category))
        main_var_keys = self._raw_opt.get('path-main-keys')
        #
        keys_main = self.VariantTypes.Constructs
        keys_extend = self.VariantTypes.Extends
        keys_includes = keys_main+keys_extend
        for k, v in kwargs.items():
            if k in keys_includes:
                if k in main_var_keys and k not in entity_var_keys:
                    kwargs.pop(k)
            # remove excludes
            else:
                kwargs.pop(k)

    def _completion_rsv_entity_create_kwargs(self, rsv_category, entity_type, kwargs, result, kwargs_extend):
        rsv_path = self._generate_rsv_entity_path(rsv_category, kwargs)
        #
        kwargs['category'] = rsv_category
        kwargs['type'] = entity_type
        kwargs['path'] = rsv_path
        user = bsc_storage.StgPathOpt(result).get_user()
        #
        kwargs['result'] = result
        if bsc_storage.StgFileOpt(result).get_is_exists() is True:
            update = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
                bsc_storage.StgFileOpt(
                    result
                ).get_modify_timestamp(),
                language=1
            )
        else:
            update = 'non-exists'
        #
        kwargs['update'] = update
        kwargs['user'] = user
        #
        kwargs.update(kwargs_extend)
        self._cleanup_rsv_entity_create_kwargs(rsv_category, kwargs)

    def get_keywords(self, regex=None):
        _ = self._patterns_dict.keys()
        if regex is not None:
            return fnmatch.filter(_, regex)
        return _

    def has_pattern(self, keyword):
        return keyword in self._patterns_dict

    def get_pattern(self, keyword):
        if keyword not in self._patterns_dict:
            raise KeyError(u'keyword: "{}" is Non-registered'.format(keyword))
        return self._patterns_dict[keyword]

    def get_pattern_opt(self, keyword):
        return bsc_core.PtnParseOpt(
            self.get_pattern(keyword)
        )

    def generate_rsv_pattern(self, keyword):
        return self.RSV_PATTERN_CLS(self.get_pattern(keyword))

    def get_variant(self, keyword):
        if keyword not in self._raw:
            raise KeyError('keyword: "{}" is Non-registered'.format(keyword))
        return self._raw[keyword]


# project
class AbsRsvProject(
    AbsRsvEntityBaseDef,
    AbsRsvConfigureExtraDef,
    unr_abstracts.AbsGuiExtraDef,
    unr_abstracts.AbsObjDagExtraDef,
):
    RSV_MATCHER_CLS = None
    #
    RSV_OBJ_STACK_CLS = None
    #
    RSV_RESOURCE_GROUP_CLS = None
    RSV_RESOURCE_CLS = None
    RSV_STEP_CLS = None
    RSV_TASK_CLS = None
    RSV_TASK_VERSION_CLS = None
    #
    RSV_UNIT_CLS = None
    RSV_UNIT_VERSION_CLS = None
    #
    RSV_APP_DEFAULT_CLS = None
    RSV_APP_NEW_CLS = None
    #
    PROPERTIES_CLS = None
    #
    CACHE = dict()

    def __init__(self, *args, **kwargs):
        self._init_entity_base_def_()
        self._init_configure_extra_def_()
        #
        project_root, project_raw = args[:2]
        #
        self._rsv_root = project_root
        self._project_raw = project_raw
        #
        self._rsv_obj_stack = self.RSV_OBJ_STACK_CLS()
        #
        self._setup_rsv_entity(
            self.PROPERTIES_CLS(self, bsc_core.DictMtd.sort_key_to(kwargs))
        )
        self._init_obj_dag_extra_def_(self._rsv_path)
        self._init_gui_extra_def_()
        #
        self._root_dict = collections.OrderedDict()
        self._root_step_choice = None
        self._root_configure = ctt_core.Content(value=collections.OrderedDict())
        #
        self._static_variant_configure = ctt_core.Content(value=collections.OrderedDict())
        #
        self._rsv_matcher = self._generate_rsv_matcher(
            self._pattern,
            self._rsv_properties.value
        )
        #
        raw = copy.copy(self._rsv_root._raw)
        raw.update(project_raw)
        self._setup_rsv_configure(raw)
        #
        self._configure = ctt_core.Content(value=self._raw)
        self._root_choices = self._configure.get('root-choices')
        self._root_step_choice = self._configure.get_as_content(
            'root-step-choice'
        )
        #
        self._project__update_all_static_variants()
        self._project__update_all_roots()
        #
        self._build_all_patterns()
        #
        self._workspace_key_mapper = {}

    def _project__completion_kwargs_from_parent_(self, rsv_category, rsv_parent, kwargs):
        path_keys = self._get_path_variant_keys(rsv_category)
        # do not override this keys
        for k, v in rsv_parent.properties.get_value().items():
            if k in path_keys:
                kwargs[k] = v

    def _project__update_all_roots(self):
        self._root_dict[self.Platforms.Windows] = self._raw_opt.get_as_unfold('project-root-windows-dir')
        self._root_dict[self.Platforms.Linux] = self._raw_opt.get_as_unfold('project-root-linux-dir')

        for i_index, i_root_choice in enumerate(self._root_choices):
            for j_platform in self.Platforms.All:
                if i_index == 0:
                    self._root_configure.set(
                        'root.{}'.format(i_root_choice, j_platform),
                        self._raw['project-{}-{}-dir'.format(i_root_choice, j_platform)]
                    )
                #
                self._root_configure.set(
                    '{}.{}'.format(i_root_choice, j_platform),
                    self._raw['project-{}-{}-dir'.format(i_root_choice, j_platform)]
                )

    def _project__update_all_static_variants(self):
        for i_variant_type_key in self.VariantCategories.All:
            i_variant_type_key_extra = '{}_extra'.format(i_variant_type_key)
            i_extras = self._raw_opt.get(i_variant_type_key_extra)
            i_variants = self._raw_opt.get(i_variant_type_key)
            if isinstance(i_variants, dict):
                for j_variant_name_key, j_value in i_variants.items():
                    j_key = '{}.{}'.format(
                        i_variant_type_key, j_variant_name_key
                    )
                    self._static_variant_configure.set(
                        j_key,
                        j_value
                    )
                    if i_extras:
                        for k_seq, k_extra in enumerate(i_extras):
                            k_key = '{}.{}'.format(
                                i_variant_type_key_extra,
                                k_extra.format(**dict(key=j_variant_name_key))
                            )
                            k_value = k_extra.format(**dict(key=j_value))
                            self._static_variant_configure.set(
                                k_key,
                                k_value
                            )

    def _project__update_roots_to_rsv_properties(self, platform_):
        for i_index, i_root_choice in enumerate(self._root_choices):
            if i_index == 0:
                self._rsv_properties.set(
                    'root',
                    self._root_configure.get('root.{}'.format(i_root_choice, platform_))
                )
            self._rsv_properties.set(
                i_root_choice,
                self._root_configure.get('{}.{}'.format(i_root_choice, platform_))
            )

    def _project_update_static_variants_to_rsv_properties(self):
        self._rsv_properties.update_from(self._static_variant_configure.get_value())

    def _project_get_workspace_key_mapper_(self):
        if not self._workspace_key_mapper:
            self._workspace_key_mapper = {v: k for k, v in self.properties.get(self.VariantCategories.Workspaces).items()}
        return self._workspace_key_mapper

    def _project__get_workspace_key_by_variants_(self, variants):
        if 'workspace_key' in variants:
            return variants['workspace_key']
        elif 'workspace' in variants:
            workspace = variants['workspace']
            workspace_key_mapper = self._project_get_workspace_key_mapper_()
            if workspace in workspace_key_mapper:
                return workspace_key_mapper[workspace]
        return self.WorkspaceKeys.Source

    def _project__get_workspace(self, **kwargs):
        if 'workspace_key' in kwargs:
            return self.to_workspace(kwargs['workspace_key'])
        elif 'workspace' in kwargs:
            return kwargs['workspace']
        return self.get_workspace_source()

    def _project__generate_workspace_args(self, variants):
        workspace_key = self._project__get_workspace_key_by_variants_(variants)
        variants['workspace_key'] = workspace_key
        workspace = self._project__get_workspace(**variants)
        variants['workspace'] = workspace
        return workspace_key, workspace

    def _project__guess_workspace(self, **kwargs):
        keyword = kwargs['keyword']
        ks = keyword.split('-')
        key = ks[1]
        if key in self.WorkspaceMatchKeys.Sources:
            return self.get_workspace_source()
        elif key in self.WorkspaceMatchKeys.Users:
            return self.get_workspace_user()
        elif key in self.WorkspaceMatchKeys.Releases:
            return self.get_workspace_release()
        elif key in self.WorkspaceMatchKeys.Temporaries:
            return self.get_workspace_temporary()
        return self.get_workspace_release()

    def _project__generate_rsv_entity_search_patterns(self, branch, entity_type):
        key = '{}-{}-search-patterns'.format(branch, entity_type)
        return collections.OrderedDict(
            [(k, self._raw_opt.unfold_value(v)) for k, v in (self._raw_opt.get(key) or {}).items()]
        )

    def _project__get_root_choice(self, variants):
        root_choice = self._root_step_choice
        if root_choice:
            if 'workspace' in variants and 'step' in variants:
                workspace_key = self._project__get_workspace_key_by_variants_(variants)
                root_choice = self._root_step_choice.get(
                    '{}.{}'.format(workspace_key, variants['step'])
                )
                if root_choice is not None:
                    return root_choice
        return 'root_primary'

    def _project__completion_rsv_matcher_variants(self, kwargs):
        # workspace
        if 'workspace' in kwargs:
            workspace = kwargs['workspace']
            # convert other workspace to "work"
            if workspace not in [
                self.get_workspace_source(),
                self.get_workspace_release(),
                # self.get_workspace_temporary()
            ]:
                kwargs['workspace'] = self.get_workspace_source()
        else:
            kwargs['workspace'] = self.get_workspace_source()
        # root_choice
        root_choice = self._project__get_root_choice(kwargs)
        kwargs['root_choice'] = root_choice
        # root
        root_cur = self._rsv_properties.get(root_choice)
        kwargs['root'] = root_cur

    def _project__generate_rsv_matcher(self, variants):
        self._project__completion_rsv_matcher_variants(variants)
        pattern = variants['pattern']
        return self._generate_rsv_matcher(pattern, variants)

    def _project__completion_main_rsv_matcher_variants(self, kwargs):
        # root_choice
        root_choice = self._project__get_root_choice(kwargs)
        kwargs['root_choice'] = root_choice
        # root
        root_cur = self._rsv_properties.get(root_choice)
        kwargs['root'] = root_cur

    def _project__generate_main_rsv_matcher(self, kwargs):
        self._project__completion_main_rsv_matcher_variants(kwargs)
        pattern = kwargs['pattern']
        return self._generate_rsv_matcher(pattern, kwargs)

    def _generate_rsv_matcher(self, pattern, variants_override):
        return self.RSV_MATCHER_CLS(
            self,
            pattern,
            variants_override
        )

    def get_rsv_root(self):
        return self._rsv_root

    rsv_root = property(get_rsv_root)

    def get_pathsep(self):
        return self.PATHSEP

    pathsep = property(get_pathsep)

    @property
    def path(self):
        return self._rsv_path

    @property
    def icon(self):
        return bsc_resource.RscExtendIcon.get('resolver/project')

    def get_all_workspaces(self):
        return self._rsv_properties.get(
            self.VariantCategories.Workspaces
        ).values()

    def to_workspace(self, workspace_key):
        return self._rsv_properties.get(
            '{}.{}'.format(self.VariantCategories.Workspaces, workspace_key)
        )

    def get_workspace_mapper(self):
        return self._rsv_properties.get(
            self.VariantCategories.Workspaces
        )

    # etc. "work"
    def get_workspace_source(self):
        return self._rsv_properties.get(
            '{}.{}'.format(self.VariantCategories.Workspaces, self.WorkspaceKeys.Source)
        )

    #
    def get_workspace_user(self):
        return self._rsv_properties.get(
            '{}.{}'.format(self.VariantCategories.Workspaces, self.WorkspaceKeys.User)
        )

    # etc. "publish"
    def get_workspace_release(self):
        return self._rsv_properties.get(
            '{}.{}'.format(self.VariantCategories.Workspaces, self.WorkspaceKeys.Release)
        )

    # etc. "output"
    def get_workspace_temporary(self):
        return self._rsv_properties.get(
            '{}.{}'.format(self.VariantCategories.Workspaces, self.WorkspaceKeys.Temporary)
        )

    def get_all_roles(self):
        return self._rsv_properties.get(
            self.VariantCategories.Roles
        ).values()

    def get_all_tags(self, branch):
        if branch == self.EntityTypes.Asset:
            return self.get_all_roles()
        elif branch == self.EntityTypes.Sequence:
            return []
        elif branch == self.EntityTypes.Shot:
            return []
        else:
            raise RuntimeError()

    def get_all_project_steps(self, with_extra=False):
        if with_extra is True:
            return self._rsv_properties.get(
                self.VariantCategories.ProjectSteps
            ).values()+(self._rsv_properties.get(
                '{}_extra'.format(
                    self.VariantCategories.ProjectSteps
                )
            ) or {}).values()
        return self._rsv_properties.get(
            self.VariantCategories.ProjectSteps
        ).values()

    def get_all_asset_steps(self, with_extra=False):
        if with_extra is True:
            return self._rsv_properties.get(
                self.VariantCategories.AssetSteps
            ).values()+(self._rsv_properties.get(
                '{}_extra'.format(
                    self.VariantCategories.AssetSteps
                )
            ) or {}).values()
        return self._rsv_properties.get(
            self.VariantCategories.AssetSteps
        ).values()

    def get_all_sequence_steps(self, with_extra=False):
        if with_extra is True:
            return self._rsv_properties.get(
                self.VariantCategories.SequenceSteps
            ).values()+(self._rsv_properties.get(
                '{}_extra'.format(
                    self.VariantCategories.SequenceSteps
                )
            ) or {}).values()
        return self._rsv_properties.get(
            self.VariantCategories.SequenceSteps
        ).values()

    def get_all_shot_steps(self, with_extra=False):
        if with_extra is True:
            return self._rsv_properties.get(
                self.VariantCategories.ShotSteps
            ).values()+(self._rsv_properties.get(
                '{}_extra'.format(
                    self.VariantCategories.ShotSteps
                )
            ) or {}).values()
        return self._rsv_properties.get(
            self.VariantCategories.ShotSteps
        ).values()

    def get_all_steps(self, branch, with_extra=False):
        if branch == self.EntityTypes.Project:
            return self.get_all_project_steps(with_extra=with_extra)
        elif branch == self.EntityTypes.Asset:
            return self.get_all_asset_steps(with_extra=with_extra)
        elif branch == self.EntityTypes.Sequence:
            return self.get_all_sequence_steps(with_extra=with_extra)
        elif branch == self.EntityTypes.Shot:
            return self.get_all_shot_steps(with_extra=with_extra)
        else:
            raise RuntimeError()

    def create_dag_fnc(self, path):
        if path == self._rsv_path:
            return self
        return self.get_rsv_entity(path)

    def _get_child_paths_(self, *args, **kwargs):
        return self._project__find_rsv_entity_child_paths(self._rsv_path)

    def _get_child_(self, path):
        return self.get_rsv_entity(path)

    def get_descendants(self):
        return self._rsv_obj_stack.get_objects()

    def get_parent(self):
        return self._rsv_root

    def get_directory_path(self):
        keyword = 'project-dir'
        rsv_pattern = self.generate_rsv_pattern(keyword)
        return rsv_pattern.update_variants(**self.properties.value)

    def get_patterns(self, regex=None):
        if regex is not None:
            return [self.get_pattern(i) for i in self.get_keywords(regex)]
        return self._patterns_dict.values()

    def get_url(self, keyword, **kwargs):
        pass

    def get_platform(self):
        return

    def get_root(self):
        return

    # resource groups
    def _project__get_rsv_resource_groups(self, **kwargs):
        list_ = []

        branch = kwargs['branch']
        if branch == self.EntityTypes.Asset:
            entity_type = self.EntityTypes.Role
        elif branch == self.EntityTypes.Shot:
            entity_type = self.EntityTypes.Sequence
        elif branch == self.EntityTypes.Sequence:
            entity_type = self.EntityTypes.Sequence
        else:
            raise TypeError()
        #
        keyword = '{}-dir'.format(entity_type)
        kwargs['keyword'] = keyword
        kwargs['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__generate_main_rsv_matcher(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        for i_m in matches:
            _, i_variants = i_m
            i_kwargs = copy.copy(kwargs)
            i_kwargs.update(i_variants)
            i_rsv_group = self._entity__get_rsv_resource_group(
                rsv_obj=self, **i_kwargs
            )
            if i_rsv_group is not None:
                if i_rsv_group not in list_:
                    list_.append(i_rsv_group)
        return list_
    
    # resource group
    def _entity__get_rsv_resource_group(self, rsv_obj, **kwargs):
        kwargs_over = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_over[k] = v

        kwargs_over.update(kwargs)

        branch = self._guess_entity_type_force(**kwargs_over)
        if branch == self.EntityTypes.Asset:
            entity_type = self.EntityTypes.Role
        elif branch == self.EntityTypes.Shot:
            entity_type = self.EntityTypes.Sequence
        elif branch == self.EntityTypes.Sequence:
            entity_type = self.EntityTypes.Sequence
        else:
            raise TypeError()

        if entity_type in kwargs_over:
            name = kwargs_over[entity_type]
            name_includes = self.get_all_tags(branch)
            if name_includes:
                if name not in name_includes:
                    return
        else:
            name = '*'

        if self._name_validation_fnc(entity_type, name) is False:
            return None
        # type
        kwargs_over['type'] = entity_type
        keyword = '{}-dir'.format(entity_type)
        kwargs_over['keyword'] = keyword
        # branch
        kwargs_over['branch'] = branch
        # asset/shot
        kwargs_over[entity_type] = name
        #
        obj_path = self._generate_rsv_entity_path(self.EntityCategories.ResourceGroup, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        variants = self._generate_rsv_entity_create_kwargs(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'branch']
        )
        return self.__create_rsv_resource_group(**variants)

    def __create_rsv_resource_group(self, **kwargs):
        rsv_matcher = self._project__generate_main_rsv_matcher(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            rsv_category = self.EntityCategories.Resource
            entity_type = kwargs['branch']
            self._completion_rsv_entity_create_kwargs(
                rsv_category, entity_type,
                kwargs, result, variants
            )
            rsv_obj = self.RSV_RESOURCE_GROUP_CLS(self, **kwargs)
            self._project__add_rsv_entity(rsv_obj)
            return rsv_obj

    # resources
    def _project__get_rsv_resources(self, **kwargs):
        list_ = []
        kwargs_over = copy.copy(kwargs)
        branch = kwargs_over['branch']
        #
        entity_type = branch
        p = None
        if entity_type in kwargs:
            p_ = kwargs[entity_type]
            if '*' in p_:
                p = p_
                kwargs.pop(entity_type)
        #
        keyword = '{}-dir'.format(entity_type)
        kwargs_over['keyword'] = keyword
        kwargs_over['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__generate_main_rsv_matcher(
            kwargs_over
        )
        matches = rsv_matcher.get_matches()
        for i_m in matches:
            i_result, i_variants = i_m
            if p is not None:
                i_name = i_variants[entity_type]
                if not bsc_core.PtnFnmatchMtd.filter([i_name], p):
                    continue
            i_kwargs_over = copy.copy(kwargs_over)
            i_kwargs_over.update(i_variants)
            i_rsv_resource = self._resource_group__get_rsv_resource(**i_kwargs_over)
            if i_rsv_resource is not None:
                if i_rsv_resource not in list_:
                    list_.append(i_rsv_resource)
        return list_

    # resource
    def __completion_rsv_resource_kwargs(self, rsv_obj, **kwargs):
        kwargs_over = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_over[k] = v
        #
        kwargs_over.update(kwargs)
        #
        branch = self._guess_entity_type_force(**kwargs_over)
        entity_type = branch
        if entity_type in kwargs_over:
            name = kwargs_over[entity_type]
        else:
            raise KeyError()
        #
        if self._name_validation_fnc(entity_type, name) is False:
            return None
        # type
        kwargs_over['type'] = entity_type
        keyword = '{}-dir'.format(entity_type)
        kwargs_over['keyword'] = keyword
        # branch
        kwargs_over['branch'] = branch
        # asset/shot
        kwargs_over[branch] = name
        return kwargs_over

    def __generate_rsv_resource_create_kwargs(self, rsv_obj, **kwargs):
        kwargs_over = self.__completion_rsv_resource_kwargs(rsv_obj, **kwargs)
        if kwargs_over is None:
            return None
        obj_path = self._generate_rsv_entity_path(self.EntityCategories.Resource, kwargs_over)
        return self._generate_rsv_entity_create_kwargs(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'branch']
        )

    def _entity__get_rsv_resource(self, rsv_obj, **kwargs):
        kwargs_over = self.__completion_rsv_resource_kwargs(rsv_obj, **kwargs)
        if kwargs_over is None:
            return None

        obj_path = self._generate_rsv_entity_path(self.EntityCategories.Resource, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)

        create_kwargs = self._generate_rsv_entity_create_kwargs(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'branch']
        )
        return self.__create_rsv_resource(**create_kwargs)

    def _resource_group__get_rsv_resource(self, **kwargs):
        rsv_resource_group = self.get_rsv_resource_group(**kwargs)
        if rsv_resource_group:
            return rsv_resource_group.get_rsv_resource(**kwargs)

    def __create_rsv_resource(self, **kwargs):
        rsv_matcher = self._project__generate_main_rsv_matcher(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            rsv_category = self.EntityCategories.Resource
            entity_type = kwargs['branch']
            result, variants = matches[-1]
            self._completion_rsv_entity_create_kwargs(
                rsv_category, entity_type,
                kwargs, result, variants
            )
            rsv_obj = self.RSV_RESOURCE_CLS(self, **kwargs)
            self._project__add_rsv_entity(rsv_obj)
            return rsv_obj

    # steps
    def _project__get_rsv_steps(self, **kwargs):
        list_ = []
        #
        entity_type = self.EntityTypes.Step
        p = None
        if entity_type in kwargs:
            p_ = kwargs[entity_type]
            if '*' in p_:
                p = p_
                kwargs.pop(entity_type)
        #
        branch = self._guess_entity_type_force(**kwargs)
        search_patterns = self._project__generate_rsv_entity_search_patterns(branch, entity_type)
        for i_workspace_key, i_pattern_args in search_patterns.items():
            i_kwargs_over = copy.copy(kwargs)
            i_kwargs_over['pattern'] = i_pattern_args
            i_kwargs_over['workspace'] = self.to_workspace(i_workspace_key)
            i_rsv_matcher = self._project__generate_main_rsv_matcher(
                i_kwargs_over
            )
            i_matches = i_rsv_matcher.get_matches()
            for j_match in i_matches:
                j_result, j_variants = j_match
                if p is not None:
                    j_name = j_variants[entity_type]
                    if not bsc_core.PtnFnmatchMtd.filter([j_name], p):
                        continue
                j_kwargs_over = self._copy_variants_as_branches_(i_kwargs_over)
                j_kwargs_over.update(j_variants)
                j_kwargs_over['resolver_workspace_key'] = i_workspace_key
                j_kwargs_over['resolver_pattern'] = i_pattern_args
                j_kwargs_over['resolver_result'] = j_result
                # project task
                if branch in self.EntityTypes.Projects:
                    j_rsv_step = self._project__get_rsv_step(**j_kwargs_over)
                # etc. sequence step
                elif branch in self.EntityTypes.ResourceGroups:
                    j_rsv_step = self._resource_group__get_rsv_step(**j_kwargs_over)
                # etc. asset step
                elif branch in self.EntityTypes.Resources:
                    j_rsv_step = self._resource__get_rsv_step(**j_kwargs_over)
                else:
                    raise RuntimeError()
                if j_rsv_step is not None:
                    if j_rsv_step not in list_:
                        list_.append(j_rsv_step)
        return list_

    # step, step may be a project step / sequence step / asset step / shot step
    def _entity__get_rsv_step(self, rsv_obj, **kwargs):
        kwargs_over = self._copy_variants_as_branches_(
            rsv_obj.properties.get_value()
        )
        #
        kwargs_over.update(kwargs)
        #
        entity_type = self.EntityTypes.Step
        rsv_category = self.EntityCategories.Step
        kwargs_over['type'] = entity_type
        if entity_type in kwargs_over:
            name = kwargs_over[entity_type]
            kwargs_over[entity_type] = name
            #
            branch = self._guess_entity_type_force(**kwargs_over)
            name_includes = self.get_all_steps(
                branch, with_extra=True
            )
            if name_includes:
                if name not in name_includes:
                    return None
        else:
            raise KeyError(
                'key "{}" must assign a value'.format(entity_type)
            )
        #
        obj_path = self._generate_rsv_entity_path(rsv_category, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        return self.__create_rsv_step_auto(**kwargs_over)
    
    def _project__get_rsv_step(self, **kwargs):
        rsv_entity = self
        return self._entity__get_rsv_step(rsv_entity, **kwargs)

    def _resource_group__get_rsv_step(self, **kwargs):
        rsv_entity = self.get_rsv_resource_group(**kwargs)
        if rsv_entity is not None:
            return self._entity__get_rsv_step(rsv_entity, **kwargs)

    def _resource__get_rsv_step(self, **kwargs):
        rsv_entity = self.get_rsv_resource(**kwargs)
        if rsv_entity is not None:
            return self._entity__get_rsv_step(rsv_entity, **kwargs)

    def __create_rsv_step_auto(self, **kwargs):
        # kwargs from upstream
        if 'resolver_result' in kwargs:
            return self.__create_rsv_step(**kwargs)
        return self.__search_rsv_step(**kwargs)

    def __search_rsv_step(self, **kwargs):
        entity_type = self.EntityTypes.Step
        branch = self._guess_entity_type_force(**kwargs)
        search_patterns = self._project__generate_rsv_entity_search_patterns(branch, entity_type)
        for i_workspace_key, i_pattern_args in search_patterns.items():
            i_kwargs_over = copy.copy(kwargs)
            i_kwargs_over['pattern'] = i_pattern_args
            i_kwargs_over['workspace'] = self.to_workspace(i_workspace_key)
            i_rsv_matcher = self._project__generate_main_rsv_matcher(
                i_kwargs_over
            )
            i_matches = i_rsv_matcher.get_matches()
            for j_match in i_matches:
                j_result, j_variants = j_match
                j_kwargs_over = self._copy_variants_as_branches_(i_kwargs_over)
                j_kwargs_over.update(j_variants)
                j_kwargs_over['resolver_workspace_key'] = i_workspace_key
                j_kwargs_over['resolver_pattern'] = i_pattern_args
                j_kwargs_over['resolver_result'] = j_result
                j_rsv_step = self.__create_rsv_step(**j_kwargs_over)
                if j_rsv_step is not None:
                    return j_rsv_step
        return None

    def __create_rsv_step(self, **kwargs):
        rsv_category = self.EntityCategories.Step
        entity_type = self.EntityTypes.Step
        #
        result = kwargs.pop('resolver_result')
        kwargs['workspace_key'] = kwargs.pop('resolver_workspace_key')
        kwargs['pattern'] = kwargs.pop('resolver_pattern')
        variants = dict()
        self._completion_rsv_entity_create_kwargs(
            rsv_category, entity_type,
            kwargs, result, variants
        )
        rsv_obj = self.RSV_STEP_CLS(self, **kwargs)
        self._project__add_rsv_entity(rsv_obj)
        return rsv_obj

    # tasks
    def _project__get_rsv_tasks(self, **kwargs):
        list_ = []
        #
        entity_type = self.EntityTypes.Task
        p = None
        if entity_type in kwargs:
            p_ = kwargs[entity_type]
            if '*' in p_:
                p = p_
                kwargs.pop(entity_type)
        #
        branch = self._guess_entity_type_force(**kwargs)
        search_patterns = self._project__generate_rsv_entity_search_patterns(branch, entity_type)
        for i_workspace_key, i_pattern in search_patterns.items():
            i_kwargs_over = copy.copy(kwargs)
            i_kwargs_over['pattern'] = i_pattern
            i_kwargs_over['workspace'] = self.to_workspace(i_workspace_key)
            i_rsv_matcher = self._project__generate_main_rsv_matcher(
                i_kwargs_over
            )

            i_matches = i_rsv_matcher.get_matches()
            for j_match in i_matches:
                j_result, j_variants = j_match
                if p is not None:
                    j_name = j_variants[entity_type]
                    if not bsc_core.PtnFnmatchMtd.filter([j_name], p):
                        continue
                j_kwargs_over = self._copy_variants_as_branches_(i_kwargs_over)
                j_kwargs_over.update(j_variants)
                j_kwargs_over['resolver_workspace_key'] = i_workspace_key
                j_kwargs_over['resolver_pattern'] = i_pattern
                j_kwargs_over['resolver_result'] = j_result
                j_rsv_task = self._step__get_rsv_task(**j_kwargs_over)
                if j_rsv_task is not None:
                    if j_rsv_task not in list_:
                        list_.append(j_rsv_task)
        return list_

    # task
    def _entity__get_rsv_task(self, rsv_obj, **kwargs):
        rsv_category = self.EntityCategories.Task
        entity_type = self.EntityTypes.Task
        #
        kwargs_over = self._copy_variants_as_branches_(
            rsv_obj.properties.get_value()
        )
        #
        kwargs_over.update(kwargs)
        #
        kwargs_over['type'] = entity_type
        if entity_type in kwargs_over:
            name = kwargs_over[entity_type]
            kwargs_over[entity_type] = name
        else:
            raise KeyError()
        obj_path = self._generate_rsv_entity_path(rsv_category, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        return self.__create_rsv_task_auto(**kwargs_over)

    def _step__get_rsv_task(self, **kwargs):
        rsv_entity = self.get_rsv_step(**kwargs)
        if rsv_entity is not None:
            if isinstance(rsv_entity, AbsRsvStep):
                return self._entity__get_rsv_task(rsv_entity, **kwargs)

    def __create_rsv_task_auto(self, **kwargs):
        if 'resolver_result' in kwargs:
            return self.__create_rsv_task(**kwargs)
        return self.__search_rsv_task(**kwargs)

    def __search_rsv_task(self, **kwargs):
        entity_type = self.EntityTypes.Task
        branch = self._guess_entity_type_force(**kwargs)
        search_patterns = self._project__generate_rsv_entity_search_patterns(branch, entity_type)
        for i_workspace_key, i_pattern_args in search_patterns.items():
            i_kwargs_over = copy.copy(kwargs)
            i_kwargs_over['pattern'] = i_pattern_args
            i_kwargs_over['workspace'] = self.to_workspace(i_workspace_key)
            i_rsv_matcher = self._project__generate_main_rsv_matcher(
                i_kwargs_over
            )
            i_matches = i_rsv_matcher.get_matches()
            for j_match in i_matches:
                j_result, j_variants = j_match
                j_kwargs_over = self._copy_variants_as_branches_(i_kwargs_over)
                j_kwargs_over.update(j_variants)
                j_kwargs_over['resolver_workspace_key'] = i_workspace_key
                j_kwargs_over['resolver_pattern'] = i_pattern_args
                j_kwargs_over['resolver_result'] = j_result
                j_rsv_task = self.__create_rsv_task(**j_kwargs_over)
                if j_rsv_task is not None:
                    return j_rsv_task
        return None

    def __create_rsv_task(self, **kwargs):
        rsv_category = self.EntityCategories.Task
        entity_type = self.EntityTypes.Task
        result = kwargs.pop('resolver_result')
        kwargs['workspace_key'] = kwargs.pop('resolver_workspace_key')
        kwargs['pattern'] = kwargs.pop('resolver_pattern')
        variants = dict()
        self._completion_rsv_entity_create_kwargs(
            rsv_category, entity_type,
            kwargs, result, variants
        )
        rsv_obj = self.RSV_TASK_CLS(self, **kwargs)
        self._project__add_rsv_entity(rsv_obj)
        return rsv_obj

    # task versions
    def _project__get_rsv_task_versions_(self, **kwargs):
        list_ = []
        #
        entity_type = self.EntityTypes.Version
        branch = self._guess_entity_type_force(**kwargs)
        #
        workspace_key, workspace = self._project__generate_workspace_args(kwargs)
        #
        keyword = '{}-{}-{}-dir'.format(branch, workspace_key, entity_type)
        kwargs['keyword'] = keyword
        kwargs['pattern'] = self.get_pattern(keyword=keyword)
        rsv_matcher = self._project__generate_main_rsv_matcher(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        for i_m in matches:
            _, i_variants = i_m
            i_kwargs = copy.copy(kwargs)
            i_kwargs.update(i_variants)
            #
            i_rsv_version = self._task__get_rsv_version(**i_kwargs)
            if i_rsv_version is not None:
                if i_rsv_version not in list_:
                    list_.append(i_rsv_version)
        return list_

    # task version
    def _entity__get_rsv_task_version(self, rsv_obj, **kwargs):
        kwargs_over = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_over[k] = v
        #
        kwargs_over.update(kwargs)
        #
        entity_type = self.EntityTypes.Version
        branch = self._guess_entity_type_force(**kwargs_over)
        #
        workspace_key, workspace = self._project__generate_workspace_args(kwargs)
        keyword = '{}-{}-{}-dir'.format(branch, workspace_key, entity_type)
        if entity_type in kwargs_over:
            name = kwargs_over[entity_type]
        else:
            raise KeyError()
        #
        if self._name_validation_fnc(entity_type, name) is False:
            return None
        #
        kwargs_over['type'] = entity_type
        kwargs_over['keyword'] = keyword
        kwargs_over[entity_type] = name
        #
        obj_path = self._generate_rsv_version_path(rsv_obj.path, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        variants = self._generate_rsv_entity_create_kwargs(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'branch']
        )
        return self.__create_rsv_task_version(**variants)

    def _task__get_rsv_version(self, **kwargs):
        rsv_entity = self.get_rsv_task(**kwargs)
        if rsv_entity is not None:
            return self._entity__get_rsv_task_version(rsv_entity, **kwargs)

    def __create_rsv_task_version(self, **kwargs):
        rsv_matcher = self._project__generate_main_rsv_matcher(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self._completion_rsv_entity_extend_create_kwargs(kwargs, result, variants)
            rsv_obj = self.RSV_TASK_VERSION_CLS(self, **kwargs)
            self._project__add_rsv_entity(rsv_obj)
            return rsv_obj
    
    # unit
    def _entity__get_rsv_unit(self, rsv_obj, **kwargs):
        kwargs_over = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_over[k] = v
        #
        kwargs_over.update(kwargs)
        #
        entity_type = 'unit'
        kwargs_over['type'] = entity_type
        keyword = self._completion_keyword(kwargs_over)
        kwargs_over['keyword'] = keyword
        if 'platform' not in kwargs_over:
            kwargs_over['platform'] = bsc_core.SysBaseMtd.get_platform()
        #
        if 'version' not in kwargs_over:
            kwargs_over['version'] = rsv_core.RsvVersion.LATEST
        #
        workspace = self._project__guess_workspace(**kwargs_over)
        kwargs_over['workspace'] = workspace
        workspace_key = self._project__get_workspace_key_by_variants_(kwargs_over)
        kwargs_over['workspace_key'] = workspace_key
        obj_path = self._generate_rsv_unit_path(rsv_obj.path, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        variants = self._generate_rsv_entity_create_kwargs(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'platform', 'application', 'branch', 'workspace', 'workspace_key', 'keyword']
        )
        return self.__create_rsv_unit(**variants)

    def __create_rsv_unit(self, **kwargs):
        rsv_obj = self.RSV_UNIT_CLS(self, **kwargs)
        self._project__add_rsv_entity(rsv_obj)
        return rsv_obj

    # unit version
    def _entity__get_rsv_unit_version(self, rsv_obj, **kwargs):
        kwargs_over = collections.OrderedDict()
        for k, v in rsv_obj.properties.value.items():
            kwargs_over[k] = v
        #
        kwargs_over.update(kwargs)
        #
        entity_type = 'version'
        keyword = rsv_obj.get('keyword')
        #
        if entity_type in kwargs_over:
            name = kwargs_over[entity_type]
        else:
            raise KeyError()
        #
        if self._name_validation_fnc(entity_type, name) is False:
            return None
        #
        kwargs_over['type'] = entity_type
        kwargs_over['keyword'] = keyword
        kwargs_over[entity_type] = name
        #
        obj_path = self._generate_rsv_version_path(rsv_obj.path, kwargs_over)
        if self._rsv_obj_stack.get_object_exists(obj_path) is True:
            return self._rsv_obj_stack.get_object(obj_path)
        #
        variants = self._generate_rsv_entity_create_kwargs(
            obj_path,
            kwargs_over,
            extend_keys=['type', 'branch']
        )
        return self.__create_rsv_unit_version(**variants)

    def __create_rsv_unit_version(self, **kwargs):
        rsv_matcher = self._project__generate_rsv_matcher(
            kwargs
        )
        matches = rsv_matcher.get_matches()
        if matches:
            result, variants = matches[-1]
            self._completion_rsv_entity_extend_create_kwargs(kwargs, result, variants)
            rsv_obj = self.RSV_UNIT_VERSION_CLS(self, **kwargs)
            self._project__add_rsv_entity(rsv_obj)
            return rsv_obj

    def get_rsv_resource_groups(self, **kwargs):
        branch = self._guess_entity_type(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_resource_groups(**kwargs)
        else:
            list_ = []
            for i_branch in self.EntityTypes.Resources:
                kwargs['branch'] = i_branch
                list_.extend(
                    self._project__get_rsv_resource_groups(**kwargs)
                )
            return list_

    def get_rsv_resource_group(self, **kwargs):
        return self._entity__get_rsv_resource_group(
            rsv_obj=self, **kwargs
        )

    def get_rsv_resources(self, **kwargs):
        branch = self._guess_entity_type(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            list_ = []
            if self.EntityTypes.Role in kwargs or self.EntityTypes.Sequence in kwargs:
                rsv_resource_group = self.get_rsv_resource_group(**kwargs)
                list_.extend(
                    rsv_resource_group.get_rsv_resources(**kwargs)
                )
            else:
                rsv_tags = self.get_rsv_resource_groups(**kwargs)
                for i_rsv_tag in rsv_tags:
                    list_.extend(
                        i_rsv_tag.get_rsv_resources(**kwargs)
                    )
            return list_
        else:
            list_ = []
            for i_branch in self.EntityTypes.Resources:
                kwargs['branch'] = i_branch
                i_rsv_tags = self.get_rsv_resource_groups(branch=i_branch)
                for j_rsv_tag in i_rsv_tags:
                    list_.extend(j_rsv_tag.get_rsv_resources())
            return list_

    def get_rsv_resource(self, **kwargs):
        # find resource
        branch = self._guess_entity_type_force(**kwargs)
        if branch in self.EntityTypes.Resources:
            if self.EntityTypes.Role in kwargs or self.EntityTypes.Sequence in kwargs:
                return self._resource_group__get_rsv_resource(**kwargs)
            # find in all resource group
            _ = self.get_rsv_resources(**kwargs)
            if _:
                return _[-1]
        else:
            _ = self.get_rsv_resources(**kwargs)
            if _:
                return _[-1]

    def get_rsv_steps(self, **kwargs):
        branch = self._guess_entity_type(**kwargs)
        kwargs['branch'] = branch
        return self._project__get_rsv_steps(**kwargs)

    def get_rsv_step(self, **kwargs):
        branch = self._guess_entity_type_force(**kwargs)
        if branch in self.EntityTypes.Projects:
            return self._project__get_rsv_step(**kwargs)
        elif branch in self.EntityTypes.ResourceGroups:
            return self._resource_group__get_rsv_step(**kwargs)
        elif branch in self.EntityTypes.Resources:
            return self._resource__get_rsv_step(**kwargs)

    def get_rsv_task(self, **kwargs):
        if 'step' in kwargs:
            return self._step__get_rsv_task(**kwargs)
        #
        _ = self._project__get_rsv_tasks(**kwargs)
        if _:
            return _[-1]

    def get_rsv_tasks(self, **kwargs):
        branch = self._guess_entity_type_force(**kwargs)
        kwargs['branch'] = branch
        return self._project__get_rsv_tasks(**kwargs)

    def get_rsv_task_version(self, **kwargs):
        if 'version' in kwargs:
            return self._task__get_rsv_version(**kwargs)
        #
        _ = self.get_rsv_task_versions(**kwargs)
        if _:
            return _[-1]

    def get_rsv_task_versions(self, **kwargs):
        branch = self._guess_entity_type_force(**kwargs)
        if branch is not None:
            kwargs['branch'] = branch
            return self._project__get_rsv_task_versions_(**kwargs)
        else:
            list_ = []
            for i_branch in self.EntityTypes.Resources:
                kwargs['branch'] = i_branch
                list_.extend(
                    self._project__get_rsv_task_versions_(**kwargs)
                )
            return list_

    # unit
    def get_rsv_task_unit(self, **kwargs):
        rsv_task = self.get_rsv_task(**kwargs)
        if rsv_task is not None:
            return rsv_task.get_rsv_unit(**kwargs)

    def get_rsv_unit(self, **kwargs):
        return self._entity__get_rsv_unit(
            self, **kwargs
        )

    # app
    def get_rsv_app(self, application):
        configure = ctt_core.Content(value=self.get_package_data())
        scheme = configure.get('scheme')
        if scheme == 'default':
            return self.RSV_APP_DEFAULT_CLS(
                rsv_project=self,
                application=application,
                configure=configure
            )
        elif scheme == 'new':
            return self.RSV_APP_NEW_CLS(
                rsv_project=self,
                application=application,
                configure=configure
            )

    def get_framework_scheme(self):
        return self._raw_opt.get('schemes.framework')

    def get_package_data(self):
        return self._raw_opt.get('package-data')

    def get_storage_scheme(self):
        return self._raw_opt.get('schemes.storage')

    def get_dcc_data(self, application):
        main_data = self._raw_opt.get_content_as_unfold(
            'dcc-data.{}'.format(application)
        )
        extend_data = self._raw_opt.get('dcc-data.dcc-extend') or {}
        extend_c = ctt_core.Content(value=extend_data)
        for i_k in extend_c.get_all_leaf_keys():
            i_v = extend_c.get(i_k)
            main_data.set(
                i_k, i_v.format(**main_data.value)
            )
        extend_data_over = self._raw_opt.get('dcc-data.{}-extend'.format(application)) or {}
        if extend_data_over:
            extend_data_over_c = ctt_core.Content(value=extend_data_over)
            for i_k in extend_data_over_c.get_all_leaf_keys():
                i_v = extend_data_over_c.get(i_k)
                main_data.set(
                    i_k, i_v.format(**main_data.value)
                )
        return main_data

    def get_rsv_entity_exists(self, rsv_obj_path):
        return self._rsv_obj_stack.get_object_exists(rsv_obj_path)

    def _project__add_rsv_entity(self, rsv_obj):
        self._rsv_obj_stack.set_object_add(rsv_obj)
        if rsv_core.RESULT_ENABLE is True:
            bsc_log.Log.trace_method_result(
                'resolver',
                '{}="{}"'.format(rsv_obj.type, rsv_obj.path)
            )

    def get_rsv_entity(self, path):
        if path == '/':
            return self._rsv_root
        elif path == self.get_path():
            return self
        return self._rsv_obj_stack.get_object(path)

    def get_rsv_entities(self, regex=None):
        return self._rsv_obj_stack.get_objects(regex)

    def _project__find_rsv_entity_child_paths(self, path):
        return bsc_core.PthNodeMtd.find_dag_child_paths(path, self._rsv_obj_stack.get_keys())

    def _project__find_rsv_entity_children(self, path):
        child_paths = bsc_core.PthNodeMtd.find_dag_child_paths(path, self._rsv_obj_stack.get_keys())
        return [self._rsv_obj_stack.get_object(i) for i in child_paths]

    def get_rsv_resource_by_any_file_path(self, file_path, variants_override=None):
        return self._project__find_rsv_resource_by_any_file_path(file_path, variants_override)

    def _project__find_rsv_resource_by_any_file_path(self, file_path, variants_override=None):
        if file_path is not None:
            for i_branch in self.EntityTypes.Resources:
                i_pattern = self.get_pattern(keyword='{}-dir'.format(i_branch))
                i_pattern_extra = '{}/{{extra}}'.format(i_pattern)
                i_patterns = [
                    i_pattern, i_pattern_extra
                ]
                for j_pattern in i_patterns:
                    j_rsv_matcher = self._generate_rsv_matcher(
                        j_pattern, variants_override
                    )
                    j_properties = j_rsv_matcher.generate_properties_by_result(result=file_path)
                    if j_properties:
                        j_properties.set('branch', i_branch)
                        j_rsv_entity = self.get_rsv_resource(**j_properties.value)
                        return j_rsv_entity

    def get_rsv_step_by_any_file_path(self, file_path):
        return self._project__find_rsv_step_by_any_file_path(file_path)

    def _project__find_rsv_step_by_any_file_path(self, file_path):
        if file_path is not None:
            entity_type = self.EntityTypes.Step
            for i_branch in self.EntityTypes.Projects+self.EntityTypes.ResourceGroups+self.EntityTypes.Resources:
                search_pattern = self._project__generate_rsv_entity_search_patterns(i_branch, entity_type)
                for j_workspace_key in self.WorkspaceKeys.All:
                    if j_workspace_key in search_pattern:
                        j_pattern = search_pattern[j_workspace_key]
                        if '{format}' not in j_pattern:
                            j_pattern_extra = '{}/{{extra}}'.format(j_pattern)
                        else:
                            j_pattern_extra = j_pattern
                        #
                        j_rsv_matcher = self._generate_rsv_matcher(
                            j_pattern_extra, variants_override={}
                        )
                        j_properties = j_rsv_matcher.generate_properties_by_result(result=file_path)
                        if j_properties:
                            j_kwargs_over = self._copy_variants_as_branches_(j_properties.get_value())
                            j_kwargs_over['resolver_workspace_key'] = j_workspace_key
                            j_kwargs_over['resolver_pattern'] = j_pattern
                            j_kwargs_over['resolver_result'] = file_path
                            i_rsv_step = self.get_rsv_step(**j_kwargs_over)
                            if i_rsv_step is not None:
                                return i_rsv_step

    def get_rsv_task_by_any_file_path(self, file_path):
        return self._project__find_rsv_task_by_any_file_path(file_path)

    def _project__find_rsv_task_by_any_file_path(self, file_path):
        if file_path is not None:
            entity_type = self.EntityTypes.Task
            for i_branch in self.EntityTypes.Resources:
                search_pattern = self._project__generate_rsv_entity_search_patterns(i_branch, entity_type)
                for j_workspace_key in self.WorkspaceKeys.All:
                    if j_workspace_key in search_pattern:
                        j_pattern = search_pattern[j_workspace_key]
                        if '{format}' not in j_pattern:
                            j_pattern_extra = '{}/{{extra}}'.format(j_pattern)
                        else:
                            j_pattern_extra = j_pattern
                        j_rsv_matcher = self._generate_rsv_matcher(
                            j_pattern_extra, variants_override={}
                        )
                        j_properties = j_rsv_matcher.generate_properties_by_result(result=file_path)
                        if j_properties:
                            j_kwargs_over = self._copy_variants_as_branches_(j_properties.get_value())
                            j_kwargs_over['resolver_workspace_key'] = j_workspace_key
                            j_kwargs_over['resolver_pattern'] = j_pattern
                            j_kwargs_over['resolver_result'] = file_path
                            i_rsv_task = self.get_rsv_task(**j_kwargs_over)
                            if i_rsv_task is not None:
                                return i_rsv_task

    # output
    def get_rsv_task_by_output_file_path(self, file_path):
        return self._project__find_rsv_task_by_any_file_path(
            file_path,
            variants_override=dict(workspace=self.get_workspace_temporary())
        )

    def restore_all_gui_variants(self):
        for i in self._rsv_obj_stack.get_objects():
            i.set_obj_gui(None)

    def create_resource_directory(self, **kwargs):
        rsv_resource_group = self.get_rsv_resource_group(**kwargs)
        create_kwargs = self.__generate_rsv_resource_create_kwargs(
            rsv_resource_group, **kwargs
        )

        p = create_kwargs['pattern']

        p_o = bsc_core.PtnParseOpt(
            p
        ).update_variants_to(
            **create_kwargs
        )
        if not p_o.get_keys():
            stg_path = p_o.get_value()
            if bsc_storage.StgFileMtd.get_is_exists(stg_path) is False:
                bsc_storage.StgPathPermissionMtd.create_directory(
                    stg_path
                )

    def auto_create_user_task_directory_by_task_data(self, task_data):
        branch = self._guess_entity_type_force(**task_data)
        variants_over = copy.copy(task_data)

        user = bsc_core.SysBaseMtd.get_user_name()
        variants_over['artist'] = user
        keyword = '{branch}-user-task-dir'.format(branch=branch)

        self._project__completion_main_rsv_matcher_variants(variants_over)

        workspace = self._project__guess_workspace(keyword=keyword)
        variants_over['workspace'] = workspace

        ptn = self.get_pattern(keyword)
        ptn_opt = bsc_core.PtnParseOpt(ptn)
        ptn_opt.set_update(**variants_over)
        if not ptn_opt.get_keys():
            directory_path = ptn_opt.get_value()
            if bsc_storage.StgPathMtd.get_is_exists(directory_path) is False:
                bsc_storage.StgPathPermissionMtd.create_directory(
                    directory_path, mode='755'
                )
                bsc_storage.StgPathPermissionMtd.change_owner(
                    directory_path, user=user, group='artists'
                )

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()


# root
class AbsRsvRoot(
    AbsRsvConfigureExtraDef,
    unr_abstracts.AbsGuiExtraDef,
    unr_abstracts.AbsObjDagExtraDef,
):
    OBJ_UNIVERSE_CLS = None

    RSV_PROJECT_STACK_CLS = None
    RSV_PROJECT_CLS = None

    RSV_VERSION_KEY_CLS = None

    @classmethod
    def get_platform(cls):
        if platform.system() == 'Windows':
            return 'windows'
        elif platform.system() == 'Linux':
            return 'linux'

    def __init__(self):
        self._init_configure_extra_def_()
        self._init_obj_dag_extra_def_('/')
        self._init_gui_extra_def_()
        #
        self._rsv_project_stack = self.RSV_PROJECT_STACK_CLS()
        self._obj_universe = self.OBJ_UNIVERSE_CLS()
        #
        raw = rsv_core.RsvConfigure.get_basic_raw()
        self._setup_rsv_configure(raw)
        #
        self._default_root_to_project_dict = {}
        #
        self._build_all_patterns()
        self._build_all_projects_()

    def _build_all_projects_(self):
        default_raws = rsv_core.RsvConfigure.get_all_default_raws()
        for i_raw in default_raws:
            i_project_raw_opt = self._generate_rsv_configure_opt(i_raw)
            key = i_project_raw_opt.get('key')
            if key is not None:
                projects = i_project_raw_opt.get('projects-include') or []
                for j_project in projects:
                    j_raw = copy.copy(i_raw)
                    j_project_raw_opt = self._generate_rsv_configure_opt(j_raw)
                    j_project_raw_opt.set('key', j_project)
                    self._root__get_rsv_project(j_raw, project=j_project)

    def get_type(self):
        return 'resolver'

    type = property(get_type)

    def get_type_name(self):
        return self.get_type()

    type_name = property(get_type_name)

    def get_pathsep(self):
        return self.PATHSEP

    pathsep = property(get_pathsep)

    def get_path(self):
        return self.PATHSEP

    path = property(get_path)

    @property
    def name(self):
        return ''

    @property
    def icon(self):
        return bsc_resource.RscExtendIcon.get('resolver/root')

    def create_dag_fnc(self, path):
        if path == self.path:
            return self

    def _get_child_paths_(self, *args, **kwargs):
        return self._rsv_project_stack.get_keys()

    def _get_child_(self, path):
        return self._rsv_project_stack.get_object(path)

    @property
    def pattern_dict(self):
        return self._patterns_dict

    def get_rsv_projects(self):
        return self._rsv_project_stack.get_objects()

    def get_rsv_project(self, *args, **kwargs):
        return self._root__get_exists_project(*args, **kwargs)

    def get_rsv_project_is_exists(self, **kwargs):
        return

    def _root__get_rsv_project(self, *args, **kwargs):
        kwargs_over = collections.OrderedDict()
        kwargs_over.update(kwargs)
        entity_type = 'project'
        if entity_type in kwargs_over:
            name = kwargs_over[entity_type]
        else:
            raise KeyError()
        #
        kwargs_over['type'] = entity_type
        kwargs_over[entity_type] = name
        keyword = '{}-dir'.format(entity_type)
        kwargs_over['keyword'] = keyword
        #
        obj_path = self._generate_rsv_entity_path(self.EntityCategories.Project, kwargs_over)
        if self._rsv_project_stack.get_object_exists(obj_path) is True:
            rsv_project = self._rsv_project_stack.get_object(obj_path)
            if 'platform' in kwargs_over:
                rsv_project._project__update_roots_to_rsv_properties(kwargs_over['platform'])
            else:
                rsv_project._project__update_roots_to_rsv_properties(platform_=self.get_platform())
            #
            rsv_project._project_update_static_variants_to_rsv_properties()
            return rsv_project
        #
        variants = self._generate_rsv_entity_create_kwargs(
            obj_path,
            kwargs_over,
            extend_keys=['type']
        )
        return self._root__create_rsv_project(*args, **variants)

    def _root__get_exists_project(self, **kwargs):
        kwargs_over = collections.OrderedDict()
        kwargs_over.update(kwargs)
        entity_type = 'project'
        if entity_type in kwargs_over:
            name = kwargs_over[entity_type]
        else:
            raise KeyError()
        #
        kwargs_over['type'] = entity_type
        kwargs_over[entity_type] = name
        keyword = '{}-dir'.format(entity_type)
        kwargs_over['keyword'] = keyword
        #
        obj_path = self._generate_rsv_entity_path(self.EntityCategories.Project, kwargs_over)
        if self._rsv_project_stack.get_object_exists(obj_path) is True:
            rsv_project = self._rsv_project_stack.get_object(obj_path)
            if 'platform' in kwargs_over:
                rsv_project._project__update_roots_to_rsv_properties(kwargs_over['platform'])
            else:
                rsv_project._project__update_roots_to_rsv_properties(platform_=self.get_platform())
            #
            rsv_project._project_update_static_variants_to_rsv_properties()
            return rsv_project

    def _root__create_rsv_project(self, *args, **kwargs):
        rsv_project = self.RSV_PROJECT_CLS(self, *args, **kwargs)
        rsv_project._project__update_roots_to_rsv_properties(platform_=self.get_platform())
        rsv_project._project_update_static_variants_to_rsv_properties()
        obj_type = rsv_project.type
        obj_path = rsv_project.path
        self._rsv_project_stack.set_object_add(rsv_project)
        if rsv_core.RESULT_ENABLE is True:
            bsc_log.Log.trace_method_result(
                'resolver',
                u'{}="{}"'.format(obj_type, obj_path)
            )
        return rsv_project

    # scene
    def get_rsv_project_by_any_file_path(self, file_path):
        return self._root__get_rsv_project_by_any_file_path(file_path)

    def _root__get_rsv_project_by_any_file_path(self, file_path):
        rsv_projects = self.get_rsv_projects()
        for i_rsv_project in rsv_projects:
            i_project = i_rsv_project.get('project')
            for j_platform in self.Platforms.All:
                j_root = i_rsv_project.get_pattern('project-root-{}-dir'.format(j_platform))
                j_glob_pattern = '{}/*'.format(j_root)
                j_results = fnmatch.filter([file_path.lower()], j_glob_pattern)
                if j_results:
                    j_variants = {'root': j_root}
                    j_keyword = 'project-dir'
                    j_pattern = i_rsv_project.get_pattern(j_keyword)
                    j_pattern_ = '{}/{{extra}}'.format(j_pattern)
                    j_variants['keyword'] = j_keyword
                    j_variants['pattern'] = j_pattern_
                    j_rsv_matcher = i_rsv_project._generate_rsv_matcher(
                        j_pattern_, j_variants
                    )
                    j_project_rsv_properties = j_rsv_matcher.generate_properties_by_result(file_path)
                    if j_project_rsv_properties:
                        j_project = j_project_rsv_properties.get('project')
                        if j_project == i_project:
                            i_rsv_project.properties.set('platform', j_platform)
                            i_rsv_project.properties.set('root', j_root)
                            return i_rsv_project
        #
        return self._root__get_rsv_project_as_default(file_path)

    # = rsv_project.get_rsv_resources
    def get_rsv_resources(self, **kwargs):
        kwargs_over = self._completion_rsv_kwargs(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_resources(**kwargs_over)

    # = rsv_project.get_rsv_resource
    def get_rsv_resource(self, **kwargs):
        kwargs_over = self._completion_rsv_kwargs(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_resource(**kwargs_over)

    #
    def get_rsv_step(self, **kwargs):
        kwargs_over = self._completion_rsv_kwargs(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_step(**kwargs_over)

    # = rsv_project.get_rsv_task
    def get_rsv_task(self, **kwargs):
        kwargs_over = self._completion_rsv_kwargs(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_task(**kwargs_over)

    def get_rsv_tasks(self, **kwargs):
        kwargs_over = self._completion_rsv_kwargs(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_tasks(**kwargs_over)

    def get_rsv_task_version(self, **kwargs):
        kwargs_over = self._completion_rsv_kwargs(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_task_version(**kwargs_over)

    # = rsv_project.get_rsv_unit
    def get_rsv_unit(self, **kwargs):
        kwargs_over = self._completion_rsv_kwargs(**kwargs)
        if kwargs_over:
            rsv_project = self.get_rsv_project(**kwargs_over)
            if rsv_project:
                return rsv_project.get_rsv_unit(**kwargs_over)

    def get_result(self, **kwargs):
        rsv_unit = self.get_rsv_unit(**kwargs)
        return rsv_unit.get_result(
            version=kwargs['version'],
            variants_extend=kwargs
        )

    def get_rsv_resource_by_any_file_path(self, file_path):
        rsv_project = self._root__get_rsv_project_by_any_file_path(file_path)
        if rsv_project is not None:
            return rsv_project._project__find_rsv_resource_by_any_file_path(
                file_path
            )
        else:
            if rsv_core.WARNING_ENABLE is True:
                bsc_log.Log.trace_method_warning(
                    'project-resolver',
                    u'file="{}" is not available'.format(file_path)
                )
        return None

    def get_rsv_step_by_any_file_path(self, file_path):
        rsv_project = self._root__get_rsv_project_by_any_file_path(file_path)
        if rsv_project is not None:
            return rsv_project._project__find_rsv_step_by_any_file_path(
                file_path
            )
        else:
            if rsv_core.WARNING_ENABLE is True:
                bsc_log.Log.trace_method_warning(
                    'project-resolver',
                    u'file="{}" is not available'.format(file_path)
                )
        return None

    def get_rsv_task_by_any_file_path(self, file_path):
        rsv_project = self._root__get_rsv_project_by_any_file_path(file_path)
        if rsv_project is not None:
            return rsv_project._project__find_rsv_task_by_any_file_path(
                file_path
            )
        else:
            if rsv_core.WARNING_ENABLE is True:
                bsc_log.Log.trace_method_warning(
                    'project-resolver',
                    u'file="{}" is not available'.format(file_path)
                )
        return None

    def _root__get_rsv_project_as_default(self, file_path):
        rsv_project = self.get_rsv_project(project='default')
        if rsv_project is not None:
            for i_platform in self.Platforms.All:
                i_root = rsv_project.get_pattern('project-root-{}-dir'.format(i_platform))
                i_glob_pattern = '{}/*'.format(i_root)
                i_results = fnmatch.filter([file_path.lower()], i_glob_pattern)
                if i_results:
                    i_variants = {'root': i_root}
                    i_pattern = rsv_project.get_pattern('project-dir')
                    i_pattern_ = '{}/{{extra}}'.format(i_pattern)
                    i_rsv_matcher = rsv_project._generate_rsv_matcher(
                        i_pattern_, i_variants
                    )
                    i_project_properties = i_rsv_matcher._generate_default_project_properties_by_result(file_path)
                    i_project = i_project_properties.get('project')
                    if rsv_core.RESULT_ENABLE is True:
                        bsc_log.Log.trace_method_result(
                            'resolver project create',
                            'project-name="{}", create use "default"'.format(i_project)
                        )
                    return self.get_rsv_project(project=i_project)

    def get_task_properties_by_work_scene_src_file_path(self, file_path):
        _ = self._get_rsv_task_properties_by_work_scene_src_file_path_(file_path)
        if _ is not None:
            return _
        else:
            if rsv_core.WARNING_ENABLE is True:
                bsc_log.Log.trace_method_warning(
                    'work-scene-src-file-resolver',
                    u'file="{}" is not available'.format(file_path)
                )
        return None

    def _get_rsv_task_properties_by_work_scene_src_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_work_scene_src_file_path(file_path)

    def get_task_properties_by_scene_src_file_path(self, file_path):
        _ = self._get_rsv_task_properties_by_scene_src_file_path_(file_path)
        if _ is not None:
            return _
        else:
            if rsv_core.WARNING_ENABLE is True:
                bsc_log.Log.trace_method_warning(
                    'scene-src-file-resolver',
                    'file="{}" is not available'.format(file_path)
                )
        return None

    def _get_rsv_task_properties_by_scene_src_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_scene_src_file_path(file_path)

    def _get_rsv_task_properties_by_scene_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_scene_file_path(file_path)

    def _get_rsv_task_properties_by_output_scene_src_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_output_scene_src_file_path(file_path)

    def _get_rsv_task_properties_by_output_scene_file_path_(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_properties_by_output_scene_file_path(file_path)

    def get_task_properties_by_any_scene_file_path(self, file_path):
        methods = [
            self._get_rsv_task_properties_by_work_scene_src_file_path_,
            self._get_rsv_task_properties_by_scene_src_file_path_,
            self._get_rsv_task_properties_by_scene_file_path_,
            self._get_rsv_task_properties_by_output_scene_src_file_path_,
            self._get_rsv_task_properties_by_output_scene_file_path_,
        ]
        for method in methods:
            # noinspection PyArgumentList
            result = method(bsc_storage.StgPathOpt(file_path).get_path())
            if result is not None:
                # print(';'.join(['{}={}'.format(k, v) for k, v in result.value.items() if isinstance(v, six.string_types)]))
                return result

    def get_rsv_resource_step_directory_paths(self, **kwargs):
        list_ = []
        project = kwargs['project']
        rsv_project = self.get_rsv_project(project=project)
        branch = rsv_project._guess_entity_type_force(**kwargs)
        keywords = [self._generate_step_keyword(branch, i) for i in self.WorkspaceKeys.Mains]
        for i_keyword in keywords:
            i_kwargs = rsv_project.properties.get_value_as_copy()
            i_kwargs.update(kwargs)
            i_rsv_pattern = rsv_project.generate_rsv_pattern(i_keyword)
            i_workspace = rsv_project._project__guess_workspace(keyword=i_keyword)
            i_kwargs['workspace'] = i_workspace
            i_result = i_rsv_pattern.update_variants(**i_kwargs)
            list_.append(i_result)
        return list_

    def get_rsv_resource_task_directory_paths(self, **kwargs):
        list_ = []
        project = kwargs['project']
        rsv_project = self.get_rsv_project(project=project)
        branch = rsv_project._guess_entity_type_force(**kwargs)
        keywords = [self._generate_task_keyword(branch, i) for i in self.WorkspaceKeys.Mains]
        #
        for i_keyword in keywords:
            i_kwargs = rsv_project.properties.value_as_copy
            i_kwargs.update(kwargs)
            i_rsv_pattern = rsv_project.generate_rsv_pattern(i_keyword)
            i_workspace = rsv_project._project__guess_workspace(keyword=i_keyword)
            i_kwargs['workspace'] = i_workspace
            i_result = i_rsv_pattern.update_variants(**i_kwargs)
            list_.append(i_result)
        return list_

    def get_rsv_scene_properties_by_any_scene_file_path(self, file_path):
        rsv_task = self.get_rsv_task_by_any_file_path(file_path)
        if rsv_task is not None:
            return rsv_task.get_rsv_scene_properties_by_any_scene_file_path(file_path)

    def get_new_version_key(self, version):
        version_key = self.RSV_VERSION_KEY_CLS(version)
        version_key += 1
        return version_key

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()
