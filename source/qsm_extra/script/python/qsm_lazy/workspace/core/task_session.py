# coding:utf-8
import lxbasic.content as bsc_content


class TaskSession(object):

    INSTANCE = None

    def __init__(self, task_parse, variants):
        self._task_parse = task_parse
        self._properties = bsc_content.DictProperties(variants)

    def __new__(cls, task_parse, variants):
        if cls.INSTANCE is not None:
            instance = cls.INSTANCE
            instance.update_properties(variants)
            return instance

        instance = super(TaskSession, cls).__new__(cls, task_parse, variants)
        cls.INSTANCE = instance
        return instance

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
    def task_scene_path(self):
        return self._task_parse.to_source_task_scene_path(**self._properties)

    @classmethod
    def task_scene(cls):
        return

    def save_source_task_scene(self, *args, **kwargs):
        return False
