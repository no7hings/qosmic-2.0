# coding:utf-8


class LoadPremiereXml(object):
    def __init__(self, node):
        self._node = node
        
    def analysis_and_build(self):
        import qsm_general.dotfile as qsm_gnl_dotfile

        file_path = self._node.get('input.file')
        if file_path:
            xml = qsm_gnl_dotfile.PremiereXml(file_path)

            self._node.set('info.fps', xml.get_fps())
            self._node.set('info.video_json', xml.get_videos())

            target_nodes = self._node.get_target_nodes()
            print(target_nodes)


class LoadMayaScene(object):
    def __init__(self, node):
        self._node = node

    def analysis_or_update(self):
        import qsm_general.dotfile as qsm_gnl_dotfile

        file_path = self._node.get('input.file')
        if file_path:
            ma = qsm_gnl_dotfile.MayaAscii(file_path)

            self._node.set('info.frame_range', ma.get_frame_range())
            self._node.set('info.fps', ma.get_fps())
            self._node.set('info.reference_json', ma.get_reference_files())

