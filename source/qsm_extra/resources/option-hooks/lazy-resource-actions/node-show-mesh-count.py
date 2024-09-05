# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.widgets as qt_widgets

import lxbasic.storage as bsc_storage

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
        keys = [
            'triangle',
            'triangle_per_world_area',
            'geometry_all',
            'geometry_visible'
        ]
        dict_ = {}
        with window.gui_progressing(maximum=len(scr_entities)) as g_p:
            for i_entity in scr_entities:
                i_entity_path = i_entity.path
                i_is_rig = self._scr_stage.is_exists_for_node_tag(
                    i_entity_path, '/task/rig'
                )
                if i_is_rig:
                    i_value_limit = dict(
                        triangle=1000000,
                        triangle_per_world_area=10,
                        geometry_all=1000,
                        geometry_visible=1000,
                    )
                else:
                    i_value_limit = dict(
                        triangle=50000000,
                        triangle_per_world_area=2,
                        geometry_all=10000,
                        geometry_visible=10000,
                    )
                i_dict = {
                    'VALUE_LIMIT': i_value_limit
                }
                for j_key in keys:
                    j_text = self._scr_stage.get_node_parameter(
                            i_entity_path, 'mesh_count.{}'.format(j_key)
                        )
                    if j_text is not None:
                        j_value_opt = bsc_core.BscTextOpt(j_text)
                        if j_value_opt.get_is_float():
                            j_value = int(float(j_text))
                        elif j_value_opt.get_is_integer():
                            j_value = int(j_text)
                        else:
                            j_value = 0
                    else:
                        j_value = 0

                    i_dict[j_key] = j_value

                dict_[i_entity_path] = i_dict

                g_p.do_update()

        if dict_:
            self.show_dialog(dict_)

    def show_dialog(self, data):
        chart_view = qt_widgets.QtViewForBarChart()
        chart_view._set_name_text_('Mesh Count')
        chart_view._set_data_(
            data,
            [
                # 'face',
                # 'face_per_world_area',
                'triangle',
                'triangle_per_world_area',
                'geometry_all',
                'geometry_visible'
            ]
        )

        gui_core.GuiApplication.show_tool_dialog(
            widget=chart_view,
            title=gui_core.GuiUtil.choice_name_(self._session.gui_configure.get('window')),
            size=(640, 480)
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
