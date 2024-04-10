# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccTextureHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccTextureHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def do_export_asset_render_texture(self):
        import lxbasic.storage as bsc_storage

        import lxkatana.fnc.objects as ktn_fnc_objects

        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')

        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-texture-base-dir'
            keyword_1 = 'asset-texture-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-texture-base-dir'
            keyword_1 = 'asset-temporary-texture-dir'
        else:
            raise TypeError()

        texture_src_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        texture_directory_path_src = texture_src_directory_rsv_unit.get_result(
            version=version
        )
        bsc_storage.StgPathPermissionMtd.create_directory(texture_directory_path_src)

        texture_tgt_directory_tgt_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        texture_directory_path_tgt = texture_tgt_directory_tgt_unit.get_result(
            version=version
        )
        bsc_storage.StgPathPermissionMtd.create_directory(texture_directory_path_tgt)
        # TODO remove orig directory
        ktn_fnc_objects.FncExporterForRenderTexture(
            option=dict(
                directory_base=texture_directory_path_src,
                directory=texture_directory_path_tgt,
                #
                fix_name_blank=True,
                with_reference=False,
                use_environ_map=True,
                #
                copy_source=True,
            )
        ).execute()

    def do_lock_asset_texture_workspace(self):
        import lxutil.rsv.objects as utl_rsv_objects

        import lxkatana.core as ktn_core

        import lxkatana.dcc.objects as ktn_dcc_objects

        import lxkatana.dcc.operators as ktn_dcc_operators

        w_s = ktn_core.WorkspaceSetting()
        opt = w_s.get_current_look_output_opt_force()
        if opt is None:
            return

        s = ktn_dcc_operators.LookOutputOpt(opt)

        location = s.get_geometry_root()

        texture_references = ktn_dcc_objects.TextureReferences()
        dcc_shaders = s.get_all_dcc_geometry_shaders_by_location(location)
        dcc_objs = texture_references.get_objs(
            include_paths=[i.path for i in dcc_shaders]
        )

        texture_workspace_opt = utl_rsv_objects.RsvAssetTextureOpt(
            self._rsv_task
        )
        texture_workspace_opt.set_all_directories_locked(
            dcc_objs
        )
