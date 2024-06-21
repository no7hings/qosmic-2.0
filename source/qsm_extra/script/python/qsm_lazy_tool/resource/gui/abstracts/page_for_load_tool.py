# coding:utf-8
import copy

import functools

import six

import lxbasic.core as bsc_core

import lxbasic.content as bsc_content

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_screw.core as qsm_scr_core


class AbsPrxPageForLoad(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    def do_gui_update_by_dcc_selection(self):
        pass

    def generate_excludes(self):
        excludes = []
        if self._prx_options_node.get('ignore.translate') is True:
            excludes.extend(['translate.translateX', 'translate.translateY', 'translate.translateZ'])
        if self._prx_options_node.get('ignore.rotate') is True:
            excludes.extend(['rotate.rotateX', 'rotate.rotateY', 'rotate.rotateZ'])
        if self._prx_options_node.get('ignore.scale') is True:
            excludes.extend(['scale.scaleX', 'scale.scaleY', 'scale.scaleZ'])
        return excludes

    def generate_key_includes(self):
        return [x.name for x in self._prx_options_node.get('data')]

    def ao_apply(self):
        pass

    def do_create_and_apply(self):
        pass

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForLoad, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self._all_scr_stage_keys = qsm_scr_core.Stage.get_all_keys()
        self._scr_stage_key = self._all_scr_stage_keys[0]
        self._scr_stage = None

        self._node_opt_list = []
        self._node_creator_list = []

        self._node_rebuild_data = None

        self._data = None

        self.gui_setup_page()

    def do_gui_show_data(self, data):
        if data != self._data:
            self._data = data
            content = bsc_content.Content(value=self._data)
            path_opts = map(lambda x: bsc_core.BscPathOpt('/{}'.format(x)), content.get_top_keys())
            self._prx_options_node.set(
                'data', path_opts
            )

    def gui_setup_page(self):
        qt_lot = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        qt_lot.setContentsMargins(*[0]*4)
        qt_lot.setSpacing(2)

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        qt_lot.addWidget(prx_sca.widget)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.load.options')
            )
        )

        prx_sca.add_widget(self._prx_options_node)

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.load.options.parameters')
        )

        if self._window._language == 'chs':
            gui_names = [
                qsm_scr_core.Stage.get_configure(x).get('options.gui_name_chs')
                for x in self._all_scr_stage_keys
            ]
        else:
            gui_names = [
                qsm_scr_core.Stage.get_configure(x).get('options.gui_name')
                for x in self._all_scr_stage_keys
            ]

        self._prx_options_node.get_port('stage').set_options(
            self._all_scr_stage_keys, gui_names
        )
        self._prx_options_node.get_port('search_scheme').connect_input_changed_to(
            self.do_gui_update_by_dcc_selection
        )

        self._prx_options_node.set(
            'automatic.create_and_apply', self.do_create_and_apply
        )
        # tip
        self._tip_prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        prx_sca.add_widget(self._tip_prx_tool_group)
        self._tip_prx_tool_group.set_expanded(True)
        self._tip_prx_tool_group.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.load.tip')
            )
        )
        self._tip_prx_text_browser = gui_prx_widgets.PrxTextBrowser()
        self._tip_prx_tool_group.add_widget(self._tip_prx_text_browser)
        self._tip_prx_text_browser.set_content(
            gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.load.tip')
            )
        )

    def do_gui_refresh_all(self):
        node_context = qsm_scr_core.NodeContext.read()
        if node_context:
            self._prx_options_node.set_dict(
                node_context
            )
            json_path = node_context.get('file')
            self._node_rebuild_data = bsc_storage.StgFileOpt(json_path).set_read()
            if self._node_rebuild_data:
                self.do_gui_show_data(self._node_rebuild_data['data'])
        else:
            self._prx_options_node.set_reset()
