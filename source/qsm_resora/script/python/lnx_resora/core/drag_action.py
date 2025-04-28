# coding:utf-8
import os

import lxbasic.core as bsc_core

import tempfile


class MayaSceneFileMel:

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
    def generate_import_mel(cls, scene_path, auto_namespace=False, move_to_mouse=False):
        mel_script = (
            u'python("import lnx_maya_resora.core as c; '
            u'c.FileDragAction.import_one(\\"{}\\", auto_namespace={}, move_to_mouse={})");'
        ).format(
            scene_path, auto_namespace, move_to_mouse
        )
        return cls.to_temp_mel_file(mel_script)

    @classmethod
    def generate_reference_mel(cls, scene_path, auto_namespace=False, move_to_mouse=False):
        mel_script = (
            u'python("import lnx_maya_resora.core as c; '
            u'c.FileDragAction.reference_one(\\"{}\\", auto_namespace={}, move_to_mouse={})");'
        ).format(
            scene_path, auto_namespace, move_to_mouse
        )
        return cls.to_temp_mel_file(mel_script)

    @classmethod
    def generate_open_mel(cls, scene_path):
        mel_script = u'python("import qsm_maya.core as c; c.SceneFile.open_with_dialog(\\"{}\\")");'.format(
            scene_path
        )
        return cls.to_temp_mel_file(mel_script)
