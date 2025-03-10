# coding:utf-8
import lxbasic.storage as bsc_storage

import lnx_screw.core as lnx_scr_core

import qsm_maya.core as qsm_mya_core


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    def execute(self):
        window = self._session.find_window()
        if window is not None:
            page = window.gui_get_current_page()
            node_opt = page._gui_node_opt
            scr_stage_name = self._option_opt.get('stage_name')

            scr_entities = node_opt.gui_get_checked_or_selected_scr_entities()
            if scr_entities:
                scr_stage = lnx_scr_core.Stage(scr_stage_name)
                with window.gui_progressing(maximum=len(scr_entities)) as g_p:
                    for i_scr_entity in scr_entities:
                        i_scene_path = scr_stage.get_node_parameter(i_scr_entity.path, 'scene')
                        if i_scene_path is None:
                            continue
                        if bsc_storage.StgPath.get_is_file(i_scene_path) is False:
                            continue

                        file_opt = bsc_storage.StgFileOpt(i_scene_path)

                        qsm_mya_core.SceneFile.reference_file(
                            i_scene_path,
                            namespace=file_opt.name_base
                        )

                        g_p.do_update()

                scr_stage.close()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
