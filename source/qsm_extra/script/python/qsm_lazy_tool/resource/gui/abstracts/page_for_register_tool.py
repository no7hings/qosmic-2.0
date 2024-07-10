# coding:utf-8
import copy

import functools

import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.resource as bsc_resource

import lxbasic.pinyin as bsc_pinyin

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_lazy.core as qsm_lzy_core


class AbsPrxPageForRegisterTool(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    def do_gui_update_by_dcc_selection(self):
        pass

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForRegisterTool, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self._all_lzy_stage_keys = qsm_lzy_core.Stage.get_all_keys()
        self._lzy_stage_key = self._all_lzy_stage_keys[0]
        self._lzy_stage = None

        self._dcc_node_opt = None
        self._dcc_node_graph_opt = None

        self.gui_setup_page()

        self._window.register_window_close_method(self.do_gui_close)

    def _do_gui_load_stage(self):
        key = self._prx_options_node.get('stage')
        if self._lzy_stage is not None:
            self._lzy_stage.close()

        self._lzy_stage_key = key
        self._lzy_stage = qsm_lzy_core.Stage(
            self._lzy_stage_key
        )
        self.do_gui_add_types()
        self.do_gui_add_tags()
        
        self.do_gui_load_data_types()

        self.do_gui_update_by_dcc_selection()
        
    def do_gui_load_data_types(self):
        configure = qsm_lzy_core.Stage.get_configure(self._lzy_stage_key)
        values = configure.get('options.data_types')

        pot = self._prx_options_node.get_port('data_type')
        if values:
            if self._window._language == 'chs':
                value_names = [qsm_lzy_core.DataTypes.NAME_CHS_MAP[x] for x in values]
            else:
                value_names = [qsm_lzy_core.DataTypes.NAME_MAP[x] for x in values]

            pot.set_options(
                values, value_names
            )
            pot.set(values[0])
        else:
            pot.set([])

    def do_gui_add_types(self):
        self._type_prx_tag_input.restore()

        for i in self._lzy_stage.find_all(
            self._lzy_stage.EntityTypes.Type,
            filters=[
                ('category', 'is', 'group'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_gui_name = i.gui_name
            if self._window._language == 'chs':
                i_gui_name = i.gui_name_chs

            i_group = self._type_prx_tag_input.create_group(i.path, show_name=i_gui_name)

            i_group._set_expanded_(True)

            i_group._set_tool_tip_(i.to_description())

        for i in self._lzy_stage.find_all(
            self._lzy_stage.EntityTypes.Type,
            filters=[
                ('category', 'is', 'node'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_gui_name = i.gui_name
            if self._window._language == 'chs':
                i_gui_name = i.gui_name_chs

            i_node = self._type_prx_tag_input.create_node(i.path, show_name=i_gui_name)

            i_node._set_tool_tip_(i.to_description())

    def do_gui_add_tags(self):
        self._tag_prx_tag_input.restore()

        for i in self._lzy_stage.find_all(
            self._lzy_stage.EntityTypes.Tag,
            filters=[
                ('category', 'is', 'group'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_gui_name = i.gui_name
            if self._window._language == 'chs':
                i_gui_name = i.gui_name_chs

            i_group = self._tag_prx_tag_input.create_group(i.path, show_name=i_gui_name)

            i_group._set_expanded_(True)

            i_group._set_tool_tip_(i.to_description())

        for i in self._lzy_stage.find_all(
            self._lzy_stage.EntityTypes.Tag,
            filters=[
                ('category', 'is', 'node'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_gui_name = i.gui_name
            if self._window._language == 'chs':
                i_gui_name = i.gui_name_chs

            i_node = self._tag_prx_tag_input.create_node(i.path, show_name=i_gui_name)

            i_node._set_tool_tip_(i.to_description())

    @staticmethod
    def _generate_screenshot_file_path():
        d = bsc_core.BscSystem.get_home_directory()
        return six.u('{}/screenshot/untitled-{}.mov').format(d, bsc_core.TimeExtraMtd.generate_time_tag_36())

    def do_show_playblast_window(self):
        raise NotImplementedError()

    def do_create_playblast(self):
        raise NotImplementedError()

    def do_gui_close(self):
        self._lzy_stage.close()

    def get_resource_data_type(self):
        return self._prx_options_node.get('data_type')

    def get_data(self):
        raise NotImplementedError()

    def do_gui_update_options_by_name_change(self):
        gui_name_chs = self._prx_options_node.get('gui_name_chs')
        if gui_name_chs:
            name = bsc_pinyin.Text.to_pinyin_name(gui_name_chs)
            path = '/{}'.format(name)
            self._prx_options_node.set('path', path)
            gui_name = bsc_core.RawTextMtd.to_prettify(name)
            self._prx_options_node.set('gui_name', gui_name)
        else:
            self._prx_options_node.set('path', '')
            self._prx_options_node.set('gui_name', '')

    def ao_apply(self):
        data = self.get_data()
        if not data:
            self._window.exec_message(
                gui_core.GuiUtil.choice_message(
                    self._window._language, self._window._configure.get('build.register.messages.node')
                ),
                status='warning'
            )
            return

        options = self._prx_options_node.to_dict()
        gui_name_chs = options.get('gui_name_chs')
        if not gui_name_chs:
            self._window.exec_message(
                gui_core.GuiUtil.choice_message(
                    self._window._language, self._window._configure.get('build.register.messages.name_empty')
                ),
                status='warning'
            )
            return

        gui_name = options.get('gui_name')

        preview_files = self._prx_options_node.get('preview')
        if not preview_files:
            self._window.exec_message(
                gui_core.GuiUtil.choice_message(
                    self._window._language, self._window._configure.get('build.register.messages.preview')
                ),
                status='warning'
            )
            return

        node_path = options.get('path')
        if self._lzy_stage.check_node_exists(node_path) is True:
            self._window.exec_message(
                gui_core.GuiUtil.choice_message(
                    self._window._language, self._window._configure.get('build.register.messages.name_exists')
                ),
                status='warning'
            )
            return

        type_paths = self._type_prx_tag_input.get_all_checked_node_paths()
        if not type_paths:
            self._window.exec_message(
                gui_core.GuiUtil.choice_message(
                    self._window._language, self._window._configure.get('build.register.messages.type')
                ),
                status='warning'
            )
            return

        tag_paths = self._tag_prx_tag_input.get_all_checked_node_paths()
        if not tag_paths:
            self._window.exec_message(
                gui_core.GuiUtil.choice_message(
                    self._window._language, self._window._configure.get('build.register.messages.tag')
                ),
                status='warning'
            )
            return

        self._lzy_stage.create_node(
            node_path, gui_name=gui_name, gui_name_chs=gui_name_chs
        )

        for i_type_path in type_paths:
            self._lzy_stage.create_type_assign(
                node_path, i_type_path
            )

        for i_tag_path in tag_paths:
            self._lzy_stage.create_tag_assign(
                node_path, i_tag_path
            )

        file_path = preview_files[-1]

        self._lzy_stage.upload_node_media(
            node_path, file_path
        )
        
        data_type = self.get_resource_data_type()
        if data_type == qsm_lzy_core.DataTypes.MayaNode:
            self._lzy_stage.upload_node_json(
                node_path, qsm_lzy_core.DataTypes.MayaNode, data
            )
            self._lzy_stage.create_or_update_parameters(
                node_path, 'data_type', qsm_lzy_core.DataTypes.MayaNode
            )
        elif data_type == qsm_lzy_core.DataTypes.MayaNodeGraph:
            self._lzy_stage.upload_node_maya_scene(
                node_path, qsm_lzy_core.DataTypes.MayaNodeGraph, data
            )
            self._lzy_stage.create_or_update_parameters(
                node_path, 'data_type', qsm_lzy_core.DataTypes.MayaNodeGraph
            )
        self._window.exec_message(
            gui_core.GuiUtil.choice_message(
                self._window._language, self._window._configure.get('build.register.messages.successful')
            ),
            status='correct'
        )

    def gui_setup_page(self):
        v_qt_lot = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        v_qt_lot.setContentsMargins(*[0]*4)
        v_qt_lot.setSpacing(2)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.register.options')
            )
        )

        v_qt_lot.addWidget(self._prx_options_node.widget)

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.register.options.parameters')
        )

        self._prx_options_node.get_port('gui_name_chs').connect_input_changed_to(
            self.do_gui_update_options_by_name_change
        )

        self._prx_options_node.set('playblast.show_window', self.do_show_playblast_window)
        self._prx_options_node.set('playblast.create', self.do_create_playblast)

        self._type_prx_tag_input = gui_prx_widgets.PrxTagInput()

        self._prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        v_qt_lot.addWidget(self._prx_tool_group.widget)
        self._prx_tool_group.set_expanded(True)
        self._prx_tool_group.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.register.filter')
            )
        )
        qt_widget_0 = gui_qt_widgets.QtTranslucentWidget()
        self._prx_tool_group.add_widget(qt_widget_0)
        h_qt_lot_0 = gui_qt_widgets.QtHBoxLayout(qt_widget_0)
        h_qt_lot_0.addWidget(
            self._type_prx_tag_input.widget
        )

        self._tag_prx_tag_input = gui_prx_widgets.PrxTagInput()
        h_qt_lot_0.addWidget(
            self._tag_prx_tag_input.widget
        )

        if self._window._language == 'chs':
            gui_names = [
                qsm_lzy_core.Stage.get_configure(x).get('options.gui_name_chs')
                for x in self._all_lzy_stage_keys
            ]
        else:
            gui_names = [
                qsm_lzy_core.Stage.get_configure(x).get('options.gui_name')
                for x in self._all_lzy_stage_keys
            ]

        self._prx_options_node.get_port('stage').set_options(
            self._all_lzy_stage_keys, gui_names
        )

        self._prx_options_node.get_port('stage').connect_input_changed_to(
            self._do_gui_load_stage
        )

        self._prx_options_node.get_port('data_type').connect_input_changed_to(
            self.do_gui_update_by_dcc_selection
        )

    def do_gui_refresh_all(self):
        self._do_gui_load_stage()
        self.do_gui_update_by_dcc_selection()

