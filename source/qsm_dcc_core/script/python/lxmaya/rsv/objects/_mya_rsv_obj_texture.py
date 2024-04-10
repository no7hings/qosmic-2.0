# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccTextureHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccTextureHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def do_export_asset_render_texture(self):
        import lxbasic.storage as bsc_storage

        import lxmaya.fnc.objects as mya_fnc_objects

        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-texture-base-dir'
            keyword_1 = 'asset-texture-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-texture-base-dir'
            keyword_1 = 'asset-temporary-texture-dir'
        else:
            raise RuntimeError()
        #
        texture_base_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        texture_base_directory = texture_base_directory_rsv_unit.get_result(
            version=version
        )
        bsc_storage.StgPathPermissionMtd.create_directory(texture_base_directory)
        #
        texture_directory_tgt_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        texture_directory_path = texture_directory_tgt_unit.get_result(
            version=version
        )
        bsc_storage.StgPathPermissionMtd.create_directory(texture_directory_path)
        #
        mya_fnc_objects.FncExporterForRenderTexture(
            option=dict(
                directory_base=texture_base_directory,
                directory=texture_directory_path,
                #
                location=root,
                #
                fix_name_blank=True,
                with_reference=False,
                #
                use_environ_map=True,
                #
                copy_source=True,
            )
        ).execute()

    def execute_preview_texture_export(self):
        import lxbasic.storage as bsc_storage

        import lxmaya.fnc.objects as mya_fnc_objects

        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-texture-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-texture-dir'
        else:
            raise RuntimeError()
        #
        texture_directory_tgt_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        texture_directory_path = texture_directory_tgt_unit.get_result(
            version=version
        )
        bsc_storage.StgPathPermissionMtd.create_directory(texture_directory_path)

        mya_fnc_objects.FncGeneralTextureExporter(
            option=dict(
                directory=texture_directory_path,
                location='/master',
                fix_name_blank=True,
                copy_source=True,
            )
        ).execute()
