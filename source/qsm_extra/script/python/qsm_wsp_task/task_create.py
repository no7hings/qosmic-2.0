# coding:utf-8
import lxbasic.content as bsc_content


class DccTaskCreateOpt(object):
    def __init__(self, task_session, variants):
        self._task_session = task_session
        self._properties = bsc_content.DictProperties(variants)

    def build_scene_src(self, *args, **kwargs):
        raise NotImplementedError()

    def create_groups_for(self, task):
        raise NotImplementedError()
