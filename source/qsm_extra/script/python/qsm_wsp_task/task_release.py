# coding:utf-8
import lxbasic.content as bsc_content


class DccTaskReleaseOpt(object):
    def __init__(self, task_session, variants):
        self._task_session = task_session
        self._properties = bsc_content.DictProperties(variants)

    def __str__(self):
        return '{}{}'.format(
            self.__class__.__name__,
            str(self._properties)
        )

    def release_scene_src(self, *args, **kwargs):
        raise NotImplementedError()
