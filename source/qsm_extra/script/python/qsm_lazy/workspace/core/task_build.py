# coding:utf-8
import lxbasic.content as bsc_content


class TaskBuild(object):
    def __init__(self, task_parse, variants):
        self._task_parse = task_parse
        self._properties = bsc_content.DictProperties(variants)

    def execute(self):
        raise NotImplementedError()
