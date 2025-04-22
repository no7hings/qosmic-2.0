# coding:utf-8
import collections

import copy

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core

import qsm_general.dotfile as qsm_gnl_dotfile

from lnx_wotrix.gui.abstracts import subpage_for_task_create as _sub_page_for_task_create

import qsm_maya.core as qsm_mya_core

from lnx_maya_wotrix.core import task_parse as _task_parse

from ..gui_operates import task_create as _task_create_opt


# cfx cloth
class GuiTaskCreateMain(_sub_page_for_task_create.AbsPrxSubpageForTaskCreate):
    TASK_CREATE_OPT_CLS = _task_create_opt.MayaShotCfxClothCreateOpt

    GUI_KEY = '{}/{}'.format(TASK_CREATE_OPT_CLS.RESOURCE_TYPE, TASK_CREATE_OPT_CLS.TASK)

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(GuiTaskCreateMain, self).__init__(window, session, subwindow, *args, **kwargs)

        self._special_load_flag = False

        self._prx_options_node.set(
            'upstream.play_preview', self.on_play_preview
        )

        self._prx_options_node.set(
            'upstream.analysis_scene', self.on_analysis_scene
        )

    def on_play_preview(self):
        preview_path = self._prx_options_node.get('upstream.preview')
        if preview_path:
            if bsc_storage.StgPath.get_is_file(preview_path):
                bsc_storage.StgFileOpt(preview_path).start_in_system()

    def on_analysis_scene(self):
        scene_path = self._prx_options_node.get('upstream.scene')
        if scene_path:
            self._special_load_flag = True

            ma = qsm_gnl_dotfile.MayaAscii(scene_path)
            references = ma.get_references()
            frame_range = ma.get_frame_range()
            fps = ma.get_fps()

            reference_port = self._prx_options_node.get_port('upstream.scene_references')
            reference_port.set(references)
            reference_port.set_all_items_checked(False)

            loaded_dict = collections.OrderedDict([(x.path, x.get('is_loaded')) for x in references])
            if loaded_dict:
                reference_port.update_check_by_dict(loaded_dict)

            self._prx_options_node.set(
                'upstream.scene_frame_range', frame_range
            )
            self._prx_options_node.set(
                'upstream.fps', fps
            )

    def do_gui_refresh_all(self):
        resource_properties = self._subwindow._resource_properties
        if not resource_properties:
            return

        kwargs_new = copy.copy(resource_properties)
        kwargs_new['step'] = 'ani'
        kwargs_new['task'] = 'animation'
        task_parse = _task_parse.TaskParse()

        # scene
        animation_scene_ptn_opt = task_parse.generate_pattern_opt_for(
            'shot-disorder-animation-scene-file', **kwargs_new
        )
        matches = animation_scene_ptn_opt.find_matches()
        if matches:
            rig_scene_path = matches[-1]['result']
            self._prx_options_node.set('upstream.scene', rig_scene_path)
            modify_time = bsc_storage.StgFileOpt(rig_scene_path).get_modify_time()
            self._prx_options_node.set('upstream.scene_modify_time', modify_time)

        # preview
        animation_preview_pth_opt = task_parse.generate_pattern_opt_for(
            'shot-disorder-animation-preview-file', **kwargs_new
        )
        matches = animation_preview_pth_opt.find_matches()
        if matches:
            preview_path = matches[-1]['result']
            self._prx_options_node.set('upstream.preview', preview_path)

        # noinspection PyBroadException
        try:
            self.on_analysis_scene()
        except Exception:
            pass

    def _on_apply(self):
        prx_widget = self._subwindow._prx_widget
        resource_properties = self._subwindow._resource_properties
        if not resource_properties:
            return

        if qsm_mya_core.SceneFile.new_with_dialog() is True:
            task_parse = _task_parse.TaskParse()

            task_unit = self._prx_options_node.get('task_unit')
            if not task_unit:
                return

            upstream_scene_path = self._prx_options_node.get('upstream.scene')
            if upstream_scene_path is None:
                return

            if self._special_load_flag:
                reference_nodes = []
                reference_paths = self._prx_options_node.get('upstream.scene_references')
                for i in reference_paths:
                    if i.get('type') == 'reference':
                        reference_nodes.append(i.get('node'))

                scene_frame_range = self._prx_options_node.get('upstream.scene_frame_range')
            else:
                reference_nodes = None
                scene_frame_range = None

            auto_load_cfx_rig = self._prx_options_node.get('auto_load_cfx_rig')
            solver_start_frame = self._prx_options_node.get('solver_start_frame')
            ignore_load_scenery = self._prx_options_node.get('ignore_load_scenery')
            auto_hide_no_use_group = self._prx_options_node.get('auto_hide_no_use_group')
            auto_hide_vfx_group = self._prx_options_node.get('auto_hide_vfx_group')

            (
                task_create_opt, kwargs_new, scene_src_path, thumbnail_path
            ) = self.TASK_CREATE_OPT_CLS.generate_scene_src_args(
                resource_properties, task_parse, task_unit, 'maya'
            )

            if bsc_storage.StgPath.get_is_file(scene_src_path) is False:
                task_create_opt.build_scene_src_fnc(
                    scene_src_path=scene_src_path,
                    upstream_scene_path=upstream_scene_path,
                    auto_load_cfx_rig=auto_load_cfx_rig,
                    solver_start_frame=solver_start_frame,
                    defer_load_reference_nodes=reference_nodes,
                    scene_frame_range=scene_frame_range,
                    ignore_load_scenery=ignore_load_scenery,
                    auto_hide_no_use_group=auto_hide_no_use_group,
                    auto_hide_vfx_group=auto_hide_vfx_group,
                )

                qsm_mya_core.SceneFile.refresh()

                with self._subwindow._window.gui_minimized():
                    gui_qt_core.QtMaya.make_snapshot(thumbnail_path)

                prx_widget.gui_load_task_unit_scene(kwargs_new)
