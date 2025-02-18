# coding:utf-8
import lxgui.core as gui_core

import lxgui.qt.chart_widgets as qt_cht_widgets

import lxbasic.storage as bsc_storage

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

            scr_entities = node_opt.gui_get_selected_scr_entities()
            if scr_entities:
                self.show_one(scr_entities[0])

    def show_one(self, scr_entity):
        entity_path = scr_entity.path
        file_path = self._scr_stage.get_node_parameter(scr_entity.path, 'mesh_count')
        if file_path:
            data_0 = bsc_storage.StgFileOpt(file_path).set_read()
            if data_0:
                mesh_count_data = data_0['mesh_count']
                dict_ = {}
                dict_.update(mesh_count_data['components'])
                dict_.update(mesh_count_data.get('gpu_caches', {}))
                is_rig = self._scr_stage.is_exists_node_tag(
                    entity_path, '/task/rig'
                )
                if is_rig:
                    dict_['VALUE_LIMIT'] = dict(
                        triangle=100000,
                        triangle_per_world_area=20,
                    )
                else:
                    dict_['VALUE_LIMIT'] = dict(
                        triangle=500000,
                        triangle_per_world_area=10,
                    )
                if dict_:
                    self.show_dialog(dict_)

    def show_dialog(self, data):
        chart_view = qt_cht_widgets.QtBarChartWidget()
        chart_view._set_name_text_('Mesh Count')
        if gui_core.GuiUtil.get_language() == 'chs':
            data_key_names = ['三角面数', '三角面数（单位面积）']
        else:
            data_key_names = None

        chart_view._set_data_(
            data,
            [
                # 'face',
                # 'face_per_world_area',
                'triangle',
                'triangle_per_world_area'
            ],
            data_key_names=data_key_names
        )
        gui_core.GuiApplication.show_tool_dialog(
            widget=chart_view,
            title=gui_core.GuiUtil.choice_gui_name_auto(self._session.gui_configure.get('window')),
            size=(640, 480)
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
