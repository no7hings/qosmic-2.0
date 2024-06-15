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

import qsm_screw.core as qsm_scr_core


class AbsPrxPageForRegister(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    def do_gui_update_by_dcc_selection(self):
        print 'AAAA'

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForRegister, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self._configure = bsc_resource.RscExtendConfigure.get_as_content(
            'lazy/resource/register'
        )
        self._scr_key = 'node'
        self._scr_stage = qsm_scr_core.Stage(
            self._scr_key
        )
        self._scr_stage.connect()

        self._window.connect_window_close_to(self._scr_stage.close)

        self.gui_setup_page()

    def gui_setup_page(self):
        v_qt_lot_0 = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        v_qt_lot_0.setContentsMargins(*[0]*4)
        v_qt_lot_0.setSpacing(2)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            'Options'
        )

        v_qt_lot_0.addWidget(self._prx_options_node.widget)

        self._prx_options_node.build_by_data(
            self._configure.get('build.main.parameters')
        )

        self._prx_options_node.get_port('gui_name_chs').connect_input_changed_to(
            self.update_options_by_name_changed
        )
        
        self._prx_options_node.set('playblast.show_window', self.show_playblast_window)
        self._prx_options_node.set('playblast.create', self.create_playblast)

        self._type_prx_tag_input = gui_prx_widgets.PrxTagInput()

        self._prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        v_qt_lot_0.addWidget(self._prx_tool_group.widget)
        self._prx_tool_group.set_expanded(True)
        self._prx_tool_group.set_name('Type & Tag')
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

        self._prx_options_node.get_port('stage').connect_input_changed_to(
            self._do_gui_switch_stage
        )

        self.do_gui_refresh_all()

    def _do_gui_switch_stage(self):
        key = self._prx_options_node.get('stage')
        if self._scr_stage is not None:
            self._scr_stage.close()
            self._scr_key = key
            self._scr_stage = qsm_scr_core.Stage(
                self._scr_key
            )
            self._scr_stage.connect()
            self.do_gui_refresh_all()

    def do_gui_add_types(self):
        self._type_prx_tag_input.restore()

        for i in self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Type,
            filters=[
                ('category', 'is', 'group'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_group = self._type_prx_tag_input.create_group(i.path, show_name=i.gui_name_chs)

            i_group._set_expanded_(True)

            i_group._set_tool_tip_(i.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))

        for i in self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Type,
            filters=[
                ('category', 'is', 'node'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_node = self._type_prx_tag_input.create_node(i.path, show_name=i.gui_name_chs)

            i_node._set_tool_tip_(i.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))

    def do_gui_add_tags(self):
        self._tag_prx_tag_input.restore()

        for i in self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Tag,
            filters=[
                ('category', 'is', 'group'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_group = self._tag_prx_tag_input.create_group(i.path, show_name=i.gui_name_chs)

            i_group._set_expanded_(True)

            i_group._set_tool_tip_(i.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))

        for i in self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Tag,
            filters=[
                ('category', 'is', 'node'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_node = self._tag_prx_tag_input.create_node(i.path, show_name=i.gui_name_chs)

            i_node._set_tool_tip_(i.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))

    def do_gui_refresh_all(self):
        self.do_gui_add_types()
        self.do_gui_add_tags()
    
    @staticmethod
    def _generate_screenshot_file_path():
        d = bsc_core.BscSystem.get_home_directory()
        return six.u('{}/screenshot/untitled-{}.mov').format(d, bsc_core.TimeExtraMtd.generate_time_tag_36())

    def show_playblast_window(self):
        raise NotImplementedError()

    def create_playblast(self):
        raise NotImplementedError()

    def get_data(self):
        raise NotImplementedError()

    def update_options_by_name_changed(self):
        gui_name_chs = self._prx_options_node.get('gui_name_chs')
        if gui_name_chs:
            name = bsc_pinyin.Text.to_pinyin(gui_name_chs)
            self._prx_options_node.set('name', name)
            gui_name = bsc_core.RawTextMtd.to_prettify(name)
            self._prx_options_node.set('gui_name', gui_name)
        else:
            self._prx_options_node.set('name', '')
            self._prx_options_node.set('gui_name', '')

    def do_register(self):
        data = self.get_data()

        if not data:
            self._window.exec_message('Data is not valid.')
            return

        options = self._prx_options_node.to_dict()
        gui_name_chs = options.get('gui_name_chs')
        if not gui_name_chs:
            self._window.exec_message('Name is empty.')
            return

        name = options.get('name')
        gui_name = options.get('gui_name')

        media_files = self._prx_options_node.get('media')
        if not media_files:
            self._window.exec_message('Add one or more video / Image.')
            return

        node_path = '/{}/{}'.format(self._scr_key, name)
        if self._scr_stage.check_node_exists(node_path) is True:
            self._window.exec_message('Name is exists.')
            return

        # data = self.get_data()
        type_paths = self._type_prx_tag_input.get_all_checked_node_paths()
        if not type_paths:
            self._window.exec_message('Check one or more Type.')
            return

        tag_paths = self._tag_prx_tag_input.get_all_checked_node_paths()
        if not type_paths:
            self._window.exec_message('Check one or more Tag.')
            return

        self._scr_stage.create_node(
            node_path, gui_name=gui_name, gui_name_chs=gui_name_chs
        )

        for i_type_path in type_paths:
            self._scr_stage.create_type_assign(
                node_path, i_type_path
            )

        for i_tag_path in tag_paths:
            self._scr_stage.create_tag_assign(
                node_path, i_tag_path
            )

        file_path = media_files[-1]

        self._scr_stage.upload_node_media(
            node_path, file_path
        )
