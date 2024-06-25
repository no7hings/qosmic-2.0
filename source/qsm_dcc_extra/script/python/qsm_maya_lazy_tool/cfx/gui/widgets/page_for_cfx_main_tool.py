# coding:utf-8
import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya_gui.core as qsm_mya_gui_core

from . import unit_for_cfx_main_tool as _unit_for_cfx_rig


class PrxPageForCfxMainTool(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget
    
    UNIT_FOR_MAIN_TOOL_CLS = _unit_for_cfx_rig.UnitForCfxRigView

    SCRIPT_JOB_NAME = 'lazy_tool_for_cfx'

    def do_gui_refresh_by_resource_tag_checking(self):
        filter_data_src = self._gui_resource_tag_prx_unit.generate_semantic_tag_filter_data_src()
        qt_view = self._resource_prx_tree_view._qt_view
        qt_view._set_view_semantic_tag_filter_data_src_(filter_data_src)
        qt_view._set_view_keyword_filter_data_src_(
            self._resource_prx_tree_view.filter_bar.get_keywords()
        )
        qt_view._refresh_view_items_visible_by_any_filter_()
        qt_view._refresh_viewport_showable_auto_()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForCfxMainTool, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self.gui_setup_page()

    def _do_dcc_register_all_script_jobs(self):
        self._script_job = qsm_mya_core.ScriptJob(
            self.SCRIPT_JOB_NAME
        )
        self._script_job.register(
            [
                self._gui_resource_prx_unit.do_gui_refresh_by_dcc_selection,
            ],
            self._script_job.EventTypes.SelectionChanged
        )
        self._script_job.register(
            self._gui_export_tool_set_unit.do_gui_refresh_by_dcc_frame_changing,
            self._script_job.EventTypes.FrameRangeChanged
        )
        self._script_job.register(
            self.do_gui_refresh_all,
            self._script_job.EventTypes.SceneOpened
        )

    def _do_dcc_destroy_all_script_jobs(self):
        self._script_job.destroy()

    def _gui_filter_update_visible(self, boolean):
        self._prx_h_splitter.swap_contract_left_or_top_at(0)

    def _gui_add_main_tools(self):
        for i in [
            ('filter', 'tool/filter', '', self._gui_filter_update_visible)
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxToggleButton()
            self._main_prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_check_toggled_to(i_fnc)

    def gui_get_tool_tab_box(self):
        return self._page_prx_tab_box
    
    def gui_get_tool_tab_current_key(self):
        return self._page_prx_tab_box.get_current_key()

    def _do_gui_build_selection_scheme(self):
        options = self._window._configure.get('build.rig_selection_scheme.options')
        default = self._window._configure.get('build.rig_selection_scheme.default')
        if self._window._language == 'chs':
            option_names_chs = self._window._configure.get('build.rig_selection_scheme.option_names_chs')
            self._selection_scheme_prx_input.set_options(
                options, option_names_chs
            )
        else:
            self._selection_scheme_prx_input.set_options(
                options
            )

        self._selection_scheme_prx_input.set(default)
        self._selection_scheme_prx_input.set_tool_tip(
            self._window.choice_tool_tip(
                self._window._configure.get('build.rig_selection_scheme')
            )
        )

        self._selection_scheme_prx_input.connect_input_changed_to(
            self._gui_resource_prx_unit.do_dcc_refresh_resources_selection
        )

    def gui_get_selection_scheme(self):
        return self._selection_scheme_prx_input.get()

    def gui_setup_page(self):
        self._qt_widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        qt_lot = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        qt_lot.setContentsMargins(*[0]*4)
        qt_lot.setSpacing(2)

        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        qt_lot.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)
        # main tool box
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )
        self._gui_add_main_tools()

        self._prx_h_splitter = gui_prx_widgets.PrxHSplitter()
        qt_lot.addWidget(self._prx_h_splitter.widget)
        # resource tag
        self._resource_tag_tree_view = gui_prx_widgets.PrxTreeView()
        self._prx_h_splitter.add_widget(self._resource_tag_tree_view)
        self._resource_tag_tree_view.create_header_view(
            [('name', 2)],
            self._window.get_definition_window_size()[0]
        )

        self._gui_resource_tag_prx_unit = qsm_mya_gui_core.PrxUnitForResourceTagOpt(
            self._window, self, self._session, self._resource_tag_tree_view
        )
        # resource
        self._resource_prx_tree_view = gui_prx_widgets.PrxTreeView()
        self._prx_h_splitter.add_widget(self._resource_prx_tree_view)
        self._prx_h_splitter.set_fixed_size_at(0, 240)
        self._prx_h_splitter.swap_contract_left_or_top_at(0)
        self._prx_h_splitter.set_contract_enable(False)

        self._gui_resource_prx_unit = _unit_for_cfx_rig.UnitForCfxRigView(
            self._window, self, self._session, self._resource_prx_tree_view
        )
        self._resource_tag_tree_view.connect_item_check_changed_to(
            self.do_gui_refresh_by_resource_tag_checking
        )
        # selection scheme
        self._selection_scheme_prx_input = gui_prx_widgets.PrxInputAsCapsule()
        qt_lot.addWidget(self._selection_scheme_prx_input.widget)
        self._do_gui_build_selection_scheme()
        # tool set
        self._page_prx_tab_box = gui_prx_widgets.PrxHTabBox()
        qt_lot.addWidget(self._page_prx_tab_box.widget)
        # export
        self._gui_export_tool_set_unit = _unit_for_cfx_rig.ToolSetUnitForCfxRigExport(
            self._window, self, self._session
        )
        # import
        self._gui_import_tool_set_unit = _unit_for_cfx_rig.ToolSetUnitForCfxRigImport(
            self._window, self, self._session
        )

        self._do_dcc_register_all_script_jobs()
        self._window.connect_window_close_to(self._do_dcc_destroy_all_script_jobs)
        
        self._page_prx_tab_box.connect_current_changed_to(self.do_gui_refresh_units)
        self._page_prx_tab_box.set_history_key('lazy-cfx-tool.main_page_key_current')
        self._page_prx_tab_box.load_history()

    def do_gui_refresh_all(self, force=False):
        self._top_prx_tool_bar.do_gui_refresh()
        is_changed = self._gui_resource_prx_unit.get_resources_query().do_update()
        if is_changed is True or force is True:
            self._gui_resource_tag_prx_unit.restore()
            self._gui_resource_tag_prx_unit.gui_add_root()

            self._gui_resource_prx_unit.restore()
            self._gui_resource_prx_unit.gui_add_all()

        self._gui_resource_prx_unit.do_gui_refresh_by_dcc_selection()
        self._gui_resource_prx_unit.do_gui_refresh_tools()

        self.do_gui_refresh_units()

    def do_gui_refresh_units(self):
        if self.gui_get_tool_tab_current_key() == 'import':
            pass
