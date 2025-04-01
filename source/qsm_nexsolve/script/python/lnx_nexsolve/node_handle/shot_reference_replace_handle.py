# coding:utf-8
import os

import functools


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
                file_opt = bsc_storage.StgFileOpt(file_path)

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
                    flag_0, replace_reference_node = root.add_node(
                        'ReplaceMayaReference',
                        path='/{}_replace'.format(node_name)
                    )

                    flag_1, output_maya_scene_node = root.add_node(
                        'OutputMayaScene',
                        path='/{}_output'.format(node_name)
                    )

                    if flag_1 is True:
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
                                    i_node_0.execute('data.update_data')

                                    i_node_0.connect(replace_reference_node)

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
                            'output.directory', '{}/{}_output'.format(directory_path, file_opt.name_base)
                        )


class LoadMayaScene(object):
    def __init__(self, node):
        self._node = node

    def update_data(self):
        import lxbasic.storage as bsc_storage

        import lxgui.core as gui_core

        import qsm_general.dotfile as qsm_gnl_dotfile

        file_path = self._node.get('input.file')
        if file_path:
            if os.path.splitext(file_path)[-1] != '.ma':
                gui_core.GuiApplication.exec_message_dialog(
                    '只支持“.ma”。',
                    title='更新数据',
                    size=(320, 120),
                    status='warning',
                )
                return

            ignore_unloaded = self._node.get('setting.ignore_unloaded')

            ma = qsm_gnl_dotfile.MayaAscii(file_path)

            self._node.set('data.frame_range', ma.get_frame_range())
            self._node.set('data.fps', ma.get_fps())
            self._node.set('data.cameras', ma.get_cameras())
            self._node.set('data.references', ma.get_reference_files(ignore_unloaded=ignore_unloaded))

            self._node.set(
                'setting.location', '/root/maya/scene/{}'.format(bsc_storage.StgFileOpt(file_path).name_base)
            )


class ReplaceMayaReference(object):
    def __init__(self, node):
        self._node = node

    def get_match_references(self):
        import lxbasic.core as bsc_core

        stage = self._node.compute_chain_to_stage()
        cel_str = self._node.get('setting.selection')
        stg_nodes = stage.find_nodes(cel_str)

        file_ptn = self._node.get('setting.reference_pattern')
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
        return list(reference_set)

    def get_file_pattern_opt(self):
        import lxbasic.core as bsc_core

        file_ptn = self._node.get('setting.reference_pattern')
        if not file_ptn:
            return

        return bsc_core.BscStgParseOpt(file_ptn)

    def create_replace(self):
        import lxgui.core as gui_core

        file_ptn_opt = self.get_file_pattern_opt()
        if not file_ptn_opt:
            return

        references_all = self.get_match_references()
        if not references_all:
            gui_core.GuiApplication.exec_message_dialog(
                '没有引用。',
                title='创建替换',
                size=(320, 120),
                status='warning',
            )
            return

        value_old = self._node.get('replace.replace_map')
        references = [x for x in references_all if x not in value_old]
        if not references:
            gui_core.GuiApplication.exec_message_dialog(
                '所有引用（替换）已经被创建。',
                title='创建替换',
                size=(320, 120),
                status='warning',
            )
            return

        self.create_or_update(references, value_old, file_ptn_opt)

    def create_or_update(self, references, value_old, file_ptn_opt):
        import lxgui.core as gui_core

        import lnx_scan

        import lnx_dcc_tool_prc.api as qsm_lzy_api

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
                            value_old[reference_old] = reference_new
                            self._node.set('replace.replace_map', value_old)

    def modify_replace(self):
        import lxgui.core as gui_core

        file_ptn_opt = self.get_file_pattern_opt()
        if not file_ptn_opt:
            return

        value_old = dict(self._node.get('replace.replace_map'))
        if not value_old:
            gui_core.GuiApplication.exec_message_dialog(
                '没有引用（替换）可以被修改。',
                title='修改替换',
                size=(320, 120),
                status='warning',
            )
            return

        references = list(value_old.keys())

        self.create_or_update(references, value_old, file_ptn_opt)

    def remove_replace(self):
        import lxgui.core as gui_core

        value_old = dict(self._node.get('replace.replace_map'))
        if not value_old:
            gui_core.GuiApplication.exec_message_dialog(
                '没有引用（替换）可以被移除。',
                title='移除替换',
                size=(320, 120),
                status='warning',
            )
            return

        references = list(value_old.keys())
        reference = gui_core.GuiApplication.exec_input_dialog(
            type='choose',
            options=references,
            info='Choose File...',
            value=references[0],
            title='Remove Replace',
        )

        if reference:
            value_old.pop(reference)
            self._node.set('replace.replace_map', value_old)


