# coding:utf-8
import copy

import lxbasic.content as bsc_content


class DccTaskCreateOpt(object):
    RESOURCE_TYPE = None

    STEP = None
    TASK = None

    def __init__(self, task_session, variants):
        self._task_session = task_session
        self._properties = bsc_content.DictProperties(variants)

    @classmethod
    def generate_task_properties(cls, resource_properties):
        kwargs_new = copy.copy(resource_properties)
        kwargs_new['step'] = cls.STEP
        kwargs_new['task'] = cls.TASK
        return kwargs_new

    @classmethod
    def generate_scene_src_args(cls, resource_properties, task_parse, task_unit, application):
        step, task = cls.STEP, cls.TASK

        kwargs = copy.copy(resource_properties)
        kwargs['step'] = step
        kwargs['task'] = task
        kwargs['task_unit'] = task_unit
        if 'version' in kwargs:
            kwargs.pop('version')

        task_scene_ptn_opt = task_parse.generate_source_task_scene_src_pattern_opt_for(
            application=application,
            **kwargs
        )

        matches = task_scene_ptn_opt.find_matches(sort=True)
        if matches:
            last_version = int(matches[-1]['version'])
            version = last_version+1
        else:
            version = 1

        kwargs_new = copy.copy(kwargs)

        kwargs_new['version'] = str(version).zfill(3)

        task_scene_ptn_opt_new = task_parse.generate_source_task_scene_src_pattern_opt_for(
            application=application,
            **kwargs_new
        )

        scene_src_path = task_scene_ptn_opt_new.get_value()
        print scene_src_path

        thumbnail_ptn_opt_new = task_parse.generate_source_task_thumbnail_pattern_opt_for(
            application=application,
            **kwargs_new
        )
        thumbnail_path = thumbnail_ptn_opt_new.get_value()

        kwargs_new['result'] = scene_src_path

        task_session = task_parse.generate_task_session_by_resource_source_scene_src(scene_src_path)

        task_create_opt = task_session.generate_opt_for(cls)
        return task_create_opt, kwargs_new, scene_src_path, thumbnail_path

    def build_scene_src_fnc(self, *args, **kwargs):
        raise NotImplementedError()

    def create_groups_for(self, task):
        raise NotImplementedError()
