# coding:utf-8

class ScpMayaNetImport(object):
    def __init__(self, data):
        self._data = data or {}
        self._resource_type_path = self._data.get('resource_type')
        self._resource_path = self._data.get('resource')
        self._file_type_path = self._data.get('file_type')
        self._file_path = self._data.get('file')

    def execute(self):
        if self._data:
            if self._file_type_path in {'/scene/maya', '/scene/maya/source'}:
                self.do_import_scene_maya()

    def do_import_scene_maya(self):
        import lxmaya.dcc.objects as mya_dcc_objects

        mya_dcc_objects.Scene.set_file_open_with_dialog(
            self._file_path
        )

