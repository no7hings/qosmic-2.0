# coding:utf-8
import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import lxgui.proxy.widgets as prx_widgets

import qsm_maya.core as qsm_mya_core

import qsm_gui.proxy.widgets as qsm_prx_widgets

from ... import core as _rsc_mng_core

from . import unit_for_scenery as _unit_for_scenery


class PrxPageForSceneryResource(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = qt_widgets.QtTranslucentWidget

    SCRIPT_JOB_NAME = 'resource_manager_for_scenery'

    def _gui_filter_update_visible(self, boolean):
        self._prx_h_splitter.swap_contract_left_or_top_at(0)

    def _gui_add_main_tools(self):
        for i in [
            ('filter', 'tool/filter', '', self._gui_filter_update_visible)
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = prx_widgets.PrxToggleButton()
            self._main_prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_check_toggled_to(i_fnc)

    def _register_all_script_jobs(self):
        self._script_job = qsm_mya_core.ScriptJob(
            self.SCRIPT_JOB_NAME
        )
        self._script_job.register(
            [
                self._gui_resource_opt.do_gui_refresh_by_dcc_selection,
                self._gui_switch_opt.do_gui_refresh_by_dcc_selection,
            ],
            self._script_job.EventTypes.SelectionChanged
        )
        self._script_job.register(
            self._gui_extend_opt.do_gui_refresh_by_dcc_frame_changing,
            self._script_job.EventTypes.FrameRangeChanged
        )
        self._script_job.register(
            self.do_gui_refresh_all,
            self._script_job.EventTypes.SceneOpened
        )

    def _destroy_all_script_jobs(self):
        self._script_job.destroy()

    def do_gui_refresh_by_resource_tag_checking(self):
        filter_data_src = self._gui_resource_tag_opt.generate_semantic_tag_filter_data_src()
        qt_view = self._resource_prx_tree_view._qt_view
        qt_view._set_view_semantic_tag_filter_data_src_(filter_data_src)
        qt_view._set_view_keyword_filter_data_src_(
            self._resource_prx_tree_view.filter_bar.get_keywords()
        )
        qt_view._refresh_view_items_visible_by_any_filter_()
        qt_view._refresh_viewport_showable_auto_()

    def do_gui_refresh_by_window_active_changing(self):
        self._gui_resource_opt.do_gui_refresh_tools()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForSceneryResource, self).__init__(*args, **kwargs)
        self._window = window
        self._session = session

        self.gui_setup_unit()

    def gui_setup_unit(self):
        self._unit_assembly_load_args_array = []

        self._qt_widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        qt_lot = qt_widgets.QtVBoxLayout(self._qt_widget)
        qt_lot.setContentsMargins(*[0]*4)
        qt_lot.setSpacing(2)
        # top toolbar
        self._top_prx_tool_bar = prx_widgets.PrxHToolBar()
        qt_lot.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)
        # main tool
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )
        self._gui_add_main_tools()
        # reference tool
        self._reference_tool_box = self._top_prx_tool_bar.create_tool_box(
            'reference', size_mode=1
        )
        # reference
        self._prx_input_for_asset = qsm_prx_widgets.PrxInputForScenery()
        self._reference_tool_box.add_widget(self._prx_input_for_asset)

        self._gui_reference_opt = _unit_for_scenery.UnitForSceneryReference(
            self._window, self, self._session, self._prx_input_for_asset
        )

        self._prx_h_splitter = prx_widgets.PrxHSplitter()
        qt_lot.addWidget(self._prx_h_splitter.widget)

        self._resource_tag_tree_view = prx_widgets.PrxTreeView()
        self._prx_h_splitter.add_widget(self._resource_tag_tree_view)
        self._resource_tag_tree_view.create_header_view(
            [('name', 2)],
            self._window.get_definition_window_size()[0]
        )

        self._resource_prx_tree_view = prx_widgets.PrxTreeView()
        self._prx_h_splitter.add_widget(self._resource_prx_tree_view)
        self._prx_h_splitter.set_fixed_size_at(0, 240)
        self._prx_h_splitter.swap_contract_left_or_top_at(0)
        self._prx_h_splitter.set_contract_enable(False)

        self._gui_resource_tag_opt = _rsc_mng_core.GuiResourceTagOpt(
            self._window, self, self._session, self._resource_tag_tree_view
        )
        self._gui_resource_opt = _unit_for_scenery.UnitForSceneryView(
            self._window, self, self._session, self._resource_prx_tree_view
        )
        self._resource_tag_tree_view.connect_item_check_changed_to(
            self.do_gui_refresh_by_resource_tag_checking
        )
        # tool kit
        self._tool_prx_tab_box = prx_widgets.PrxHTabBox()
        qt_lot.addWidget(self._tool_prx_tab_box.widget)
        # utility
        self._gui_utility_opt = _unit_for_scenery.UnitForSceneryUtilityToolSet(
            self._window, self, self._session
        )
        # switch
        self._gui_switch_opt = _unit_for_scenery.UnitForScenerySwitchToolSet(
            self._window, self, self._session
        )
        # extend
        self._gui_extend_opt = _unit_for_scenery.UnitForSceneryExtendToolSet(
            self._window, self, self._session
        )

        self._gui_extend_opt.do_gui_refresh_by_camera_changing()
        self._gui_extend_opt.do_gui_refresh_by_dcc_frame_changing()

        self._register_all_script_jobs()

        self._window.connect_window_activate_changed_to(self.do_gui_refresh_by_window_active_changing)
        self._window.connect_window_close_to(self._destroy_all_script_jobs)
        self._tool_prx_tab_box.connect_current_changed_to(self.do_gui_refresh_tabs)

    def gui_get_tool_tab_box(self):
        return self._tool_prx_tab_box

    def do_gui_refresh_all(self, force=False):
        self._top_prx_tool_bar.do_gui_refresh()
        is_changed = self._gui_resource_opt.get_resources_query().do_update()
        if is_changed is True or force is True:
            self._gui_resource_tag_opt.restore()
            self._gui_resource_tag_opt.gui_add_root()

            self._gui_resource_opt.restore()
            self._gui_resource_opt.gui_add_all()

        self._gui_resource_opt.do_gui_refresh_by_dcc_selection()
        self._gui_resource_opt.do_gui_refresh_tools()

        self.do_gui_refresh_tabs()

    def gui_get_current_tool_tab_key(self):
        return self._tool_prx_tab_box.get_current_key()

    def do_gui_refresh_tabs(self):
        self._gui_switch_opt.do_gui_refresh_by_dcc_selection()