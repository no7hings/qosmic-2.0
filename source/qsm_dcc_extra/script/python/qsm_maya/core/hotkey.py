# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Hotkey(object):
    @classmethod
    def set_current_set(cls, set_name):
        if not cmds.hotkeySet(set_name, query=True, exists=True):
            cmds.hotkeySet(set_name, current=True, source="Maya_Default")

    @classmethod
    def create(cls, key, name, annotation, cmd_script, ctrl=False, shift=False, alt=False):
        cmds.nameCommand(
            name,
            annotation=annotation,
            command='python("{}")'.format(cmd_script)
        )

        cmds.hotkey(
            name=name,
            k=key, ctrlModifier=ctrl, shiftModifier=shift, altModifier=alt
        )

