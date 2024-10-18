# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.model as bsc_model

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

from qsm_lazy_tool.montage.gui import abstracts as _gui_abstracts

import qsm_maya.core as qsm_mya_core

import qsm_maya.steps.animation.core as qsm_mya_stp_anm_core

import qsm_maya_lazy.montage.core as qsm_mya_lzy_mtg_core

import qsm_maya_lazy.montage.scripts as qsm_mya_lzy_mtg_scripts

from ....generate.gui import widgets as _gnl_gui_weights


class PrxPageForSplicing(_gui_abstracts.AbsPrxPageForSplicing):
    SCRIPT_JOB_NAME = 'lazy_montage_for_splicing'

    UNIT_CLASS_DICT = dict(
        scene_space=_gnl_gui_weights.PrxUnitForSceneSpace
    )

    def _do_dcc_register_all_script_jobs(self):
        self._script_job_opt = qsm_mya_core.ScriptJobOpt(
            self.SCRIPT_JOB_NAME
        )

        self._script_job_opt.register_as_attribute_change_(
            self._do_gui_update_current_frame, 'time1.outTime'
        )

    def _do_dcc_destroy_all_script_jobs(self):
        self._script_job_opt.destroy()

    def _do_dcc_playback_swap(self):
        if qsm_mya_core.Play.is_active() is False:
            qsm_mya_core.Play.start()
        else:
            qsm_mya_core.Play.stop()
            self._motion_prx_track_widget.set_current_frame(
                int(qsm_mya_core.Frame.get_current_time())
            )

    def _do_gui_update_frame(self):
        pass

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForSplicing, self).__init__(window, session, *args, **kwargs)

    def gui_refresh_stage(self, force=False):
        if force is True:
            self._motion_prx_track_widget.restore()

        data = qsm_mya_lzy_mtg_core.AdvMotionStage().generate_track_data()
        if data:
            for i_kwargs in data:
                self._motion_prx_track_widget.create_node(**i_kwargs)

    def _do_check_update(self):
        dcc_all_layers = qsm_mya_lzy_mtg_core.AdvMotionStage().get_all_layer_names()
        gui_all_layers = self._motion_prx_track_widget.get_all_layer_names()
        if set(dcc_all_layers) != set(gui_all_layers):
            self.do_gui_refresh_all(force=True)

    def get_dcc_character_args(self):
        results = []

        master_layer = qsm_mya_lzy_mtg_scripts.AdvChrMotionImportOpt.find_master_layer_path()
        if master_layer:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.exists_master_layer'.format(self.PAGE_KEY))
                ),
                status='warning'
            )
            return

        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            results = qsm_mya_stp_anm_core.AdvRigAsset.filter_namespaces(namespaces)

        if not results:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_character'.format(self.PAGE_KEY))
                ),
                status='warning'
            )
            return
        return results

    def _open_scene_fnc(self, scene_path):
        result = qsm_mya_core.SceneFile.open_with_dialog(scene_path)
        if result is True:
            self.do_gui_refresh_all(True)
        return result

    def _save_scene_fnc(self, scene_path, thumbnail_path):
        gui_qt_core.QtMaya.make_snapshot(thumbnail_path)
        return qsm_mya_core.SceneFile.save_with_dialog(scene_path)

    def _new_fnc(self, asset_path):
        file_opt = bsc_storage.StgFileOpt(asset_path)
        namespace = file_opt.name_base
        qsm_mya_core.SceneFile.reference_file(
            self._asset_path,
            namespace=namespace
        )
        qsm_mya_lzy_mtg_scripts.AdvChrMotionImportOpt.setup_for(namespace)

    def _on_dcc_load_asset(self):
        if self._asset_path is None:
            return

        result = qsm_mya_core.SceneFile.new_with_dialog()
        if result is True:
            self._new_fnc(self._asset_path)

    def _on_dcc_export_asset(self):
        master_layer = qsm_mya_lzy_mtg_core.AdvChrMotionLayer.find_master_layer_path()
        if master_layer:
            file_path = gui_core.GuiStorageDialog.save_file(ext_filter='All File (*.jsz)', parent=self._qt_widget)
            master_layer_opt = qsm_mya_lzy_mtg_core.AdvChrMotionMasterLayerOpt(master_layer)
            master_layer_opt.export_motion_to(file_path)
        else:
            self._window.exec_message_dialog(
                'No motion to export.',
                status='warning'
            )

    def do_dcc_motion_update(self):
        stage = self._motion_prx_track_widget.get_stage_model()
        start_frame, end_frame = stage.track_start, stage.track_end
        current_frame = self._motion_prx_track_widget.get_current_time()

        qsm_mya_core.Frame.update_frame(start_frame, end_frame, current_frame)

        tvl = stage.generate_valid_frame_range_travel()

        while tvl.is_valid():
            frame_range, track_model = tvl.current_data()

            is_start, is_end = tvl.is_start(), tvl.is_end()

            if track_model is not None:
                frame_range_index = track_model.get_frame_range_index(frame_range)
                key = track_model.key
                location = '|{}:LAYER'.format(key)
                layer_opt = qsm_mya_lzy_mtg_core.AdvChrMotionLayer(location)

                for i_key in bsc_model.TrackModel.MAIN_KEYS:
                    layer_opt.set(i_key, track_model.get(i_key))

                layer_opt.set('valid_start', track_model.get_valid_start())
                layer_opt.set('valid_end', track_model.get_valid_end())
                layer_opt.set('output_end', frame_range[-1])

                if frame_range_index == 0:
                    # restore curves
                    layer_opt.restore_main_weight_curve()
                    layer_opt.restore_root_start_input_transformation_curves()

                if tvl.next_is_valid() is False:
                    data_next = tvl.next_data()
                    if data_next is not None:
                        frame_range_next, track_model_next = data_next
                        frame_range = (frame_range[0], frame_range_next[-1])

                layer_opt.update_main_weight(frame_range, is_start, is_end)

                model_last = tvl.last_model()
                if model_last:
                    key_last = model_last.key
                    location_last = '|{}:LAYER'.format(key_last)
                    layer_opt_last = qsm_mya_lzy_mtg_core.AdvChrMotionLayer(location_last)
                    layer_opt.update_root_start_opt(layer_opt, layer_opt_last, frame_range[0])
                else:
                    if is_start:
                        # update root start
                        layer_opt.update_root_start_for_self(layer_opt, frame_range[0])
                    else:
                        model_last_last = tvl.last_last_model()
                        if model_last_last:
                            key_last = model_last_last.key
                            location_last = '|{}:LAYER'.format(key_last)
                            layer_opt_last = qsm_mya_lzy_mtg_core.AdvChrMotionLayer(location_last)
                            layer_opt.update_root_start_opt(layer_opt, layer_opt_last, frame_range[0])

            tvl.next()
        # update bypass
        for i in stage.get_all_nodes():
            i_tack_model = i._track_model
            i_key = i_tack_model.key
            i_location = '|{}:LAYER'.format(i_key)
            i_layer_opt = qsm_mya_lzy_mtg_core.AdvChrMotionLayer(i_location)
            i_layer_opt.set('is_bypass', i_tack_model.is_bypass)
        # flush undo
        qsm_mya_core.Undo.flush()

    def do_dcc_update_current_frame(self, frame):
        qsm_mya_core.Frame.set_current(frame)