class OutputMayaScene(object):
    API_VERSION = '1.0.0'

    TASK_KEY = 'shot_replace_reference'

    def __init__(self, node):
        self._node = node

    @staticmethod
    def valid_fnc(file_path, references, reference_map):
        if not references:
            return

        list_ = []
        for i in references:
            if i not in reference_map:
                list_.append(i)

        if list_:
            return u'{}\n[\n    {}\n]'.format(
                file_path, u', '.join(list_)
            )

    def generate_prc_args(self, file_path, reference_replace_map):
        import lxbasic.core as bsc_core

        import lxbasic.storage as bsc_storage

        import qsm_general.core as qsm_gnl_core

        import qsm_general.process as qsm_gnl_process

        file_path = bsc_core.ensure_string(file_path)

        cache_path = qsm_gnl_core.DccCache.generate_shot_replace_reference_file(
            file_path, reference_replace_map, self.API_VERSION
        )

        task_name = '[{}][{}]'.format(
            self.TASK_KEY, bsc_storage.StgFileOpt(file_path).name
        )

        if os.path.isfile(cache_path) is False:
            cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script_by_option_dict(
                self.TASK_KEY,
                dict(
                    file_path=file_path,
                    reference_replace_map=reference_replace_map,
                    cache_path=cache_path
                )
            )
            return task_name, cmd_script, cache_path
        return task_name, None, cache_path

    @classmethod
    def _push_result(cls, cache_file_path, output_directory_path, with_playblast):
        import lxbasic.storage as bsc_storage

        cache_file_opt = bsc_storage.StgFileOpt(cache_file_path)

        cache_video_path = '{}.mov'.format(cache_file_opt.path_base)

        output_file_path = '{}/{}'.format(output_directory_path, cache_file_opt.name)

        cache_file_opt.copy_to_file(output_file_path, replace=True)

        if with_playblast is True:
            output_video_path = '{}/{}.mov'.format(output_directory_path, cache_file_opt.name_base)
            bsc_storage.StgFileOpt(cache_video_path).copy_to_file(output_video_path, replace=True)

    def _start_delay(self, task_window, execute_args, output_directory_path, with_playblast):
        process_args = []

        for i_args in execute_args:
            i_task_name, i_cmd_script, i_cache_path = self.generate_prc_args(*i_args)
            if i_cmd_script is not None:
                process_args.append(
                    (i_task_name, i_cmd_script, i_cache_path)
                )
            else:
                self._push_result(i_cache_path, output_directory_path, with_playblast)

        if process_args:
            task_window.show_window_auto(exclusive=False)
            for i_args in process_args:
                i_task_name, i_cmd_script, i_cache_path = i_args
                task_window.submit(
                    self.TASK_KEY,
                    name=i_task_name,
                    cmd_script=i_cmd_script,
                    completed_fnc=functools.partial(
                        self._push_result, i_cache_path, output_directory_path, with_playblast
                    ),
                    application='maya'
                )
        else:
            task_window.close_window()

    def open_output_directory(self):
        import lxbasic.storage as bsc_storage

        output_directory_path = self._node.get('output.directory')
        if not output_directory_path:
            return

        bsc_storage.StgFileOpt(output_directory_path).show_in_system()

    def output_all(self):
        import lxgui.core as gui_core

        import lxgui.proxy.widgets as gui_prx_widgets

        stage = self._node.compute_chain_to_stage()

        output_directory_path = self._node.get('output.directory')
        if not output_directory_path:
            return

        with_playblast = self._node.get('output.with_playblast')

        cel_str = self._node.get('setting.selection')
        stg_nodes = stage.find_nodes(cel_str)

        results = []

        execute_args = []

        for i in stg_nodes:
            i_file_path = i.get_data('file')

            i_references = i.get_data('references') or []
            i_reference_replace_map = i.get_data('reference_replace_map') or {}

            i_result = self.valid_fnc(i_file_path, i_references, i_reference_replace_map)
            if i_result:
                results.append(i_result)

            execute_args.append((i_file_path, i_reference_replace_map))

        if results:
            result = gui_core.GuiApplication.exec_message_dialog(
                u'以下文件有没被替换的引用，是否要忽略？\n{}'.format(u'\n'.join(results)),
                title='输出所有',
                size=(480, 320),
                status='warning',
                show_cancel=True,
            )
            if result is not True:
                return

        if execute_args:
            task_window = gui_prx_widgets.PrxSpcTaskWindow()
            task_window.set_thread_maximum(2)

            if task_window._language == 'chs':
                task_window.set_window_title('镜头引用替换')
                task_window.set_tip(
                    '正在生成镜头，请耐心等待；\n'
                    '如需要终止任务，请点击“关闭”。'
                )
            else:
                task_window.set_window_title('Shot Reference Replace')

            task_window.run_fnc_delay(
                functools.partial(
                    self._start_delay,
                    task_window, execute_args, output_directory_path, with_playblast
                ),
                500
            )

