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

    NAMESPACE = 'scenery'

    RESOURCES_QUERY_CLS = qsm_mya_scn_core.SceneriesQuery

    RESOURCE_SCHEME = 'reference'

    def __init__(self, window, unit, session, prx_tree_view):
        super(_GuiResourceOpt, self).__init__(window, unit, session, prx_tree_view)


class _GuiReferenceOpt(
    _rsc_mng_core.GuiBaseOpt
):
    def __init__(self, window, unit, session, prx_input_for_asset):
        super(_GuiReferenceOpt, self).__init__(window, unit, session)
        self._scan_root = qsm_gnl_scan.Root.generate()
        self._prx_input_for_asset = prx_input_for_asset

        self._count_input = qt_widgets.QtInputAsConstant()
        self._prx_input_for_asset.add_widget(self._count_input)
        self._count_input._set_value_type_(int)
        self._count_input.setMaximumWidth(64)
        self._count_input.setMinimumWidth(64)
        self._count_input._set_value_(1)

        self._reference_button = qt_widgets.QtPressButton()
        self._prx_input_for_asset.add_widget(self._reference_button)
        self._reference_button._set_name_text_(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.buttons.reference')
            )
        )
        self._reference_button._set_tool_tip_text_(
            gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._session.configure.get('build.buttons.reference')
            )
        )
        self._reference_button.setMaximumWidth(64)
        self._reference_button.setMinimumWidth(64)
        self._reference_button.press_clicked.connect(self.do_dcc_reference_resource)
        self._reference_button._set_action_enable_(False)

        self._prx_input_for_asset.connect_input_change_accepted_to(self.do_gui_refresh_resource)

        self._resource_file_path = None

        self.do_gui_refresh_resource(self._prx_input_for_asset.get_path())

    def do_dcc_reference_resource(self):
        if self._resource_file_path is not None:
            file_opt = bsc_storage.StgFileOpt(self._resource_file_path)
            count = self._count_input._get_value_()
            for i in range(count):
                qsm_mya_core.SceneFile.reference_file(
                    self._resource_file_path,
                    namespace=file_opt.name_base
                )
            self._unit.do_gui_refresh_all()

    def do_gui_refresh_resource(self, path):
        self._resource_file_path = None
        self._reference_button._set_action_enable_(False)
        entity = self._prx_input_for_asset.get_entity(path)
        if entity is not None:
            if entity.type == 'Asset':
                task = entity.task(self._scan_root.EntityTasks.Model)
                if task is not None:
                    result = task.find_result(
                        self._scan_root.ResultPatterns.ModelFIle
                    )
                    if result is not None:
                        self._resource_file_path = result
                        self._reference_button._set_action_enable_(True)


class PrxUnitForSceneryResource(prx_abstracts.AbsPrxWidget):
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
            self._gui_resource_opt.do_gui_select_resources,
            self._script_job.EventTypes.SelectionChanged
        )
        self._script_job.register(
            self.do_gui_refresh_by_dcc_frame_changing,
            self._script_job.EventTypes.FrameRangeChanged
        )
        self._script_job.register(
            self.do_gui_refresh_all,
            self._script_job.EventTypes.SceneOpened
        )

    def _destroy_all_script_jobs(self):
        self._script_job.destroy()

    def do_gui_refresh_by_rig_tag_checking(self):
        filter_data_src = self._gui_resource_tag_opt.generate_semantic_tag_filter_data_src()
        qt_view = self._resource_prx_tree_view._qt_view
        qt_view._set_view_semantic_tag_filter_data_src_(filter_data_src)
        qt_view._set_view_keyword_filter_data_src_(
            self._resource_prx_tree_view.filter_bar.get_keywords()
        )
        qt_view._refresh_view_items_visible_by_any_filter_()
        qt_view._refresh_viewport_showable_auto_()

    def do_gui_refresh_by_camera_changing(self):
        cameras = qsm_mya_core.Cameras.get_all()
        active_camera = qsm_mya_core.Camera.get_active()
        self._camera_port.set(
            cameras
        )
        self._camera_port.set(
            active_camera
        )

    def get_frame_scheme(self):
        return self._utility_options_node.get('scene.frame_scheme')

    def do_gui_refresh_by_frame_scheme_changing(self):
        frame_scheme = self.get_frame_scheme()
        if frame_scheme == 'frame_range':
            self._frame_range_port.set_locked(False)
        else:
            self._frame_range_port.set_locked(True)
            self.do_gui_refresh_by_dcc_frame_changing()

    def do_gui_refresh_by_dcc_frame_changing(self):
        frame_scheme = self.get_frame_scheme()
        if frame_scheme == 'time_slider':
            frame_range = qsm_mya_core.Frame.get_frame_range()
            self._frame_range_port.set(frame_range)

    def do_gui_refresh_by_window_active_changing(self):
        self._gui_resource_opt.do_gui_refresh_tools()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxUnitForSceneryResource, self).__init__(*args, **kwargs)
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
        # rig reference
        self._prx_input_for_asset = qsm_prx_widgets.PrxInputForScenery()
        self._reference_tool_box.add_widget(self._prx_input_for_asset)

        self._gui_reference_opt = _GuiReferenceOpt(
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
        self._gui_resource_opt = _GuiResourceOpt(
            self._window, self, self._session, self._resource_prx_tree_view
        )
        self._resource_tag_tree_view.connect_item_check_changed_to(
            self.do_gui_refresh_by_rig_tag_checking
        )
        # tool tab
        self._prx_tab_group = prx_widgets.PrxHTabGroup()
        qt_lot.addWidget(self._prx_tab_group.widget)
        # utility
        self._utility_options_node = prx_widgets.PrxNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.options.scenery_utility')
            )
        )
        self._utility_options_node.create_ports_by_data(
            self._session.configure.get('build.options.scenery_utility.parameters'),
        )

        self._load_unit_assembly_button = self._utility_options_node.get_port('unit_assembly.load')
        self._load_unit_assembly_button.set(self.do_dcc_load_unit_assemblies_by_selection)
        self._load_unit_assembly_button.connect_finished_to(self.load_unit_assemblies)

        self._utility_options_node.get_port('scene.frame_scheme').connect_input_changed_to(
            self.do_gui_refresh_by_frame_scheme_changing
        )
        self._camera_port = self._utility_options_node.get_port('scene.camera')
        self._frame_range_port = self._utility_options_node.get_port('scene.frame_range')
        self._prx_tab_group.add_widget(
            self._utility_options_node,
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.tag-groups.scenery_utility')
            ),
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._session.configure.get('build.tag-groups.scenery_utility')
            )
        )

        self.do_gui_refresh_by_camera_changing()
        self.do_gui_refresh_by_dcc_frame_changing()
        self._gui_resource_opt.do_gui_select_resources()
        
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

    def load_unit_assemblies(self):
        pass

    def do_dcc_load_unit_assemblies_by_selection(self):
        if self._load_unit_assembly_button.get_is_started() is False:
            namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
            if namespaces:
                self._unit_assembly_load_args_array = []
                create_cmds = []
                resources_query = self._gui_resource_opt.get_resources_query()
                valid_namespaces = resources_query.to_valid_namespaces(namespaces)
                if valid_namespaces:
                    with self._window.gui_progressing(
                        maximum=len(valid_namespaces), label='processing skin proxies'
                    ) as g_p:
                        for i_namespace in valid_namespaces:
                            print i_namespace
                            g_p.do_update()
