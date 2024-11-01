# coding:utf-8
import lxbasic.content as bsc_content


class DccTaskWorker(object):
    def __init__(self, task_parse, variants):
        self._task_parse = task_parse
        self._properties = bsc_content.DictProperties(variants)

    def create_groups_for(self, task):
        raise NotImplementedError()

