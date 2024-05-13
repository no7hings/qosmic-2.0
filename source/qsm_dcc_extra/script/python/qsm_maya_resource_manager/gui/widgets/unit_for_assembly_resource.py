# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import lxgui.proxy.widgets as prx_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import qsm_general.scan as qsm_gnl_scan

import qsm_maya.core as qsm_mya_core

import qsm_maya.asset.core as qsm_mya_ast_core

import qsm_maya.scenery.core as qsm_mya_scn_core

import qsm_maya.motion as qsm_mya_motion

import qsm_gui.proxy.widgets as qsm_prx_widgets

from ... import core as _rsc_mng_core


class _GuiResourceOpt(
    _rsc_mng_core.GuiResourceOpt
):
    ROOT_NAME = 'Sceneries'

    NAMESPACE = 'assembly'

    RESOURCES_QUERY_CLS = qsm_mya_scn_core.SceneriesQuery

    RESOURCE_SCHEME = 'assembly'

    def __init__(self, window, unit, session, prx_tree_view):
        super(_GuiResourceOpt, self).__init__(window, unit, session, prx_tree_view)


class PrxUnitForAssemblyResource(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = qt_widgets.QtTranslucentWidget

    SCRIPT_JOB_NAME = 'resource_manager_for_assembly'

    def _gui_filter_update_visible(self, boolean):
        self._prx_h_splitter.swap_contract_left_or_top_at(0)

    def _gui_add_main_tools(self):
        for i in [
            ('filter', 'tool/filter', '...', self._gui_filter_update_visible)
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
            self._gui_resource_opt.do_gui_select_resources,
            self._script_job.EventTypes.SelectionChanged
        )
        self._script_job.register(
            self.do_gui_refresh_all,
            self._script_job.EventTypes.SceneOpened
        )

    def _destroy_all_script_jobs(self):
        self._script_job.destroy()

    def do_gui_refresh_by_window_active_changing(self):
        self._gui_resource_opt.do_gui_refresh_tools()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxUnitForAssemblyResource, self).__init__(*args, **kwargs)
        self._window = window
        self._session = session

        self.gui_setup_unit()

    def gui_setup_unit(self):
        self._qt_widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        qt_lot = qt_widgets.QtVBoxLayout(self._qt_widget)
        qt_lot.setContentsMargins(*[0]*4)
        qt_lot.setSpacing(2)

        self._top_prx_tool_bar = prx_widgets.PrxHToolBar()
        qt_lot.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)
        # main tool
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )
        self._gui_add_main_tools()

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
        self._gui_resource_opt = _GuiResourceOpt(
            self._window, self, self._session, self._resource_prx_tree_view
        )
        # tool tab
        self._prx_tab_group = prx_widgets.PrxHTabGroup()
        qt_lot.addWidget(self._prx_tab_group.widget)
        # utility
        self._utility_options_node = prx_widgets.PrxNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.options.assembly_utility')
            )
        )
        self._utility_options_node.create_ports_by_data(
            self._session.configure.get('build.options.assembly_utility.parameters'),
        )
        self._prx_tab_group.add_widget(
            self._utility_options_node,
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.tag-groups.assembly_utility')
            ),
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._session.configure.get('build.tag-groups.assembly_utility')
            )
        )

        self._register_all_script_jobs()

        self._window.connect_window_activate_changed_to(self.do_gui_refresh_by_window_active_changing)
        self._window.connect_window_close_to(self._destroy_all_script_jobs)

    def do_gui_refresh_all(self):
        self._top_prx_tool_bar.do_gui_refresh()

        self._gui_resource_tag_opt.restore()
        self._gui_resource_tag_opt.gui_add_root()

        self._gui_resource_opt.restore()
        self._gui_resource_opt.gui_add_all()

    def do_gui_refresh_all_auto(self):
        self._top_prx_tool_bar.do_gui_refresh()
        is_changed = self._gui_resource_opt.get_resources_query().do_update()
        if is_changed is True:
            self._gui_resource_tag_opt.restore()
            self._gui_resource_tag_opt.gui_add_root()

            self._gui_resource_opt.restore()
            self._gui_resource_opt.gui_add_all()

    def do_dcc_load_unit_assemblies_by_selection(self):
        pass
