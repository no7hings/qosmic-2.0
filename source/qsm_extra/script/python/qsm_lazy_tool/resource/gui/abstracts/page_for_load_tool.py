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

import qsm_general.dotfile as qsm_gnl_dotfile

import qsm_lazy.core as qsm_lzy_core


class AbsPrxPageForLoadTool(gui_prx_abstracts.AbsPrxWidget):
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
        return [x.name for x in self._prx_options_node.get('node_data')]

    def do_apply(self):
        pass

    def do_create_and_apply(self):
        pass

    def get_resource_data_type(self):
        return self._prx_options_node.get('data_type')

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForLoadTool, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self._all_lzy_stage_keys = qsm_lzy_core.Stage.get_all_keys()
        self._lzy_stage_key = self._all_lzy_stage_keys[0]
        self._lzy_stage = None

        self._dcc_node_opt_list = []
        self._dcc_node_creator_list = []
        
        self._dcc_node_graph_opt = None

        self._lzy_data_file_path = None

        self._lzy_data_for_node = None

        self.gui_setup_page()

    def do_gui_update_file(self, file_path):
        # file opt put first
        if self._lzy_data_file_path != file_path:
            self._lzy_data_file_path = file_path
            file_opt = bsc_storage.StgFileOpt(file_path)
            if file_opt.ext == '.json':
                node_data = file_opt.set_read()
                self._lzy_data_for_node = node_data
                content = bsc_content.Content(value=node_data['data'])
                path_opts = map(lambda x: bsc_core.BscPathOpt('/{}'.format(x)), content.get_top_keys())
                self._prx_options_node.set(
                    'node_data', path_opts
                )
            elif file_opt.ext == '.ma':
                node_dict = qsm_gnl_dotfile.MayaAscii(file_path).get_node_dict()
                path_opts = map(lambda x: bsc_core.BscPathOpt('/{}'.format(x)), node_dict.keys())
                self._prx_options_node.set(
                    'node_data', path_opts
                )

    def do_gui_load_data_types(self):
        values = qsm_lzy_core.DataTypes.All
        pot = self._prx_options_node.get_port('data_type')
        if self._window._language == 'chs':
            value_names = [qsm_lzy_core.DataTypes.NAME_CHS_MAP[x] for x in values]
        else:
            value_names = [qsm_lzy_core.DataTypes.NAME_MAP[x] for x in values]

        pot.set_options(
            values, value_names
        )
        pot.set(values[0])

    def gui_setup_page(self):
        v_qt_lot = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        v_qt_lot.setContentsMargins(*[0]*4)
        v_qt_lot.setSpacing(2)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.load.options')
            )
        )

        v_qt_lot.addWidget(self._prx_options_node.widget)

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.load.options.parameters')
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

        self._prx_options_node.set(
            'automatic.create_and_apply', self.do_create_and_apply
        )

        self.do_gui_load_data_types()
        # tip
        self._tip_prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        v_qt_lot.addWidget(self._tip_prx_tool_group.widget)
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
        node_context = qsm_lzy_core.DataContext.read()
        if node_context:
            self._prx_options_node.set_dict(
                node_context
            )
            file_path = node_context.get('file')
            if bsc_storage.StgPath.get_is_file(file_path):
                self.do_gui_update_file(file_path)
        else:
            self._prx_options_node.set_reset()
