# coding:utf-8
import os

import lxbasic.core as bsc_core

import tempfile


class MayaSceneDropAction:

    @classmethod
    def to_temp_mel_file(cls, mel_script):
        key = bsc_core.BscUuid.generate_by_text(mel_script)
        temp_dir = tempfile.gettempdir().replace('\\', '/')

        temp_file_path = '{}/{}.mel'.format(temp_dir, key)
        if os.path.isfile(temp_file_path) is False:
            with open(temp_file_path, 'w') as f:
                f.write(mel_script)

        return temp_file_path

    @classmethod
    def generate_load_mel(cls, scene_path, auto_namespace=False, move_to_mouse=False):
        mel_script = (
            u'python("import lnx_maya_resora.core as c; '
            u'c.SceneDropAction.load_one(\\"{}\\", auto_namespace={}, move_to_mouse={})");'
        ).format(
            scene_path, auto_namespace, move_to_mouse
        )
        return cls.to_temp_mel_file(mel_script)


class MayaVideoDropAction:

    @classmethod
    def generate_load_mel(cls, scene_path, auto_namespace=False, move_to_mouse=False):
        mel_script = (
            u'python("import lnx_maya_resora.core as c; '
            u'c.SceneDropAction.load_one(\\"{}\\", auto_namespace={}, move_to_mouse={})");'
        ).format(
            scene_path, auto_namespace, move_to_mouse
        )
        return MayaSceneDropAction.to_temp_mel_file(mel_script)
