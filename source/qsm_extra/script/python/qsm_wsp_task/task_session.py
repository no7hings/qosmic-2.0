# coding:utf-8
import copy

import lxbasic.content as bsc_content


class TaskSession(object):

    INSTANCE = None

    ASSET_CREATE_OPT_DICT = {}
    SHOT_CREATE_OPT_DICT = {}

    def generate_task_create_opt(self):
        raise NotImplementedError()

    def generate_task_tool_opt(self):
        raise NotImplementedError()

    def generate_task_release_opt(self):
        raise NotImplementedError()

    def __init__(self, task_parse, variants):
        self._task_parse = task_parse
        self._properties = bsc_content.DictProperties(variants)

    def __new__(cls, task_parse, variants):
        if cls.INSTANCE is not None:
            instance = cls.INSTANCE
            # update properties
            instance.update_properties(variants)
            return instance

        instance = super(TaskSession, cls).__new__(cls, task_parse, variants)
        cls.INSTANCE = instance
        return instance

    def __str__(self):
        return '{}{}'.format(
            self.__class__.__name__,
            str(self._properties)
        )

    def update_properties(self, variants):
        self._properties.clear()
        self._properties.update(variants)

    @property
    def properties(self):
        return self._properties

    @property
    def entity_path(self):
        return self._task_parse.to_entity_path(**self._properties)

    @property
    def resource_path(self):
        return self._task_parse.to_resource_path(**self._properties)

    @property
    def scan_resource_path(self):
        return self._task_parse.to_scan_resource_path(**self._properties)

    @property
    def task_unit_path(self):
        return self._task_parse.to_task_unit_path(**self._properties)

    @property
    def scene_src_path(self):
        return self._task_parse.to_source_scene_src_path(**self._properties)

    @property
    def resource_branch(self):
        return self._properties['resource_branch']
    
    def save_source_task_scene_src(self, *args, **kwargs):
        return False

    def increment_and_save_source_task_scene_src(self, *args, **kwargs):
        return False

    def generate_pattern_opt_for(self, keyword, **kwargs):
        return self._task_parse.generate_pattern_opt_for(keyword, **kwargs)

    def generate_file_variants_for(self, keyword, file_path):
        ptn_opt = self._task_parse.generate_pattern_opt_for(
            keyword
        )
        return ptn_opt.get_variants(file_path, extract=True)

    def get_file_for(self, keyword, **kwargs):
        kwargs_new = copy.copy(self._properties)
        kwargs_new.update(**kwargs)
        ptn_opt = self._task_parse.generate_pattern_opt_for(
            keyword, **kwargs_new
        )
        if not ptn_opt.get_keys():
            return ptn_opt.get_value()
        else:
            matches = ptn_opt.find_matches(sort=True)
            if matches:
                return matches[-1]['result']

    def get_latest_file_for(self, keyword, **kwargs):
        kwargs_new = copy.copy(self._properties)
        kwargs_new.update(**kwargs)
        # remove version key latest
        kwargs_new.pop('version')

        ptn_opt = self._task_parse.generate_pattern_opt_for(
            keyword, **kwargs_new
        )

        matches = ptn_opt.find_matches(sort=True)
        if matches:
            return matches[-1]['result']
        return None

    def generate_release_new_version_number(self, **kwargs):
        kwargs_new = copy.copy(self._properties)
        kwargs_new.update(**kwargs)
        resource_branch = kwargs_new['resource_branch']
        if resource_branch == 'asset':
            return self._task_parse.generate_asset_release_new_version_number(
                **kwargs_new
            )
        elif resource_branch == 'shot':
            return self._task_parse.generate_shot_release_new_version_number(
                **kwargs_new
            )
        else:
            raise RuntimeError()

    def get_last_release_scene_src_file(self):
        if self.resource_branch == 'asset':
            return self.get_latest_file_for(
                'asset-release-maya-scene_src-file'
            )
        elif self.resource_branch == 'shot':
            return self.get_latest_file_for(
                'shot-release-maya-scene_src-file'
            )
        else:
            raise RuntimeError()
