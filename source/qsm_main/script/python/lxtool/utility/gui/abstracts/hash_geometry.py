# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets


class AbsPnlForHashGeometryDcc(
    prx_widgets.PrxSessionWindow
):
    CONFIGURE_FILE_PATH = 'utility/panel/database-geometry-manager'

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlForHashGeometryDcc, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._set_panel_build_()

    def _set_panel_build_(self):
        self._set_utility_group_build_()
        self._set_database_export_group_build_()
        self._set_database_import_group_build_()
        self._set_hash_uv_group_build_()

    def _set_utility_group_build_(self):
        expand_box_0 = prx_widgets.PrxHToolGroup()
        expand_box_0.set_name('Utility')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.add_widget(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.add_widget(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._utility_node_prx = prx_widgets.PrxNodeOld()
        qt_layout_0.addWidget(self._utility_node_prx.widget)
        #
        _port = self._utility_node_prx.add_port(
            prx_widgets.PrxPortAsFileSave('save_usd_file', 'Save USD-file')
        )
        _port.set_ext_filter('All USD File (*.usd *.usda)')
        _port.set_tool_tip(
            [
                'choose / enter a usd "file-path"'
            ]
        )
        #
        _port = self._utility_node_prx.add_port(
            prx_widgets.PrxPortAsButton('export_select_to_usd_file', 'Export Select(s) to USD-file')
        )
        _port.set_tool_tip(
            [
                'press to export select(s) to usd "Save USD-file"'
            ]
        )
        _port.set(self._set_usd_file_export_)
        #
        _port = self._utility_node_prx.add_port(
            prx_widgets.PrxPortAsFileOpen('open_usd_file', 'Open USD-file')
        )
        _port.set_ext_filter('All USD File (*.usd *.usda)')
        _port.set_tool_tip(
            [
                'choose / enter a usd "file-path"'
            ]
        )
        #
        _port = self._utility_node_prx.add_port(
            prx_widgets.PrxPortAsButton('import_from_usd_file', 'Import from USD-file')
        )
        _port.set_tool_tip(
            [
                'press to import geometry from usd "Open USD-file"'
            ]
        )
        _port.set(self._set_usd_file_import_)

    def _set_database_export_group_build_(self):
        expand_box_0 = prx_widgets.PrxHToolGroup()
        expand_box_0.set_name('Database Export')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.add_widget(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.add_widget(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._database_export_node_prx = prx_widgets.PrxNodeOld()
        qt_layout_0.addWidget(self._database_export_node_prx.widget)
        #
        _port = self._database_export_node_prx.add_port(
            prx_widgets.PrxPortAsBoolean('export_uv_map_force', 'Export UV-map(s) Force')
        )
        _port.set_tool_tip(
            [
                'override data in database if is "checked"'
            ]
        )
        _port = self._database_export_node_prx.add_port(
            prx_widgets.PrxPortAsButton(
                'export_uv_map_to_database_from_select', 'Export Database UV-map(s) from Select(s)'
                )
        )
        _port.set_tool_tip(
            [
                '"LMB-click" to export selected mesh(s) to database'
            ]
        )
        _port.set(self._set_database_uv_map_export_)

    def _set_database_import_group_build_(self):
        expand_box_0 = prx_widgets.PrxHToolGroup()
        expand_box_0.set_name('Database Import')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.add_widget(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.add_widget(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._database_import_node_prx = prx_widgets.PrxNodeOld()
        qt_layout_0.addWidget(self._database_import_node_prx.widget)
        #
        _port = self._database_import_node_prx.add_port(
            prx_widgets.PrxPortAsButton('import_database_uv_map_to_select', 'Import Database UV-map(s) to Select(s)')
        )
        _port.set_tool_tip(
            [
                'press to import geometry from database to selected geometry(s)'
            ]
        )
        _port.set(self._set_database_uv_map_import_)

    def _set_hash_uv_group_build_(self):
        expand_box_0 = prx_widgets.PrxHToolGroup()
        expand_box_0.set_name('Database Extend')
        expand_box_0.set_size_mode(1)
        expand_box_0.set_expanded(True)
        self.add_widget(expand_box_0)
        qt_widget_0 = qt_widgets.QtWidget()
        expand_box_0.add_widget(qt_widget_0)
        qt_layout_0 = qt_widgets.QtVBoxLayout(qt_widget_0)
        self._hash_uv_node_prx = prx_widgets.PrxNodeOld()
        qt_layout_0.addWidget(self._hash_uv_node_prx.widget)
        #
        _port = self._hash_uv_node_prx.add_port(
            prx_widgets.PrxSubProcessPort('geometry_unify', 'Unify Geometry by Select(s)')
        )
        _port.set(self._set_geometry_unify_run_)
        _port.set_menu_data(
            [
                ('Stop Deadline-job', None, self._set_geometry_unify_ddl_job_stop_)
            ]
        )
        #
        self._geometry_unify_ddl_job_process = None
        self.connect_window_close_to(self._set_geometry_unify_ddl_job_stop_)
        #
        _port = self._hash_uv_node_prx.add_port(
            prx_widgets.PrxSubProcessPort('geometry_uv_map_assign', 'Assign Geometry UV-map By Select(s)')
        )
        _port.set(self._set_geometry_uv_map_assign_run_)
        _port.set_menu_data(
            [
                ('Stop Deadline-job', None, self._set_geometry_uv_map_assign_ddl_job_stop_)
            ]
        )
        self._geometry_uv_assign_ddl_job_process = None

    def _set_tool_panel_setup_(self):
        self.refresh_all_fnc()

    def refresh_all_fnc(self):
        pass

    def _set_usd_file_export_(self):
        pass

    def _set_usd_file_import_(self):
        pass

    def _set_geometry_unify_run_(self):
        raise NotImplementedError()

    def _set_database_uv_map_export_(self):
        raise NotImplementedError()

    def _set_database_uv_map_import_(self):
        raise NotImplementedError()

    def _set_geometry_unify_ddl_job_stop_(self):
        if self._geometry_unify_ddl_job_process is not None:
            self._geometry_unify_ddl_job_process.set_stop()

    def _set_geometry_unify_ddl_job_processing_(self, running_time_cost):
        raise NotImplementedError()

    def _set_geometry_unify_ddl_job_status_changed_(self, process_status):
        raise NotImplementedError()

    #
    def _set_geometry_uv_map_assign_run_(self):
        raise NotImplementedError()

    #
    def _set_geometry_uv_map_assign_ddl_job_stop_(self):
        if self._geometry_uv_assign_ddl_job_process is not None:
            self._geometry_uv_assign_ddl_job_process.set_stop()

    def _set_geometry_uv_map_assign_ddl_job_processing_(self, running_time_cost):
        raise NotImplementedError()

    def _set_geometry_uv_map_assign_ddl_job_status_changed_(self, process_status):
        raise NotImplementedError()