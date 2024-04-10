# coding:utf-8
import lxbasic.log as bsc_log

from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccLookHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccLookHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def do_export_asset_look_ass(self, force=False, texture_use_environ_map=True):
        import lxbasic.dcc.objects as bsc_dcc_objects

        import lxkatana.core as ktn_core

        import lxkatana.dcc.operators as ktn_dcc_operators

        import lxkatana.fnc.objects as ktn_fnc_objects

        w_s = ktn_core.WorkspaceSetting()
        opt = w_s.get_current_look_output_opt_force()
        if opt is None:
            return

        s = ktn_dcc_operators.LookOutputOpt(opt)

        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')

        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-look-ass-file'
            keyword_1 = 'asset-look-ass-sub-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-look-ass-file'
            keyword_1 = 'asset-temporary-look-ass-sub-file'
        else:
            raise TypeError()

        look_pass_names = s.get_all_look_pass_names()

        for i_look_pass_name in look_pass_names:
            if i_look_pass_name == 'default':
                i_look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword_0)
                i_look_ass_file_path = i_look_ass_file_rsv_unit.get_result(version=version)
            else:
                i_look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword_1)
                i_look_ass_file_path = i_look_ass_file_rsv_unit.get_result(
                    version=version, variants_extend=dict(look_pass=i_look_pass_name)
                )
            #
            i_look_ass_file = bsc_dcc_objects.StgFile(i_look_ass_file_path)
            if i_look_ass_file.get_is_exists() is False or force is True:
                i_look_pass_source_node = s.get_look_pass_source_node(i_look_pass_name)
                if i_look_pass_source_node is not None:
                    ktn_fnc_objects.FncExporterForLookAss(
                        option=dict(
                            file=i_look_ass_file_path,
                            location=root,
                            #
                            look_pass_node=opt.get_path(),
                            look_pass=i_look_pass_name,
                            #
                            texture_use_environ_map=texture_use_environ_map
                        )
                    ).set_run()
            else:
                bsc_log.Log.trace_method_warning(
                    'look-ass export',
                    u'file="{}" is exists'.format(i_look_ass_file_path)
                )

        model_act_cmp_usd_file_path = self.get_asset_model_act_cmp_usd_file()
        if model_act_cmp_usd_file_path is not None:
            dynamic_override_uv_maps = self._hook_option_opt.get_as_boolean('with_look_ass_dynamic_override_uv_maps')
            s.export_ass_auto(
                dynamic_override_uv_maps=dynamic_override_uv_maps
            )

    def do_export_asset_look_klf(self):
        import lxkatana.dcc.objects as ktn_dcc_objects

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
            keyword_0 = 'asset-look-klf-file'
            keyword_1 = 'asset-look-klf-extra-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-look-klf-file'
            keyword_1 = 'asset-temporary-look-klf-extra-file'
        else:
            raise TypeError()

        look_klf_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        look_klf_file_path = look_klf_file_rsv_unit.get_result(
            version=version
        )

        asset_geometries = ktn_dcc_objects.Node('asset__geometries')
        if asset_geometries.get_is_exists() is True:
            asset_geometries.get_port('lynxi_variants.look').set('asset-work')

        s.export_klf(look_klf_file_path)
        # extra
        look_json_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        look_json_file_path = look_json_file_rsv_unit.get_result(
            version=version
        )
        s.export_klf_extra(
            look_json_file_path
        )
