# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.dcc.core as bsc_dcc_core

import lxgui.core as gui_core

import lxgui.proxy.widgets as prx_widgets

import lxgui.proxy.scripts as gui_prx_scripts

import lxresolver.core as rsv_core


class AbsPnlComparerForAssetGeometryDcc(prx_widgets.PrxSessionWindow):
    PANEL_KEY = 'asset_comparer'
    #
    DCC_NODE_CLS = None
    #
    FNC_COMPARER_FOR_DCC_GEOMETRY = None
    #
    DESCRIPTION_INDEX = 2
    #
    DCC_SELECTION_CLS = None
    #
    USD_NAMESPACE = 'usd'
    #
    DCC_NAMESPACE = None
    DCC_PATHSEP = None
    #
    RSV_KEYWORD = 'asset-geometry-usd-payload-file'
    #
    DCC_LOCATION = None
    DCC_LOCATION_SOURCE = None
    #
    DCC_LOCATION_FOR_GEOMETRY = None

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlComparerForAssetGeometryDcc, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._set_panel_build_()
        self.post_setup_fnc()
        #
        self.refresh_all_fnc()

    def post_setup_fnc(self):
        pass

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()
        self._set_configure_groups_build_()
        #
        self._update_geometry_from_model_item = prx_widgets.PrxPressItem()
        self._update_geometry_from_model_item.set_name('update geometry from source')
        self._update_geometry_from_model_item.set_icon_name('application/python')
        self._update_geometry_from_model_item.set_tool_tip(
            [
                'press to update geometry(s) form model task'
            ]
        )
        self.add_button(self._update_geometry_from_model_item)
        self._update_geometry_from_model_item.connect_press_clicked_to(self.import_fnc)

    def _set_viewer_groups_build_(self):
        expand_box_0 = prx_widgets.PrxHToolGroup()
        expand_box_0.set_name('Viewer(s)')
        expand_box_0.set_expanded(True)
        self.add_widget(expand_box_0)
        h_splitter_0 = prx_widgets.PrxHSplitter()
        v_splitter_0 = prx_widgets.PrxVSplitter()
        h_splitter_0.add_widget(v_splitter_0)
        expand_box_0.add_widget(h_splitter_0)
        self._filter_tree_viewer_0 = prx_widgets.PrxTreeView()
        v_splitter_0.add_widget(self._filter_tree_viewer_0)
        self._sector_chart = prx_widgets.PrxSectorChart()
        v_splitter_0.add_widget(self._sector_chart)
        #
        self._obj_tree_viewer_0 = prx_widgets.PrxTreeView()
        h_splitter_0.add_widget(self._obj_tree_viewer_0)
        h_splitter_0.set_stretches([1, 2])
        #
        self._set_tree_viewer_build_()

    def _set_tree_viewer_build_(self):
        self._filter_tree_viewer_0.set_header_view_create(
            [('name', 3), ('count', 1)],
            self.get_definition_window_size()[0]*(1.0/3.0)-24
        )
        #
        self._obj_tree_viewer_0.set_header_view_create(
            [('name', 4), ('type', 2), ('status', 2)],
            self.get_definition_window_size()[0]*(2.0/3.0)-24
        )
        #
        self._prx_usd_mesh_tree_view_add_opt = gui_prx_scripts.GuiPrxScpForUsdTreeAdd(
            prx_tree_view=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxDccObjTreeItem,
            dcc_namespace=self.DCC_NAMESPACE,
            dcc_pathsep=self.DCC_PATHSEP,
            dcc_node_class=self.DCC_NODE_CLS,
            dcc_geometry_location=self.DCC_LOCATION_FOR_GEOMETRY,
        )
        #
        self._prx_dcc_obj_tree_view_selection_opt = gui_prx_scripts.GuiPrxScpForTreeSelection(
            prx_tree_view=self._obj_tree_viewer_0,
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE,
            dcc_geometry_location=self.DCC_LOCATION_FOR_GEOMETRY,
            dcc_pathsep=self.DCC_PATHSEP
        )
        self._obj_tree_viewer_0.connect_item_select_changed_to(
            self._prx_dcc_obj_tree_view_selection_opt.set_select
        )
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt = gui_prx_scripts.GuiPrxScpForTreeTagFilter(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._obj_tree_viewer_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

    def _set_configure_groups_build_(self):
        self._options_prx_node = prx_widgets.PrxNode(
            'options'
        )
        self.add_widget(self._options_prx_node)
        self._options_prx_node.set_expanded(False)
        #
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )
        self._options_prx_node.set(
            'refresh', self.refresh_gui_fnc
        )

    def _set_tool_panel_setup_(self):
        self.refresh_all_fnc()

    def _set_comparer_result_update_(self):
        scene_file_path = self._options_prx_node.get('scene.file')
        self._fnc_dcc_geometry_comparer = self.FNC_COMPARER_FOR_DCC_GEOMETRY(
            option=dict(
                file=scene_file_path,
                location=self.DCC_LOCATION,
                location_source=self.DCC_LOCATION_SOURCE
            )
        )
        #
        self._fnc_dcc_geometry_comparer.set_source_file(
            self._options_prx_node.get('usd.source_file')
        )
        #
        return self._fnc_dcc_geometry_comparer.generate_results()

    def _set_dcc_obj_guis_build_(self):
        self._prx_usd_mesh_tree_view_add_opt.restore_all()
        self._prx_dcc_obj_tree_view_tag_filter_opt.restore_all()
        #
        comparer_results = self._set_comparer_result_update_()
        #
        sector_chart_data_dict = {}
        count = len(comparer_results)
        if comparer_results:
            with bsc_log.LogProcessContext.create(maximum=count, label='gui-add for geometry-comparer result') as g_p:
                for i_src_geometry_path, i_tgt_geometry_path, i_check_statuses in comparer_results:
                    g_p.do_update()
                    #
                    i_check_statuses_list = i_check_statuses.split('+')
                    for j_check_status in i_check_statuses_list:
                        sector_chart_data_dict.setdefault(
                            j_check_status, []
                        ).append(
                            i_src_geometry_path
                        )
                    i_dcc_geometry = self._fnc_dcc_geometry_comparer.get_geometry_src(i_src_geometry_path)
                    if i_dcc_geometry is None:
                        i_dcc_geometry = self._fnc_dcc_geometry_comparer.get_geometry_tgt(i_src_geometry_path)
                        #
                    if i_dcc_geometry.type_name in ['Mesh', 'mesh']:
                        i_mesh_prx_item_src = self._prx_usd_mesh_tree_view_add_opt.gui_add_as(
                            i_dcc_geometry, mode='list'
                        )
                        #
                        key = 'from-model'
                        if i_check_statuses == bsc_dcc_core.DccMeshCheckStatus.NonChanged:
                            i_mesh_prx_item_src.set_adopt_state()
                        else:
                            if i_tgt_geometry_path is not None:
                                i_mesh_prx_item_src.set_warning_state()
                            else:
                                i_mesh_prx_item_src.set_error_state()
                        #
                        tag_filter_key = '{}.{}'.format(key, i_check_statuses)
                        #
                        self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                            tag_filter_key, i_mesh_prx_item_src
                        )
                        #
                        i_mesh_prx_item_src.set_gui_attribute(
                            'src_mesh_dcc_path', i_src_geometry_path
                        )
                        i_mesh_prx_item_src.set_gui_attribute(
                            'tgt_mesh_dcc_path', i_tgt_geometry_path
                        )
                        i_mesh_prx_item_src.set_gui_attribute(
                            'check_statuses', i_check_statuses
                        )
                        #
                        i_mesh_prx_item_src.set_name(i_check_statuses, self.DESCRIPTION_INDEX)
                        if i_tgt_geometry_path is not None:
                            i_mesh_prx_item_src.set_tool_tip(i_tgt_geometry_path, self.DESCRIPTION_INDEX)
        #
        sector_chart_data = []
        for i_check_status in bsc_dcc_core.DccMeshCheckStatus.All:
            if i_check_status != bsc_dcc_core.DccMeshCheckStatus.NonChanged:
                if i_check_status in sector_chart_data_dict:
                    sector_chart_data.append(
                        (i_check_status, count, len(sector_chart_data_dict[i_check_status]))
                    )
                else:
                    sector_chart_data.append(
                        (i_check_status, count, 0)
                    )
        #
        self._sector_chart.set_chart_data(
            sector_chart_data,
            gui_core.GuiSectorChartMode.Error
        )

    def refresh_all_fnc(self):
        self._resolver = rsv_core.RsvBase.generate_root()
        scene_file_path = self._options_prx_node.get('scene.file')
        self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
            file_path=scene_file_path
        )
        if self._rsv_scene_properties is not None:
            step = self._rsv_scene_properties.get('step')
            if step in ['mod', 'srf', 'rig', 'grm']:
                keyword = self.RSV_KEYWORD
                rsv_resource = self._resolver.get_rsv_resource(
                    **self._rsv_scene_properties.get_value()
                )
                rsv_model_task = rsv_resource.get_rsv_task(
                    step='mod', task='modeling'
                )
                if rsv_model_task is not None:
                    rsv_unit = rsv_model_task.get_rsv_unit(
                        keyword=keyword
                    )
                    results = rsv_unit.get_result(version='all')
                    if results:
                        self._options_prx_node.set(
                            'usd.source_file', results
                        )
                        self._options_prx_node.set(
                            'usd.source_file', results[-1]
                        )
            #
            self.refresh_gui_fnc()

    #
    def refresh_gui_fnc(self):
        self._set_dcc_obj_guis_build_()
        #
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def _get_checked_geometry_objs_(self):
        lis = []
        for i_item_prx in self._obj_tree_viewer_0.get_all_items():
            if i_item_prx.get_is_checked() is True:
                i_dcc_obj = i_item_prx.get_gui_dcc_obj(namespace=self.USD_NAMESPACE)
                if i_dcc_obj is not None:
                    lis.append((i_item_prx, i_dcc_obj))
        return lis

    def import_fnc(self):
        checked_src_geometries = self._get_checked_geometry_objs_()
        if checked_src_geometries:
            with bsc_log.LogProcessContext.create(maximum=len(checked_src_geometries), label='import geometry') as g_p:
                for i_src_geometry_item_prx, i_src_dcc_geometry in checked_src_geometries:
                    g_p.do_update()
                    if i_src_dcc_geometry.type_name in ['Mesh', 'mesh']:
                        i_tgt_dcc_mesh_path = i_src_geometry_item_prx.get_gui_attribute('tgt_mesh_dcc_path')
                        if i_tgt_dcc_mesh_path is not None:
                            i_check_statuses = i_src_geometry_item_prx.get_gui_attribute('check_statuses')
                            i_src_mesh_dcc_path = i_src_dcc_geometry.path
                            self._fnc_dcc_geometry_comparer.do_repair_mesh(
                                i_src_mesh_dcc_path, i_tgt_dcc_mesh_path, i_check_statuses
                            )
        #
        self.refresh_gui_fnc()

    @classmethod
    def get_location(cls):
        if cls.DCC_LOCATION_SOURCE is not None:
            return cls.DCC_LOCATION_SOURCE
        return cls.DCC_LOCATION

    def _set_path_exchanged_repair_(self, i_tgt_mesh, i_tgt_data):
        pass

    def _set_checked_look_import_from_surface_(self):
        pass
