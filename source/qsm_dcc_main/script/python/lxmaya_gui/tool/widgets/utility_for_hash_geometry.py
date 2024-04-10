# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxtool.utility.gui.abstracts as utl_gui_abstracts

import lxmaya.dcc.objects as mya_dcc_objects


class PnlHashGeometry(utl_gui_abstracts.AbsPnlForHashGeometryDcc):
    def __init__(self, session, *args, **kwargs):
        super(PnlHashGeometry, self).__init__(session, *args, **kwargs)

    def _set_usd_file_export_(self):
        import lxmaya.dcc.objects as maya_dcc_objects

        import lxmaya.fnc.objects as mya_fnc_objects

        file_path = self._utility_node_prx.get_port('save_usd_file').get()
        if file_path:
            root = maya_dcc_objects.Selection.get_current()
            if root:
                mya_fnc_objects.FncExporterForGeometryUsd(
                    option=dict(
                        file=file_path,
                        location=root,
                        #
                        default_prim_path=root,
                        with_mesh_uv=True,
                        with_mesh=True,
                        use_override=False,
                        port_match_patterns=['pg_*']
                    )
                ).execute()

    def _set_usd_file_import_(self):
        import lxmaya.fnc.objects as mya_fnc_objects

        file_path = self._utility_node_prx.get_port('open_usd_file').get()
        if file_path:
            mya_fnc_objects.FncImporterForGeometryUsd(
                option=dict(
                    file=file_path
                )
            ).execute()

    def _set_database_uv_map_export_(self):
        import lxmaya.fnc.objects as mya_fnc_objects

        force = self._database_export_node_prx.get_port('export_uv_map_force').get()
        mya_fnc_objects.FncExporterForDatabaseGeometry(
            option=dict(force=force)
        ).set_run()

    def _set_database_uv_map_import_(self):
        import lxmaya.fnc.objects as mya_fnc_objects

        mya_fnc_objects.FncImporterForDatabaseGeometry().set_run()

    # geometry unify
    def _set_geometry_unify_run_(self):
        if self._geometry_unify_ddl_job_process is not None:
            if self._geometry_unify_ddl_job_process.get_is_stopped():
                self._set_geometry_unify_start_()
            else:
                if self._geometry_unify_ddl_job_process.get_is_completed():
                    self._set_geometry_unify_next_()
        else:
            self._set_geometry_unify_start_()

    def _set_geometry_unify_ddl_job_processing_(self, running_time_cost):
        if self._geometry_unify_ddl_job_process is not None:
            port = self._hash_uv_node_prx.get_port('geometry_unify')
            port.set_name(
                'Unify Geometry by Select(s) [ Running {} ]'.format(
                    bsc_core.RawIntegerMtd.second_to_time_prettify(running_time_cost)
                )
            )

    def _set_geometry_unify_ddl_job_status_changed_(self, status):
        if self._geometry_unify_ddl_job_process is not None:
            port = self._hash_uv_node_prx.get_port('geometry_unify')
            port.set_status(status)
            status = str(status).split('.')[-1]
            port.set_name(
                'Unify Geometry by Select(s) [ {} ]'.format(status)
            )
            mya_dcc_objects.Scene.set_message_show(
                'Unify Geometry by Select(s)',
                status
            )

    def _set_geometry_unify_start_(self):
        raise RuntimeError('this method is removed')

    def _set_geometry_unify_next_(self):
        raise RuntimeError('this method is removed')

    # geometry uv-map assign
    def _set_geometry_uv_map_assign_run_(self):
        if self._geometry_uv_assign_ddl_job_process is not None:
            if self._geometry_uv_assign_ddl_job_process.get_is_stopped():
                self._set_geometry_uv_map_assign_start_()
            else:
                if self._geometry_uv_assign_ddl_job_process.get_is_completed():
                    self._set_geometry_uv_map_assign_next_()
        else:
            self._set_geometry_uv_map_assign_start_()

    def _set_geometry_uv_map_assign_ddl_job_processing_(self, running_time_cost):
        if self._geometry_uv_assign_ddl_job_process is not None:
            port = self._hash_uv_node_prx.get_port('geometry_uv_map_assign')
            port.set_name(
                'Assign Geometry UV-map By Select(s) [ Running {} ]'.format(
                    bsc_core.RawIntegerMtd.second_to_time_prettify(running_time_cost)
                )
            )

    def _set_geometry_uv_map_assign_ddl_job_status_changed_(self, status):
        if self._geometry_uv_assign_ddl_job_process is not None:
            port = self._hash_uv_node_prx.get_port('geometry_uv_map_assign')
            port.set_status(status)
            status = str(status).split('.')[-1]
            port.set_name(
                'Assign Geometry UV-map By Select(s) [ {} ]'.format(status)
            )
            mya_dcc_objects.Scene.set_message_show(
                'Assign Geometry UV-map By Select(s)',
                status
            )

    def _set_geometry_uv_map_assign_start_(self):
        raise RuntimeError('this method is removed')

    def _set_geometry_uv_map_assign_next_(self):
        raise RuntimeError('this method is removed')
