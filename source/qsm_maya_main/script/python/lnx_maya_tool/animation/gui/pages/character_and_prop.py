# coding:utf-8
import lxgui.qt.core as gui_qt_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

import lnx_dcc_tool_prc.gui.proxy.widgets as lzy_gui_prx_widgets

import lnx_maya_gui.core as qsm_mya_gui_core

from ..toolsets import character_and_prop as _toolsets_character_and_prop


class PrxPageForCharacterAndProp(gui_prx_widgets.PrxBasePage):
    SCRIPT_JOB_NAME = 'lazy_tool_for_character_and_prop'

    def do_gui_refresh_by_resource_tag_checking(self):
        filter_data_src = self._gui_asset_tag_filter_prx_unit.generate_semantic_tag_filter_data_src()
        qt_view = self._asset_prx_tree_view._qt_view
        qt_view._set_view_semantic_tag_filter_data_src_(filter_data_src)
        qt_view._set_view_keyword_filter_data_src_(
            self._asset_prx_tree_view.filter_bar.get_keywords()
        )
        qt_view._refresh_view_items_visible_by_any_filter_()
        qt_view._refresh_viewport_showable_auto_()

    def do_gui_refresh_by_window_active_changing(self):
        self._gui_asset_prx_unit.do_gui_refresh_tools()

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

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForCharacterAndProp, self).__init__(window, session, *args, **kwargs)

        self.gui_page_setup_fnc()

    def _do_dcc_register_all_script_jobs(self):
        self._script_job_opt = qsm_mya_core.ScriptJobOpt(
            self.SCRIPT_JOB_NAME
        )
        self._script_job_opt.register(
            [
                self._gui_asset_prx_unit.do_gui_refresh_by_dcc_selection,
                self._gui_skin_proxy_prx_toolset_unit.do_gui_refresh_by_dcc_selection,
            ],
            self._script_job_opt.EventTypes.SelectionChanged
        )
        self._script_job_opt.register(
            self._gui_skin_proxy_prx_toolset_unit.do_gui_refresh_by_dcc_frame_changing,
            self._script_job_opt.EventTypes.FrameRangeChanged
        )

        self._script_job_opt.register(
            self.do_gui_refresh_all,
            self._script_job_opt.EventTypes.SceneNew
        )
        self._script_job_opt.register(
            self.do_gui_refresh_all,
            self._script_job_opt.EventTypes.SceneOpened
        )
        self._script_job_opt.register(
            self.do_gui_refresh_all,
            self._script_job_opt.EventTypes.SceneSaved
        )

    def _do_dcc_destroy_all_script_jobs(self):
        self._script_job_opt.destroy()

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
            self._window.choice_gui_tool_tip(
                self._window._configure.get('build.rig_selection_scheme')
            )
        )

        self._selection_scheme_prx_input.set_history_key(
            [self._window.GUI_KEY, '{}.page'.format(self._gui_path)]
        )
        self._selection_scheme_prx_input.pull_history_latest()

        self._selection_scheme_prx_input.connect_input_changed_to(
            self._gui_asset_prx_unit.do_dcc_refresh_resources_selection
        )

    def gui_get_selection_scheme(self):
        return self._selection_scheme_prx_input.get()

    def gui_get_tool_tab_box(self):
        return self._page_prx_tab_tool_box

    def gui_get_tool_tab_current_key(self):
        return self._page_prx_tab_tool_box.get_current_key()

    def gui_page_setup_fnc(self):
        self._dynamic_gpu_load_args_array = []

        self._qt_widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )

        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)
        # main tool box
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )
        self._gui_add_main_tools()
        # reference tool
        self._asset_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'reference', size_mode=1
        )
        # reference
        self._asset_prx_input = lzy_gui_prx_widgets.PrxInputForAssetCharacterAndProp()
        self._asset_prx_tool_box.add_widget(self._asset_prx_input)
        # self._asset_prx_input.widget.setMaximumWidth(488)

        self._gui_rig_reference_prx_toolbar_unit = _toolsets_character_and_prop.PrxToolbarForCharacterAndPropReference(
            self._window, self, self._session, self._asset_prx_input
        )

        self._prx_h_splitter = gui_prx_widgets.PrxHSplitter()
        self._qt_layout.addWidget(self._prx_h_splitter.widget)
        # resource tag
        self._asset_tag_filter_tree_view = gui_prx_widgets.PrxTreeView()
        self._prx_h_splitter.add_widget(self._asset_tag_filter_tree_view)
        self._asset_tag_filter_tree_view.create_header_view(
            [('name', 2)],
            self._window.get_definition_window_size()[0]
        )

        self._gui_asset_tag_filter_prx_unit = qsm_mya_gui_core.PrxTreeviewUnitForAssetTagFilterOpt(
            self._window, self, self._session, self._asset_tag_filter_tree_view
        )
        # resource
        self._asset_prx_tree_view = gui_prx_widgets.PrxTreeView()
        self._prx_h_splitter.add_widget(self._asset_prx_tree_view)
        self._prx_h_splitter.set_fixed_size_at(0, 240)
        self._prx_h_splitter.swap_contract_left_or_top_at(0)
        self._prx_h_splitter.set_contract_enable(False)

        self._gui_asset_prx_unit = _toolsets_character_and_prop.PrxUnitForRigAssetView(
            self._window, self, self._session, self._asset_prx_tree_view
        )
        self._asset_tag_filter_tree_view.connect_item_check_changed_to(
            self.do_gui_refresh_by_resource_tag_checking
        )
        # selection scheme
        self._selection_scheme_prx_input = gui_prx_widgets.PrxInputForCapsule()
        self._qt_layout.addWidget(self._selection_scheme_prx_input.widget)
        self._do_gui_build_selection_scheme()
        # tool set
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self._qt_layout.addWidget(self._page_prx_tab_tool_box.widget)
        self._page_prx_tab_tool_box.set_expand_enable(True)
        # utility
        self._gui_skin_proxy_prx_toolset_unit = _toolsets_character_and_prop.PrxToolsetForSkinProxyLoad(
            self._window, self, self._session
        )
        # extend
        # self._gui_motion_opt = _toolsets_character_and_prop.PrxToolsetForMotion(
        #     self._window, self, self._session
        # )

        self._do_dcc_register_all_script_jobs()
        self._window.register_window_close_method(self._do_dcc_destroy_all_script_jobs)

        self._window.connect_window_activate_changed_to(self.do_gui_refresh_by_window_active_changing)
        self._page_prx_tab_tool_box.connect_current_changed_to(self.do_gui_refresh_toolset_units)
        self._page_prx_tab_tool_box.set_history_key(
            [self._window.GUI_KEY, '{}.page'.format(self._gui_path)]
        )
        self._page_prx_tab_tool_box.load_history()

    def gui_setup_post_fnc(self):
        self._top_prx_tool_bar.do_gui_refresh()

    def do_gui_refresh_all(self, force=False):
        self._top_prx_tool_bar.do_gui_refresh()

        is_changed = self._gui_asset_prx_unit.get_resources_query().do_update()
        if is_changed is True or force is True:
            self._gui_asset_tag_filter_prx_unit.restore()
            self._gui_asset_tag_filter_prx_unit.gui_add_root()

            self._gui_asset_prx_unit.restore()
            self._gui_asset_prx_unit.gui_add_all()

        self._gui_asset_prx_unit.do_gui_refresh_by_dcc_selection()
        self._gui_asset_prx_unit.do_gui_refresh_tools()

        self.do_gui_refresh_toolset_units()

        self._top_prx_tool_bar.do_gui_refresh()

    def do_gui_refresh_toolset_units(self):
        self._gui_skin_proxy_prx_toolset_unit.do_gui_refresh_by_dcc_selection()
