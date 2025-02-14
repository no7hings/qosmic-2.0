# coding:utf-8

# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel


class AnmLayerOpt(object):
    def __init__(self, path):
        self._path = path

    def is_active(self):
        return not cmds.animLayer(self._path, query=1, mute=1)

    def get_weight(self):
        return cmds.animLayer(self._path, query=1, weight=1)

    def set_current(self):
        mel.eval('selectLayer("{}");'.format(self._path))

    @classmethod
    def switch_to_current_base(cls):
        mel.eval('selectLayer("BaseAnimation");')


class AnmLayers(object):
    @classmethod
    def get_root(cls):
        return cmds.animLayer(query=1, root=1)

    @classmethod
    def get_all(cls):
        return cmds.ls(type='animLayer', long=1) or []

    @classmethod
    def merge_all(cls):
        """
        C:/Program Files/Autodesk/Maya2020/scripts/others/performAnimLayerMerge.mel
        """
        cmds.select(cls.get_all())
        mel_script = (
            'source performAnimLayerMerge; '
            'global string $gSelectedAnimLayers[]; '
            '$gSelectedAnimLayers = {{{}}}; '
            'performAnimLayerMerge(0)'
        ).format(
            ', '.join(['"{}"'.format(x) for x in cls.get_all()])
        )
        mel.eval(mel_script)

