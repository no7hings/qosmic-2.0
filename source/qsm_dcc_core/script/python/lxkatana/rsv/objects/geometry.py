# coding:utf-8
import lxbasic.log as bsc_log

from lxutil.rsv import utl_rsv_obj_abstract


# noinspection PyUnusedLocal
class RsvDccGeometryHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccGeometryHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def do_export_asset_geometry_usd(self):
        import lxkatana.core as ktn_core

        import lxkatana.dcc.operators as ktn_dcc_operators

        w_s = ktn_core.WorkspaceSetting()
        opt = w_s.get_current_look_output_opt_force()
        if opt is None:
            return

        s = ktn_dcc_operators.LookOutputOpt(opt)

        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')

        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-cache-usd-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-cache-usd-dir'
        else:
            raise TypeError()

        directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        directory_path = directory_rsv_unit.get_result(
            version=version
        )

        file_path = s.get_geometry_uv_map_usd_source_file()
        if file_path:
            import lxusd.core as usd_core

            usd_core.UsdBasic.copy_with_references_fnc(
                file_path,
                directory_path,
                replace=True
            )
        else:
            bsc_log.Log.trace_method_error(
                'usd export',
                'file="{}" is non-exists'.format(file_path)
            )

    def do_export_asset_geometry_uv_map_usd(self):
        import lxkatana.core as ktn_core

        import lxkatana.dcc.operators as ktn_dcc_operators

        w_s = ktn_core.WorkspaceSetting()
        opt = w_s.get_current_look_output_opt_force()
        if opt is None:
            return

        s = ktn_dcc_operators.LookOutputOpt(opt)

        rsv_scene_properties = self._rsv_scene_properties

        step = rsv_scene_properties.get('step')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')

        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-cache-usd-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-cache-usd-dir'
        else:
            raise TypeError()

        directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        directory_path = directory_rsv_unit.get_result(
            version=version
        )
        file_path = s.get_geometry_uv_map_usd_file()
        if file_path:
            import lxusd.core as usd_core
            usd_core.UsdBasic.copy_with_references_fnc(
                file_path,
                directory_path,
                replace=True
            )
        else:
            bsc_log.Log.trace_method_error(
                'usd export',
                'file="{}" is non-exists'.format(file_path)
            )
