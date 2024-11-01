# coding:utf-8
import copy

import lxbasic.core as bsc_core

import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

import qsm_general.core as qsm_gnl_core


class TaskParse(object):
    INSTANCE = None

    @classmethod
    def to_project_path(cls, **kwargs):
        return '/{project}'.format(
            **kwargs
        )

    @classmethod
    def to_entity_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']

        return '/{project}/{entity}'.format(
            **kwargs
        )

    @classmethod
    def to_task_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']

        return '/{project}/{entity}/{step}.{task}'.format(
            **kwargs
        )

    @classmethod
    def to_task_unit_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']

        return '/{project}/{entity}/{step}.{task}/{task_unit}'.format(
            **kwargs
        )

    @classmethod
    def to_source_task_scene_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']

        return (
            '/{project}/{entity}/{step}.{task}/{task_unit}/{entity}.{step}.{task}.{task_unit}.v{version}.{file_format}'
        ).format(
            **kwargs
        )

    @classmethod
    def generate_session_for_auto(cls):
        return None
    
    @classmethod
    def generate_session_for_scene(cls, scene_path):
        return None

    def __init__(self):
        if qsm_gnl_core.scheme_is_release():
            configure_key = 'lazy-workspace/task/default'
        else:
            configure_key = 'lazy-workspace/task/default'

        self._configure = bsc_resource.RscExtendConfigure.get_as_content(configure_key)

        self._configure.do_flatten()

        self._properties = bsc_content.DictProperties(
            root_source=self._configure.get('root_source.windows'),
            root_temporary=self._configure.get('root_temporary.windows'),
            root_release=self._configure.get('root_release.windows')
        )

        self._task_ptn_opt = bsc_core.BscStgParseOpt(
            self._configure.get('patterns.asset-source-task-dir')
        ).update_variants_to(**self._properties)
        self._task_unit_ptn_opt = bsc_core.BscStgParseOpt(
            self._configure.get('patterns.asset-source-task_unit-dir')
        ).update_variants_to(**self._properties)
        self._task_scene_ptn_opt = bsc_core.BscStgParseOpt(
            self._configure.get('patterns.asset-source-task_scene-file')
        ).update_variants_to(**self._properties)
        self._task_scene_thumbnail_ptn_opt = bsc_core.BscStgParseOpt(
            self._configure.get('patterns.asset-source-task_scene-thumbnail-file')
        ).update_variants_to(**self._properties)

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        instance = super(TaskParse, cls).__new__(cls)
        cls.INSTANCE = instance
        return instance

    @property
    def properties(self):
        return self._properties

    @property
    def configure(self):
        return self._configure

    @property
    def task_pattern_opt(self):
        return self._task_ptn_opt

    def generate_pattern_opt_for(self, keyword, **kwargs):
        kwargs.update(**self._properties)
        return bsc_core.BscStgParseOpt(
            self._configure.get('patterns.{}'.format(keyword))
        ).update_variants_to(**kwargs)

    def generate_task_pattern_opt_for(self, **kwargs):
        return self._task_ptn_opt.update_variants_to(**kwargs)

    @property
    def task_unit_pattern_opt(self):
        return self._task_unit_ptn_opt

    def generate_task_unit_pattern_opt_for(self, **kwargs):
        return self._task_unit_ptn_opt.update_variants_to(**kwargs)

    @property
    def task_scene_pattern_opt(self):
        return self._task_scene_ptn_opt

    def generate_task_scene_pattern_opt_for(self, **kwargs):
        return self._task_scene_ptn_opt.update_variants_to(**kwargs)

    @property
    def task_scene_thumbnail_ptn_opt(self):
        return self._task_scene_thumbnail_ptn_opt

    def generate_task_scene_thumbnail_pattern_opt_for(self, **kwargs):
        return self._task_scene_thumbnail_ptn_opt.update_variants_to(**kwargs)
