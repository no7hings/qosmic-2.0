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
    def to_source_scene_src_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']

        return (
            '/{project}/{entity}/{step}.{task}/{task_unit}/{entity}.{step}.{task}.{task_unit}.v{version}.ma'
        ).format(
            **kwargs
        )

    @classmethod
    def generate_task_session_by_asset_source_scene_src_auto(cls):
        return None
    
    @classmethod
    def generate_task_session_by_asset_source_scene_src(cls, scene_path):
        return None

    def __init__(self):
        if qsm_gnl_core.scheme_is_release():
            configure_key = 'lazy-workspace/task/default'
        else:
            configure_key = 'lazy-workspace/task/default'

        self._configure = bsc_resource.RscExtendConfigure.get_as_content(configure_key)

        self._configure.do_flatten()

        self._space_dict = self._configure.get('spaces')

        self._properties = bsc_content.DictProperties(
            root_source=self._configure.get('root_source.windows'),
            root_temporary=self._configure.get('root_temporary.windows'),
            root_release=self._configure.get('root_release.windows')
        )

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

    def generate_pattern_opt_for(self, keyword, **kwargs):
        kwargs_new = copy.copy(kwargs)
        _ = keyword.split('-')
        kwargs_new.update(**self._properties)
        resource_type = _[0]
        kwargs_new['resource_type'] = resource_type
        space_key = _[1]
        kwargs_new['space_key'] = space_key
        space = self._space_dict[space_key]
        kwargs_new['space'] = space
        return bsc_core.BscStgParseOpt(
            self._configure.get('patterns.{}'.format(keyword))
        ).update_variants_to(**kwargs_new)

    # source
    @property
    def asset_source_task_scene_pattern_opt(self):
        return self.generate_pattern_opt_for(
            'asset-source-scene_src-maya-file'
        )

    def generate_asset_source_task_scene_pattern_opt_for(self, **kwargs):
        return self.generate_pattern_opt_for(
            'asset-source-scene_src-maya-file', **kwargs
        )

    @property
    def asset_source_task_scene_thumbnail_ptn_opt(self):
        return self.generate_pattern_opt_for(
            'asset-source-scene_src-maya-thumbnail-file'
        )

    def generate_asset_source_task_scene_thumbnail_pattern_opt_for(self, **kwargs):
        return self.generate_pattern_opt_for(
            'asset-source-scene_src-maya-thumbnail-file', **kwargs
        )

    # release
    @property
    def asset_release_task_scene_pattern_opt(self):
        return self.generate_pattern_opt_for(
            'asset-release-scene_src-maya-file'
        )

    def generate_asset_release_new_version_number(self, **kwargs):
        kwargs_new = copy.copy(kwargs)
        kwargs_new.pop('version')

        release_task_version_ptn_opt = self.generate_pattern_opt_for(
            'asset-release-task_version-dir', **kwargs_new
        )

        matches = release_task_version_ptn_opt.find_matches(sort=True)
        if matches:
            version_latest = int(matches[-1]['version'])
            return version_latest+1
        return 1
