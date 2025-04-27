# coding:utf-8


class MayaSceneFileMel:

    @classmethod
    def generate_import_mel(cls, scene_path):
        mel_script = u'python("import qsm_maya.core as c; c.SceneFile.import_file(\\"{}\\")")'.format(scene_path)
        print(mel_script)

    @classmethod
    def generate_reference_mel(cls, scene_path):
        mel_script = u'python("import qsm_maya.core as c; c.SceneFile.reference_file(\\"{}\\", auto_namespace=True)")'.format(scene_path)
        print(mel_script)

    @classmethod
    def generate_open_mel(cls, scene_path):
        pass
