# coding:utf-8
import copy

import lxbasic.content as bsc_content


class TaskSession(object):

    INSTANCE = None

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
    def task_unit_path(self):
        return self._task_parse.to_task_unit_path(**self._properties)

    @property
    def scene_src_path(self):
        return self._task_parse.to_source_scene_src_path(**self._properties)

    def save_source_task_scene(self, *args, **kwargs):
        return False

    def get_file_for(self, keyword, **kwargs):
        kwargs_new = copy.copy(self._properties)
        kwargs_new.update(**kwargs)
        return self._task_parse.generate_pattern_opt_for(
            keyword, **kwargs_new
        ).get_value()

    def generate_pattern_opt(self):
        pass

    def get_latest_file_for(self, keyword, **kwargs):
        kwargs_new = copy.copy(self._properties)
        kwargs_new.pop('version')
        kwargs_new.update(**kwargs)

        ptn_opt = self._task_parse.generate_pattern_opt_for(
            keyword, **kwargs_new
        )

        matches = ptn_opt.find_matches(sort=True)
        if matches:
            return matches[-1]['result']
        return None

    def generate_asset_release_new_version_number(self, **kwargs):
        kwargs_new = copy.copy(self._properties)
        kwargs_new.update(**kwargs)
        return self._task_parse.generate_asset_release_new_version_number(
            **kwargs_new
        )
