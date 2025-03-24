# coding:utf-8
import os


class LoadPremiereXml(object):
    def __init__(self, node):
        self._node = node
        
    def analysis_and_build(self):
        import lxbasic.storage as bsc_storage

        import qsm_general.dotfile as qsm_gnl_dotfile

        root = self._node.root_model
        with root.disable_undo():
            file_path = self._node.get('input.file')
            if file_path:
                directory_path = os.path.dirname(file_path)

                xml = qsm_gnl_dotfile.PremiereXml(file_path)

                videos = xml.get_videos()

                self._node.set('data.fps', xml.get_fps())
                self._node.set('data.videos', videos)

                x_spc, y_spc = 96, 96

                node_name = self._node.get_name()
                x, y = self._node.get_position()
                w, h = self._node.get_size()

                if videos:
                    _, replace_reference_node = root.add_node(
                        'ReplaceMayaReference',
                        path='/{}_replace'.format(node_name)
                    )

                    _, output_maya_scene_node = root.add_node(
                        'OutputMayaScene',
                        path='/{}_output'.format(node_name)
                    )

                    i_x, i_y = 0, 0
                    i_w, i_h = 0, 0

                    c = len(videos)
                    for idx, i_video_path in enumerate(videos):
                        i_ma = bsc_storage.StgFileOpt(i_video_path).replace_ext_to('.ma')
                        if i_ma.get_is_exists():
                            i_name = i_ma.get_name_base()
                            i_flag_0, i_node_0 = root.add_node(
                                'LoadMayaScene',
                                path='/{}_{}_S'.format(node_name, i_name)
                            )
                            if i_flag_0 is True:
                                i_w, i_h = i_node_0.get_size()
                                i_node_0.set_position((x+(idx-int(c/2))*(i_w+x_spc), y+h+y_spc))

                                i_x, i_y = i_node_0.get_position()

                                self._node.connect(i_node_0)

                                i_node_0.set('input.file', i_ma.get_path())
                                i_node_0.set_video(i_video_path)
                                i_node_0.set('setting.location', '/root/maya/scene/{}'.format(i_name))
                                i_node_0.execute('data.update_info')

                                i_node_0.connect(replace_reference_node)

                    replace_reference_node.execute('data.update_info')

                    replace_reference_node.connect(output_maya_scene_node)

                    replace_reference_node.set_position(
                        (x, i_y+i_h+y_spc)
                    )
                    x, y = replace_reference_node.get_position()
                    w, h = replace_reference_node.get_size()

                    output_maya_scene_node.set_position(
                        (x, y+h+y_spc)
                    )

                    output_maya_scene_node.set(
                        'output.directory', '{}/replace_output'.format(directory_path)
                    )


class LoadMayaScene(object):
    def __init__(self, node):
        self._node = node

    def update_info(self):
        import qsm_general.dotfile as qsm_gnl_dotfile

        file_path = self._node.get('input.file')
        if file_path:
            ma = qsm_gnl_dotfile.MayaAscii(file_path)

            self._node.set('data.frame_range', ma.get_frame_range())
            self._node.set('data.fps', ma.get_fps())
            self._node.set('data.references', ma.get_reference_files())


class ReplaceMayaReference(object):
    def __init__(self, node):
        self._node = node

    def update_info(self):
        import lxbasic.core as bsc_core

        stage = self._node.generate_stage()
        cel_str = self._node.get('setting.selection')
        stg_nodes = stage.find_nodes(cel_str)

        file_ptn = self._node.get('setting.file_pattern')
        if file_ptn:
            file_ptn_opt = bsc_core.BscStgParseOpt(file_ptn)
        else:
            file_ptn_opt = None

        reference_set = set()
        for i in stg_nodes:
            i_references = i.get_data('references')
            if i_references:
                for j in i_references:
                    if j in reference_set:
                        continue

                    if file_ptn_opt:
                        if file_ptn_opt.check_is_matched(j):
                            reference_set.add(j)
                    else:
                        reference_set.add(j)

        self._node.set('data.references', list(reference_set))

    def create_replace(self):
        import lxbasic.core as bsc_core

        import lxgui.core as gui_core

        import lnx_scan

        import qsm_lazy.api as qsm_lzy_api

        file_ptn = self._node.get('setting.file_pattern')
        if not file_ptn:
            return

        file_ptn_opt = bsc_core.BscStgParseOpt(file_ptn)

        references = self._node.get('data.references')
        reference_old = gui_core.GuiApplication.exec_input_dialog(
            type='choose',
            options=references,
            info='Choose File...',
            value=references[0],
            title='Create Replace',
            ok_label='Next'
        )
        if reference_old:
            scan_entity = qsm_lzy_api.get_asset_entity()
            if scan_entity:
                if scan_entity.type == lnx_scan.EntityTypes.Asset:
                    file_ptn_opt_new = file_ptn_opt.update_variants_to(**scan_entity.variants)
                    if not file_ptn_opt_new.get_keys():
                        reference_new = file_ptn_opt_new.get_value()
                        if reference_new != reference_old:
                            value_old = self._node.get('replace.replace_dict')
                            value_old[reference_old] = reference_new
                            self._node.set('replace.replace_dict', value_old)

    def remove_replace(self):
        print('BBB')
