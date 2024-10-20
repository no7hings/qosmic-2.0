# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_screw.core as qsm_scr_core

import qsm_maya_lazy.montage.scripts as qsm_mya_mtg_scripts


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    def execute(self):
        window = self._session.find_window()
        if window is not None:
            if not qsm_mya_mtg_scripts.AdvChrMotionImportOpt.find_master_layer_path():
                window.exec_message_dialog(
                    'Master layer is not found, you can create use "Lazy Montage".',
                    status='warning'
                )
                return

            page = window.gui_get_current_page()
            node_opt = page._gui_node_opt
            scr_stage_key = self._option_opt.get('stage_key')

            scr_entities = node_opt.gui_get_checked_or_selected_scr_entities()
            if scr_entities:
                scr_stage = qsm_scr_core.Stage(scr_stage_key)
                with window.gui_progressing(maximum=len(scr_entities)) as g_p:
                    for i_scr_entity in scr_entities:
                        i_motion_path = scr_stage.get_node_parameter(i_scr_entity.path, 'motion')
                        if i_motion_path is None:
                            continue
                        if bsc_storage.StgPath.get_is_file(i_motion_path) is False:
                            continue

                        qsm_mya_mtg_scripts.AdvChrMotionImportOpt.append_layer(i_motion_path)

                        g_p.do_update()

                scr_stage.close()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
