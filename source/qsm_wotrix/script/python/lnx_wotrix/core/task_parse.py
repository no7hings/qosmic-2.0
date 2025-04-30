# coding:utf-8
import copy

import sys

import lxbasic.core as bsc_core

import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

import lnx_parsor.parse as lnx_prs_parse

from . import task_session as _task_session


# todo: support to each project different stage?
class TaskParse(object):
    EntityTypes = lnx_prs_parse.Stage.EntityTypes
    SpaceKeys = lnx_prs_parse.Stage.SpaceKeys
    ResourceTypes = lnx_prs_parse.Stage.ResourceTypes

    Roots = lnx_prs_parse.Stage.Roots
    Spaces = lnx_prs_parse.Stage.Spaces
    Steps = lnx_prs_parse.Stage.Steps
    Tasks = lnx_prs_parse.Stage.Tasks

    INSTANCE = None

    TASK_SESSION_CLS = _task_session.TaskSession

    @classmethod
    def generate_task_session_by_resource_source_scene_src_auto(cls):
        return None

    @classmethod
    def generate_task_session_by_resource_source_scene_src(cls, application, scene_path, **kwargs_over):
        task_parse = cls()

        for i_resource_type in cls.ResourceTypes.All:
            i_ptn_opt = task_parse.generate_pattern_opt_for(
                '{}-source-{}-scene_src-file'.format(i_resource_type, application)
            )
            i_variants = i_ptn_opt.get_variants(scene_path, extract=True)
            if i_variants:
                if kwargs_over:
                    i_variants.update(kwargs_over)
                # do not pop result
                # i_variants.pop('result')
                i_variants['resource_type'] = i_resource_type
                return cls.TASK_SESSION_CLS(task_parse, i_variants)
    
    @classmethod
    def autosave_source_scene_scr(cls):
        return False

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(TaskParse, cls).__new__(cls)

        self._parse_stage = lnx_prs_parse.Stage(scheme='default')
        self.Roots = self._parse_stage.Roots
        self.Spaces = self._parse_stage.Spaces
        self.Steps = self._parse_stage.Steps
        self.Tasks = self._parse_stage.Tasks

        self._parse_configure = self._parse_stage.configure

        self._dcc_configure = bsc_resource.BscExtendConfigure.get_as_content('parsor/dcc/default')
        self._dcc_configure.do_flatten()

        self._properties = bsc_content.DictProperties(self._parse_stage.variants)

        cls.INSTANCE = self
        return self

    @classmethod
    def variants_factor(cls, variants):
        dict_ = {}
        for k, v in variants.items():
            dict_[k] = bsc_core.ensure_string(v)
        return dict_

    @classmethod
    def to_project_path(cls, **kwargs):
        return '/{project}'.format(
            **kwargs
        )

    def to_scan_resource_path(self, **variants):
        resource_type = variants['resource_type']
        variants_new = copy.copy(variants)
        if resource_type == self.ResourceTypes.Project:
            return u'/{project}'.format(
                **variants_new
            )
        elif resource_type == self.ResourceTypes.Asset:
            return u'/{project}/{role}/{asset}'.format(
                **variants_new
            )
        elif resource_type == self.ResourceTypes.Sequence:
            return u'/{project}/{sequence}'.format(
                **variants_new
            )
        elif resource_type == self.ResourceTypes.Shot:
            return u'/{project}/{sequence}/{shot}'.format(
                **variants_new
            )
        else:
            raise RuntimeError()

    def to_wsp_resource_path(self, **variants):
        resource_type = variants['resource_type']
        ptn = self._parse_configure.get('workspace.path_pattern.{}'.format(resource_type))
        if ptn:
            return ptn.format(**variants)
        else:
            raise RuntimeError()

    def to_wsp_task_path(self, **variants):
        resource_type = variants['resource_type']
        ptn = self._parse_configure.get('workspace.path_pattern.{}_task'.format(resource_type))
        if ptn:
            return ptn.format(**variants)
        else:
            raise RuntimeError()

    def to_wsp_task_unit_path(self, **variants):
        resource_type = variants['resource_type']
        ptn = self._parse_configure.get('workspace.path_pattern.{}_task_unit'.format(resource_type))
        if ptn:
            return ptn.format(**variants)
        else:
            raise RuntimeError()

    def to_wsp_task_unit_scene_path(self, **variants):
        resource_type = variants['resource_type']
        ptn = self._parse_configure.get('workspace.path_pattern.{}_task_unit_scene'.format(resource_type))
        if ptn:
            return ptn.format(**variants)
        else:
            raise RuntimeError()

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
        space = self._parse_stage._to_space(space_key)
        kwargs_new['space'] = space

        key = 'patterns.{}.{}.{}'.format(
            resource_type, space, '-'.join(keys[2:])
        )
        value = self._parse_configure.get(key)
        if value:
            return bsc_core.BscTaskParseOpt(
                value
            ).update_variants_to(**kwargs_new)
        else:
            raise RuntimeError(
                sys.stderr.write(
                    'pattern: {} is not found.\n'.format(keyword)
                )
            )

    # source
    @property
    def asset_source_task_scene_src_pattern_opt(self):
        return self.generate_pattern_opt_for(
            'asset-source-maya-scene_src-file'
        )

    def generate_source_task_unit_pattern_opt_for(self, application, **variants):
        resource_type = variants['resource_type']
        return self.generate_pattern_opt_for(
            '{}-source-{}-dir'.format(resource_type, application), **variants
        )

    def generate_source_task_scene_src_pattern_opt_for(self, application, **variants):
        resource_type = variants['resource_type']
        return self.generate_pattern_opt_for(
            '{}-source-{}-scene_src-file'.format(resource_type, application), **variants
        )

    def generate_source_task_thumbnail_pattern_opt_for(self, application, **variants):
        resource_type = variants['resource_type']
        return self.generate_pattern_opt_for(
            '{}-source-{}-thumbnail-file'.format(resource_type, application), **variants
        )

    def generate_asset_release_new_version_number(self, **kwargs):
        kwargs_new = copy.copy(kwargs)
        kwargs_new.pop('version')

        release_task_version_ptn_opt = self.generate_pattern_opt_for(
            'asset-release-version-dir', **kwargs_new
        )

        matches = release_task_version_ptn_opt.find_matches(sort=True)
        if matches:
            version_latest = int(matches[-1]['version'])
            return version_latest+1
        return 1

    def generate_shot_release_new_version_number(self, **kwargs):
        kwargs_new = copy.copy(kwargs)
        kwargs_new.pop('version')

        release_task_version_ptn_opt = self.generate_pattern_opt_for(
            'shot-release-version-dir', **kwargs_new
        )

        matches = release_task_version_ptn_opt.find_matches(sort=True)
        if matches:
            version_latest = int(matches[-1]['version'])
            return version_latest+1
        return 1
