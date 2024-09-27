# coding:utf-8
import lxgui.core as gui_core

import lxgui.qt.widgets as qt_widgets

import qsm_lazy.screw.core as qsm_lzy_src_core


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    def execute(self):
        window = self._session.find_window()
        if window is not None:
            page = window.gui_get_current_page()
            node_opt = page._gui_node_opt
            scr_stage_key = self._option_opt.get('stage_key')
            self._scr_stage = qsm_lzy_src_core.Stage(scr_stage_key)

            scr_entities = node_opt.gui_get_checked_or_selected_scr_entities()
            if scr_entities:
                self.show_many(window, scr_entities)

    def show_many(self, window, scr_entities):
        dict_ = {}
        keys = [
            'mesh_count_generate',
            'snapshot_generate',
            'unit_assembly_generate',
        ]
        with window.gui_progressing(maximum=len(scr_entities)) as g_p:
            for i_entity in scr_entities:
                i_dict = {}
                i_entity_path = i_entity.path
                i_is_rig = self._scr_stage.is_exists_node_tag(
                    i_entity_path, '/task/rig'
                )

                for j_key in keys:
                    j_value = self._scr_stage.get_node_parameter(i_entity_path, 'process_memory_usage.{}'.format(j_key))
                    if j_value is None:
                        j_value = 0
                    else:
                        j_value = int(j_value)

                    i_dict[j_key] = j_value

                dict_[i_entity_path] = i_dict

                g_p.do_update()

        if dict_:
            self.show_dialog(dict_, keys)

    def show_dialog(self, data, keys):
        chart_view = qt_widgets.QtViewForLineChart()
        chart_view._set_name_text_('Process Memory Usage')
        chart_view._set_data_(
            data,
            keys,
            data_type_dict={x: 'file_size' for x in keys}
        )
        gui_core.GuiApplication.show_tool_dialog(
            widget=chart_view,
            title=gui_core.GuiUtil.choice_name_auto(self._session.gui_configure.get('window')),
            size=(640, 480)
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
