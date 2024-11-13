# coding:utf-8
import copy

import lxbasic.core as bsc_core

import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

import qsm_general.core as qsm_gnl_core

from . import task_session as _task_session


class TaskParse(object):
    INSTANCE = None

    TASK_SESSION_CLS = _task_session.TaskSession

    @classmethod
    def to_project_path(cls, **kwargs):
        return '/{project}'.format(
            **kwargs
        )
    
    @classmethod
    def to_scan_resource_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']
            return '/{project}/{asset}'.format(
                **kwargs
            )
        elif 'shot' in kwargs:
            return '/{project}/{sequence}/{shot}'.format(
                **kwargs
            )
        else:
            raise RuntimeError()

    @classmethod
    def to_resource_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']
            return '/{project}/{asset}'.format(
                **kwargs
            )
        elif 'shot' in kwargs:
            return '/{project}/{shot}'.format(
                **kwargs
            )
        else:
            raise RuntimeError()

    @classmethod
    def to_entity_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']
            return '/{project}/{asset}'.format(
                **kwargs
            )
        elif 'shot' in kwargs:
            return '/{project}/{shot}'.format(
                **kwargs
            )
        else:
            raise RuntimeError()

    @classmethod
    def to_task_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']
        elif 'shot' in kwargs:
            kwargs['entity'] = kwargs['shot']
        return '/{project}/{entity}/{step}.{task}'.format(
            **kwargs
        )

    @classmethod
    def to_task_unit_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']
        elif 'shot' in kwargs:
            kwargs['entity'] = kwargs['shot']
        return '/{project}/{entity}/{step}.{task}/{task_unit}'.format(
            **kwargs
        )

    @classmethod
    def to_source_scene_src_path(cls, **kwargs):
        kwargs = copy.copy(kwargs)
        if 'asset' in kwargs:
            kwargs['entity'] = kwargs['asset']
        elif 'shot' in kwargs:
            kwargs['entity'] = kwargs['shot']
        return (
            '/{project}/{entity}/{step}.{task}/{task_unit}/{entity}.{step}.{task}.{task_unit}.v{version}.ma'
        ).format(
            **kwargs
        )

    @classmethod
    def generate_task_session_by_resource_source_scene_src_auto(cls):
        return None

    @classmethod
    def generate_task_session_by_resource_source_scene_src(cls, scene_path):
        task_parse = cls()

        for i_resource_branch in [
            'asset', 'shot'
        ]:
            i_ptn_opt = task_parse.generate_pattern_opt_for(
                '{}-source-maya-scene_src-file'.format(i_resource_branch)
            )
            i_variants = i_ptn_opt.get_variants(scene_path, extract=True)
            if i_variants:
                i_variants['resource_branch'] = i_resource_branch
                return cls.TASK_SESSION_CLS(task_parse, i_variants)

    def __init__(self):
        if qsm_gnl_core.scheme_is_release():
            configure_key = 'wsp_task/default'
        else:
            configure_key = 'wsp_task/default'

        self._parse_configure = bsc_resource.RscExtendConfigure.get_as_content('wsp_task/parse/default')
        self._parse_configure.do_flatten()

        self._dcc_configure = bsc_resource.RscExtendConfigure.get_as_content('wsp_task/dcc/default')
        self._dcc_configure.do_flatten()

        self._space_dict = self._parse_configure.get('spaces')

        self._properties = bsc_content.DictProperties(
            root_disorder=self._parse_configure.get('roots.disorder.windows'),
            root_source=self._parse_configure.get('roots.source.windows'),
            root_temporary=self._parse_configure.get('roots.temporary.windows'),
            root_release=self._parse_configure.get('roots.release.windows')
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
    def parse_configure(self):
        return self._parse_configure

    @property
    def dcc_configure(self):
        return self._dcc_configure

    def generate_pattern_opt_for(self, keyword, **kwargs):
        kwargs_new = copy.copy(kwargs)
        keys = keyword.split('-')
        kwargs_new.update(**self._properties)
        resource_type = keys[0]
        kwargs_new['resource_type'] = resource_type
        space_key = keys[1]
        kwargs_new['space_key'] = space_key
        space = self._space_dict[space_key]
        kwargs_new['space'] = space

        key = 'patterns.{}.{}.{}'.format(
            resource_type, space, '-'.join(keys[2:])
        )
        return bsc_core.BscTaskParseOpt(
            self._parse_configure.get(key)
        ).update_variants_to(**kwargs_new)

    # source
    @property
    def asset_source_task_scene_src_pattern_opt(self):
        return self.generate_pattern_opt_for(
            'asset-source-maya-scene_src-file'
        )

    def generate_resource_source_task_scene_src_pattern_opt_for(self, **kwargs):
        if 'asset' in kwargs:
            return self.generate_pattern_opt_for(
                'asset-source-maya-scene_src-file', **kwargs
            )
        elif 'shot' in kwargs:
            return self.generate_pattern_opt_for(
                'shot-source-maya-scene_src-file', **kwargs
            )
        else:
            raise RuntimeError()

    def generate_resource_source_task_scene_src_thumbnail_pattern_opt_for(self, **kwargs):
        if 'asset' in kwargs:
            return self.generate_pattern_opt_for(
                'asset-source-maya-thumbnail-file', **kwargs
            )
        elif 'shot' in kwargs:
            return self.generate_pattern_opt_for(
                'shot-source-maya-thumbnail-file', **kwargs
            )
        else:
            raise RuntimeError()

    # release
    @property
    def asset_release_task_scene_src_pattern_opt(self):
        return self.generate_pattern_opt_for(
            'asset-release-maya-scene_src-file'
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
