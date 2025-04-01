# coding:utf-8
import json

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import lnx_screw.core as lnx_scr_core

import lxgui.core as gui_core


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    @gui_core.Verify.execute('resora-admin', 7)
    def execute(self):
        window = self._session.find_window()
        if window is not None:

            scr_stage_name = self._option_opt.get('stage_name')

            page = window.gui_get_current_page()
            node_opt = page._gui_node_opt
            scr_entities = node_opt.gui_get_checked_or_selected_scr_entities()
            if not scr_entities:
                return

            search_args = []
            scr_stage = lnx_scr_core.Stage(scr_stage_name)
            for i_scr_entity in scr_entities:
                i_scr_entity_path = i_scr_entity.path
                i_source_path = scr_stage.get_node_parameter(i_scr_entity_path, 'source')
                if bsc_storage.StgPath.get_is_file(i_source_path):
                    continue

                search_args.append((i_scr_entity_path, i_source_path))

            if search_args:
                directory_path = gui_core.GuiStorageDialog.open_directory(
                    parent=window.widget
                )
                if directory_path:
                    # get all below
                    directory_paths = bsc_storage.StgDirectoryOpt(directory_path).get_all_directory_paths()
                    search_opt = bsc_storage.StgFileSearchOpt(
                        ignore_name_case=True, ignore_ext_case=True
                    )
                    search_opt.set_search_directories(directory_paths)

                    founds = []
                    not_founds = []
                    c = len(search_args)
                    with bsc_log.LogProcessContext.create(maximum=c, label='find lost file (source)') as l_p:
                        for i_args in search_args:
                            i_scr_entity_path, i_source_path = i_args
                            i_result = search_opt.get_result(i_source_path)
                            if i_result:
                                founds.append(i_source_path)
                                scr_stage.create_or_update_node_parameter(
                                    i_scr_entity_path, 'source', i_result
                                )
                            else:
                                not_founds.append(i_source_path)
                            l_p.do_update()

                    if not_founds:
                        window.exec_message_dialog(
                            u'{} file (source) is not found:\n{}'.format(
                                len(not_founds),
                                json.dumps(not_founds, indent=4)
                            ),
                            status='warning'
                        )
            else:
                window.exec_message_dialog(
                    u'No any file (source) is lost.',
                    status='warning'
                )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
