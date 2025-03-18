# coding:utf-8


class LoadPremiereXml(object):
    def __init__(self, node):
        self._node = node
        
    def analysis_and_build(self):
        import lxbasic.storage as bsc_storage

        import qsm_general.dotfile as qsm_gnl_dotfile

        root = self._node.root_model
        with root.undo_group():
            pass

        file_path = self._node.get('input.file')
        if file_path:
            xml = qsm_gnl_dotfile.PremiereXml(file_path)
            
            videos = xml.get_videos()

            self._node.set('info.fps', xml.get_fps())
            self._node.set('info.video_json', videos)

            x_spc, y_spc = 96, 96

            node_name = self._node.get_name()
            x, y = self._node.get_position()
            w, h = self._node.get_size()

            if videos:
                flag_0, replace_reference_node = root.add_node(
                    'ReplaceMayaReference',
                    name='{}_replace'.format(node_name)
                )

                flag_1, output_maya_scene_node = root.add_node(
                    'OutputMayaScene',
                    name='{}_output'.format(node_name)
                )

                i_x, i_y = 0, 0
                i_w, i_h = 0, 0
                for idx, i_video_path in enumerate(videos):
                    i_ma = bsc_storage.StgFileOpt(i_video_path).replace_ext_to('.ma')
                    if i_ma.get_is_exists():
                        i_name = i_ma.get_name_base()
                        i_flag_0, i_node_0 = root.add_node(
                            'LoadMayaScene',
                            name='{}_{}'.format(node_name, i_name)
                        )
                        if i_flag_0 is True:
                            i_w, i_h = i_node_0.get_size()
                            i_node_0.set_position((x+idx*(i_w+x_spc), y+h+y_spc))

                            i_x, i_y = i_node_0.get_position()

                            self._node.connect(i_node_0)

                            i_node_0.set('input.file', i_ma.get_path())
                            i_node_0.set_video(i_video_path)
                            i_node_0.execute('info.update_info')

                            i_node_0.connect(replace_reference_node)

                if flag_1 is True:
                    replace_reference_node.connect(output_maya_scene_node)

                    replace_reference_node.set_position(
                        (x, i_y+i_h+y_spc)
                    )
                    x, y = replace_reference_node.get_position()
                    w, h = replace_reference_node.get_size()

                    output_maya_scene_node.set_position(
                        (x, y+h+y_spc)
                    )


class LoadMayaScene(object):
    def __init__(self, node):
        self._node = node

    def update_info(self):
        import qsm_general.dotfile as qsm_gnl_dotfile

        file_path = self._node.get('input.file')
        if file_path:
            ma = qsm_gnl_dotfile.MayaAscii(file_path)

            self._node.set('info.frame_range', ma.get_frame_range())
            self._node.set('info.fps', ma.get_fps())
            self._node.set('info.reference_json', ma.get_reference_files())


class ReplaceMayaReference(object):
    def __init__(self, node):
        self._node = node

    def update_info(self):
        source_nodes = self._node.get_source_nodes()
        print(source_nodes)
