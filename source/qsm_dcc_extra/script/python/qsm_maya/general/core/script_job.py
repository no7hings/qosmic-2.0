# coding:utf-8
import enum
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ScriptJobEventTypes(enum.EnumMeta):
    SelectionChanged = 'SelectionChanged'
    FrameChanged = 'timeChanged'
    FrameRangeChanged = 'playbackRangeChanged'


class ScriptJob(object):
    EventTypes = ScriptJobEventTypes

    def __init__(self, name):
        self._window_name = '{}_script_job_window'.format(name)

    def register(self, method, event_type):
        if not cmds.window(self._window_name, exists=1):
            cmds.window(self._window_name, title='script gob window', sizeable=1, resizeToFitChildren=1)

        if isinstance(method, list):
            for i_method in method:
                cmds.scriptJob(parent=self._window_name, event=[event_type, i_method])
        else:
            cmds.scriptJob(parent=self._window_name, event=[event_type, method])

    def destroy(self):
        if cmds.window(self._window_name, exists=1):
            cmds.deleteUI(self._window_name)
