# coding:utf-8
import six

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxbasic.content as bsc_content

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin

import qsm_general.core as qsm_gnl_core

import qsm_screw.core as qsm_scr_core


class MotionRegisterOpt(object):
    def __init__(self, scr_stage, root_path, directory_path):
        if isinstance(scr_stage, qsm_scr_core.Stage) is False:
            raise RuntimeError()

        self._src_stage = scr_stage
        self._root_path = root_path
        self._directory_path = bsc_core.auto_unicode(directory_path)

    def execute(self):
        if bsc_storage.StgPath.get_is_exists(self._directory_path) is False:
            raise RuntimeError()

        path_relative = self._directory_path[len(self._root_path):]
        _ = path_relative.split('/')
        type_path_src = '/'.join(_[:-1])
        name = _[-1][:-len('.anim')]

        node_path = '/{}'.format('_'.join(bsc_pinyin.Text.split_any_to_words(path_relative))).lower()

        json_file_path = six.u('{}/pose.json').format(self._directory_path)
        image_sequence_path = six.u('{}/sequence/thumbnail.%04d.jpg').format(self._directory_path)

        content = bsc_content.Content(value=json_file_path)
        data = bsc_storage.StgFileOpt(json_file_path).set_read()
        references = content.get('metadata.references')
        if not references:
            return
        reference_file_path = references[0]['filename']
        ctime = content.get('metadata.ctime')

        start_frame = content.get('metadata.startFrame')
        end_frame = content.get('metadata.endFrame')
        frame_count = end_frame-start_frame+1
        user = content.get('metadata.user')

        time_unit = content.get('metadata.timeUnit')
        fps = qsm_gnl_core.MayaTimeunit.timeunit_to_fps(time_unit)

        names = bsc_pinyin.Text.split_any_to_words(name)
        gui_name = ' '.join(map(lambda x: str(x).capitalize(), names))
        gui_name_chs = gui_name
        info = content.get('info')
        if info:
            _ = info.get('CNName')
            if _ is not None:
                gui_name_chs = _

        type_path = self.create_types(type_path_src)
        self._src_stage.create_node(
            node_path, gui_name=gui_name, gui_name_chs=gui_name_chs, user=user, ctime=float(ctime)
        )
        self._src_stage.create_node_type_assign(
            node_path, type_path
        )
        self._src_stage.upload_node_preview_as_image_sequence(
            node_path, image_sequence_path
        )
        self._src_stage.create_or_update_parameters(
            node_path, 'stl_animation_source', self._directory_path
        )
        self._src_stage.create_or_update_parameters(
            node_path, 'rig_maya_scene', reference_file_path
        )
        self._src_stage.create_or_update_parameters(
            node_path, 'fps', fps
        )

    def create_types(self, type_path_src):
        _ = type_path_src.split('/')
        keys = []
        for i in _:
            if _:
                keys.append('_'.join(bsc_pinyin.Text.split_any_to_words(i)).lower())
            else:
                keys.append(i)

        max_index = len(keys)-1
        for i_index, i_key in enumerate(keys):
            if i_index > 0:
                i_path = '/'.join(keys[:i_index+1])
                i_gui_name = i_key.capitalize()
                i_gui_name_chs = _[i_index]
                if i_index == max_index:
                    self._src_stage.create_type(i_path, gui_name=i_gui_name, gui_name_chs=i_gui_name_chs)
                else:
                    self._src_stage.create_type_as_group(i_path, gui_name=i_gui_name, gui_name_chs=i_gui_name_chs)

        return '/'.join(keys)


class MotionBatchRegister(object):
    def __init__(self, root_path, directory_path):
        self._scr_stage = qsm_scr_core.Stage('motion_test')

        self._root_path = bsc_core.auto_unicode(root_path)
        self._directory_path = bsc_core.auto_unicode(directory_path)

    def execute(self):
        all_directory_paths = bsc_storage.StgDirectoryOpt(self._directory_path).get_all_directory_paths()
        with bsc_log.LogProcessContext(maximum=len(all_directory_paths)) as l_p:
            for i_directory_path in all_directory_paths:
                if bsc_core.BscFnmatch.filter([i_directory_path], six.u('{}/*.anim').format(self._directory_path)):
                    MotionRegisterOpt(
                        self._scr_stage,
                        self._root_path,
                        i_directory_path
                    ).execute()

                l_p.do_update()

