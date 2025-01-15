# coding:utf-8
import lxgui.core as gui_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

import qsm_maya_lazy_mtg.core as qsm_mya_lzy_mtg_core

import qsm_maya_lazy_mtg.scripts as qsm_mya_lzy_mtg_scripts

from qsm_lazy_mtg.gui.abstracts import page_for_splicing as _page_for_splicing


class PrxPageForSplicing(_page_for_splicing.AbsPrxPageForSplicing):
    SCRIPT_JOB_NAME = 'lazy_montage_for_splicing'

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
        # super(PrxPageForSplicing, self)._do_dcc_playback_swap()

        if qsm_mya_core.Play.is_active() is False:
            qsm_mya_core.Play.start()
        else:
            qsm_mya_core.Play.stop()
            self._motion_prx_track_widget.set_current_frame(
                int(qsm_mya_core.Frame.get_current())
            )

    def _do_gui_update_frame(self):
        pass

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForSplicing, self).__init__(window, session, *args, **kwargs)

    def _dcc_get_rig_namespaces(self):
        return qsm_mya_lzy_mtg_core.MtgStage.find_all_valid_rig_namespaces()

    def _dcc_set_current_rig_namespace(self, rig_namespace):
        qsm_mya_lzy_mtg_core.MtgRoot.set_current_rig_namespace(rig_namespace)

    def _dcc_get_current_rig_namespace(self):
        return qsm_mya_lzy_mtg_core.MtgRoot.get_current_rig_namespace()

    def gui_refresh_fnc(self, force=False):
        rig_namespaces = self._dcc_get_rig_namespaces()
        if rig_namespaces:
            if self._rig_namespace is None:
                dcc_rig_namespace = self._dcc_get_current_rig_namespace()
                if dcc_rig_namespace in rig_namespaces:
                    self._rig_namespace = dcc_rig_namespace
                else:
                    self._rig_namespace = rig_namespaces[0]

                self._rig_namespace_qt_info_bubble._set_text_(
                    self._rig_namespace
                )
        else:
            self.gui_restore()
            return

        if self._rig_namespace is not None:
            if force is True:
                self._motion_prx_track_widget.restore()

            mtg_stage = qsm_mya_lzy_mtg_core.MtgStage(self._rig_namespace)
            data = mtg_stage.generate_track_data()
            if data:
                for i_kwargs in data:
                    self._motion_prx_track_widget.create_node(**i_kwargs)
        else:
            self.gui_restore()

    def _do_check_update(self):
        rig_namespaces = self._dcc_get_rig_namespaces()
        if rig_namespaces:
            if self._rig_namespace is not None:
                dcc_keys = qsm_mya_lzy_mtg_core.MtgStage(self._rig_namespace).get_all_track_keys()
                gui_keys = self._motion_prx_track_widget.get_all_track_keys()
                if set(dcc_keys) != set(gui_keys):
                    self.gui_refresh_fnc(force=True)
            else:
                self.gui_refresh_fnc(force=True)
        else:
            self.gui_restore()

    def _on_dcc_export_track(self):
        if self._rig_namespace is not None:
            track_json_path = gui_core.GuiStorageDialog.save_file(
                ext_filter='All File (*.jsz)', parent=self._qt_widget
            )
            if track_json_path:
                mtg_stage = qsm_mya_lzy_mtg_core.MtgStage(self._rig_namespace)
                mtg_stage.export_track_data(track_json_path)
        else:
            self._window.exec_message_dialog(
                'No motion to export.',
                status='warning'
            )

    def _on_dcc_import_track(self):
        if self._rig_namespace is not None:
            track_json_path = gui_core.GuiStorageDialog.open_file(
                ext_filter='All File (*.jsz)', parent=self._qt_widget
            )
            if track_json_path:
                qsm_mya_lzy_mtg_core.MtgStage(self._rig_namespace).import_track_json(track_json_path)
        else:
            self._window.exec_message_dialog(
                'No motion to import.',
                status='warning'
            )

    def _on_dcc_delete(self):
        if self._rig_namespace is not None:
            result = self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.messages.delete_confirm')
                ),
                status='warning'
            )
            if result:
                mtg_stage = qsm_mya_lzy_mtg_core.MtgStage(self._rig_namespace)
                mtg_stage.do_delete()

                self._rig_namespace = None

                self.gui_refresh_fnc(force=True)

    def _on_dcc_bake(self):
        if self._rig_namespace is not None:
            result = self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.messages.bake_confirm')
                ),
                status='warning'
            )
            if result:
                mtg_stage = qsm_mya_lzy_mtg_core.MtgStage(self._rig_namespace)
                mtg_stage.do_bake()

                self._rig_namespace = None

                self.gui_refresh_fnc(force=True)

    def _on_dcc_look_from_persp_cam(self):
        if self._rig_namespace is not None:
            mtg_stage = qsm_mya_lzy_mtg_core.MtgStage(self._rig_namespace)
            mtg_stage.look_from_persp_cam()

    def on_dcc_stage_update(self):
        if self._rig_namespace is not None:
            stage = self._motion_prx_track_widget.get_stage_model()
            current_frame = self._motion_prx_track_widget.get_current()
            qsm_mya_lzy_mtg_core.MtgStage.update_by_stage(self._rig_namespace, stage, current_frame)

    def do_dcc_update_current_frame(self, frame):
        qsm_mya_core.Frame.set_current(frame)
