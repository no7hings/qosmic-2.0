# coding:utf-8
import lxgui.core as gui_core

import lxgui.qt.chart_widgets as qt_cht_widgets

import lnx_screw.core as lzy_src_core


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
            self._scr_stage = lzy_src_core.Stage(scr_stage_name)

            scr_entities = node_opt.gui_get_checked_or_selected_scr_entities()
            if scr_entities:
                self.show_many(window, scr_entities)

    def show_many(self, window, scr_entities):
        dict_ = {}
        with window.gui_progressing(maximum=len(scr_entities)) as g_p:
            for i_entity in scr_entities:
                i_entity_path = i_entity.path
                i_is_rig = self._scr_stage.is_exists_node_tag(
                    i_entity_path, '/task/rig'
                )

                i_memory_size = self._scr_stage.get_node_parameter(i_entity_path, 'system_memory_usage')
                if i_memory_size is not None:
                    i_dict = dict(
                        memory=int(i_memory_size)
                    )

                    if i_is_rig:
                        i_dict['VALUE_LIMIT'] = dict(
                            # 1Gb
                            memory=1*1024**3,
                        )
                    else:
                        i_dict['VALUE_LIMIT'] = dict(
                            # 8Gb
                            memory=8*1024**3,
                        )

                    dict_[i_entity_path] = i_dict

                g_p.do_update()

        if dict_:
            self.show_dialog(dict_)

    def show_dialog(self, data):
        chart_view = qt_cht_widgets.QtBarChartWidget()
        chart_view._set_name_text_('System Resource Usage')
        chart_view._set_data_(
            data,
            ['memory'],
            data_type_dict=dict(memory='file_size')
        )
        gui_core.GuiApplication.show_tool_dialog(
            widget=chart_view,
            title=gui_core.GuiUtil.choice_gui_name_auto(self._session.gui_configure.get('window')),
            size=(640, 480)
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
