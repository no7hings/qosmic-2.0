# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccSceneHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccSceneHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def do_create_asset_scene_src(self):
        import lxbasic.storage as bsc_storage

        import lxkatana.dcc.objects as ktn_dcc_objects

        import lxkatana.scripts as ktn_scripts

        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-katana-scene-src-file'
            keyword_1 = 'asset-katana-scene-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-katana-scene-src-file'
            keyword_1 = 'asset-temporary-katana-scene-file'
        else:
            raise TypeError()

        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(
            version=version
        )
        # save file first
        ktn_dcc_objects.Scene.save_to_file(scene_src_file_path)

        ktn_scripts.ScpWorkspaceCreateNew.new()

        ktn_dcc_objects.Scene.save_to_file(scene_src_file_path)
        #
        if self._hook_option_opt.get_as_boolean('with_scene_link') is True:
            scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_1
            )
            scene_file_path = scene_file_rsv_unit.get_result(version=version)
            bsc_storage.StgFileOpt(scene_file_path).create_directory()
            bsc_storage.StgPathLinkMtd.link_file_to(
                scene_src_file_path, scene_file_path
            )

    def do_export_asset_scene(self):
        import lxkatana.dcc.objects as ktn_dcc_objects

        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = '{branch}-katana-scene-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = '{branch}-temporary-katana-scene-file'
        else:
            raise TypeError()
        #
        scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_file_path = scene_file_rsv_unit.get_result(
            version=version
        )
        ktn_dcc_objects.Scene.save_to_file(scene_file_path)
        return scene_file_path

    def get_scene_src_file_path(self):
        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')

        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-katana-scene-src-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-katana-scene-src-file'
        else:
            raise TypeError()

        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(
            version=version
        )
        return scene_src_file_path

    # for render
    def do_create_asset_scene(self):
        import fnmatch

        import lxkatana.core as ktn_core

        import lxkatana.dcc.objects as ktn_dcc_objects

        import lxkatana.fnc.objects as ktn_fnc_objects

        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        step = rsv_scene_properties.get('step')
        task = rsv_scene_properties.get('task')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-katana-scene-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-katana-scene-file'
        else:
            raise TypeError()

        scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_file_path = scene_file_rsv_unit.get_result(version=version)

        render_file_path = scene_file_path
        # save file first
        ktn_dcc_objects.Scene.save_to_file(render_file_path)
        #
        katana_workspace = ktn_dcc_objects.AssetWorkspaceOld()
        # create workspace
        ktn_fnc_objects.FncCreatorForLookWorkspaceOld().set_run()
        #
        look_pass_names = self._hook_option_opt.get('look_passes')
        if 'white_disp' in look_pass_names:
            self.do_create_asset_white_disp()

        if 'white_zbrush' in look_pass_names:
            self.do_create_asset_white_zbrush()
        #
        shot_name = self._hook_option_opt.get('shot')
        if shot_name:
            shot_geometries_node_opt = ktn_core.NGNodeOpt('shot__geometries')
            shot_paths = shot_geometries_node_opt.get_as_enumerate('options.shot')
            _ = fnmatch.filter(shot_paths, '*/{}'.format(shot_name))
            if _:
                shot_geometries_node_opt.set('options.shot', _[0])
            shot_geometries_node_opt.execute_port('usd.create')
        # usd
        geometries = [ktn_dcc_objects.Node(i) for i in ['asset__geometries', 'shot__geometries']]
        usd_version_enable = self._hook_option_opt.get_as_boolean('usd_version_enable')
        usd_version_override_enable = self._hook_option_opt.get_as_boolean('usd_version_override_enable')
        usd_reverse_face_vertex_enable = self._hook_option_opt.get_as_boolean('usd_reverse_face_vertex_enable')
        for i_geometry_dcc_node in geometries:
            if i_geometry_dcc_node.get_is_exists() is True:
                i_geometry_dcc_node.set(
                    'usd.variants.enable', usd_version_enable
                )
                i_geometry_dcc_node.set(
                    'usd.variants.override_enable', usd_version_override_enable
                )
                i_geometry_dcc_node.set(
                    'usd.debuggers.reverse_face_vertex_enable', usd_reverse_face_vertex_enable
                )
        #
        front_camera_scheme = self._hook_option_opt.get('front_camera_scheme')
        # camera
        cameras = self._hook_option_opt.get_as_array('cameras')
        for i_camera in cameras:
            if i_camera == 'front':
                if front_camera_scheme is not None:
                    if front_camera_scheme == 'lineup':
                        # self.set_front_camera()
                        katana_workspace.set_asset_front_camera_fill_to_front()
                    elif front_camera_scheme == 'assess':
                        # self.set_front_camera_for_assess()
                        katana_workspace.set_asset_front_camera_fill_to_rotation()
        #
        light_pass_all = self._hook_option_opt.get('light_pass_all')
        if light_pass_all:
            light_pass_dcc_node = ktn_dcc_objects.Node('all__light')
            if light_pass_dcc_node.get_is_exists() is True:
                light_pass_dcc_node.set('lights.light_rig.name', light_pass_all)
                ktn_core.NGNodeOpt(light_pass_dcc_node.ktn_obj).execute_port(
                    'lights.light_rig.load'
                )
        #
        light_pass_add_1 = self._hook_option_opt.get('light_pass_add_1')
        if light_pass_add_1:
            light_pass_dcc_node = ktn_dcc_objects.Node('light_rig_1__light')
            if light_pass_dcc_node.get_is_exists() is True:
                light_pass_dcc_node.set('lights.light_rig.name', light_pass_add_1)
                ktn_core.NGNodeOpt(light_pass_dcc_node.ktn_obj).execute_port(
                    'lights.light_rig.load'
                )
        #
        light_pass_add_2 = self._hook_option_opt.get('light_pass_add_2')
        if light_pass_add_2:
            light_pass_dcc_node = ktn_dcc_objects.Node('light_rig_2__light')
            if light_pass_dcc_node.get_is_exists() is True:
                light_pass_dcc_node.set('lights.light_rig.name', light_pass_add_2)
                ktn_core.NGNodeOpt(light_pass_dcc_node.ktn_obj).execute_port(
                    'lights.light_rig.load'
                )
        # light
        light_pass_override_enable = self._hook_option_opt.get_as_boolean('light_pass_override_enable')
        if light_pass_override_enable is True:
            light_passes = self._hook_option_opt.get_as_array('light_passes')
            light_pass_override_scheme = self._hook_option_opt.get('light_pass_override_scheme')
            for i_light_pass in light_passes:
                i_light_pass_dcc_node = ktn_dcc_objects.Node('{}__light'.format(i_light_pass))
                if i_light_pass_dcc_node.get_is_exists() is True:
                    i_light_pass_dcc_node.set('options.scheme', light_pass_override_scheme)
        # quality
        render_arnold_aov_enable = self._hook_option_opt.get_as_boolean('render_arnold_aov_enable')
        qualities = self._hook_option_opt.get_as_array('qualities')
        for i_quality in qualities:
            i_quality_dcc_node = ktn_dcc_objects.Node('{}__quality'.format(i_quality))
            if i_quality_dcc_node.get_is_exists() is True:
                i_quality_dcc_node.set('lynxi_variants.arnold.aov_enable', render_arnold_aov_enable)
        # render over
        render_override_enable = self._hook_option_opt.get('render_override_enable')
        if render_override_enable is True:
            render_override_percent = self._hook_option_opt.get('render_override_percent')
            #
            qualities = self._hook_option_opt.get('qualities', as_array=True)
            for i_quality in qualities:
                i_quality_dcc_node = ktn_dcc_objects.Node('{}__quality'.format(i_quality))
                #
                i_quality_dcc_node.set('lynxi_variants.percent', render_override_percent)
        # render arnold over
        render_arnold_override_enable = self._hook_option_opt.get('render_arnold_override_enable')
        if render_arnold_override_enable is True:
            render_arnold_override_aa_sample = self._hook_option_opt.get('render_arnold_override_aa_sample')
            #
            qualities = self._hook_option_opt.get('qualities', as_array=True)
            for i_quality in qualities:
                i_quality_dcc_node = ktn_dcc_objects.Node('{}__quality'.format(i_quality))
                #
                i_quality_dcc_node.set('lynxi_variants.arnold_override_enable', True)
                i_quality_dcc_node.set('lynxi_variants.arnold_override.aa_sample', render_arnold_override_aa_sample)
        # render output directory
        render_settings_node_opt = ktn_core.NGNodeOpt('render_settings')
        render_output_directory_path = self._hook_option_opt.get('render_output_directory')
        if render_output_directory_path is None:
            render_output_directory_path = self.get_asset_katana_render_output_directory()
        #
        render_output_file_path = '{}/main/<camera>.<layer>.<light-pass>.<look-pass>.<quality>/<render-pass>.####.exr'.format(
            render_output_directory_path
        )
        render_settings_node_opt.set(
            'lynxi_settings.render_output', render_output_file_path
        )
        #
        renderer_node_opt = ktn_core.NGNodeOpt('render_outputs')
        #
        variable_keys = [
            'cameras',
            'layers',
            'light_passes',
            'look_passes',
            'qualities',
        ]
        for i_variable_key in variable_keys:
            renderer_node_opt.set(
                'lynxi_variants.{}'.format(i_variable_key),
                ', '.join(self._hook_option_opt.get(i_variable_key, as_array=True))
            )

        renderer_node_opt.execute_port('create')
        #
        ktn_dcc_objects.Scene.save_file()

    def do_link_asset_scene_src_(self):
        import lxbasic.storage as bsc_storage

        import lxbasic.dcc.objects as bsc_dcc_objects

        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-katana-scene-file'
            keyword_1 = 'asset-katana-scene-src-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-katana-scene-file'
            keyword_1 = 'asset-temporary-katana-scene-src-file'
        else:
            raise TypeError()
        #
        scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_file_path = scene_file_rsv_unit.get_result(version=version)
        #
        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(version=version)
        #
        if bsc_storage.StgPathMtd.get_is_exists(scene_src_file_path) is False:
            bsc_dcc_objects.StgFile(
                scene_file_path
            ).link_to(
                scene_src_file_path
            )

    def do_create_asset_white_disp(self):
        import lxkatana.fnc.objects as ktn_fnc_objects

        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')

        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-look-ass-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-look-ass-file'
        else:
            raise TypeError()

        look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword_0)
        look_ass_file_path = look_ass_file_rsv_unit.get_exists_result(version=version)
        if look_ass_file_path:
            ktn_fnc_objects.FncImporterForLookAssOld(
                option=dict(
                    file=look_ass_file_path,
                    auto_white_disp_assign=True,
                    look_pass='white_disp'
                )
            ).set_run()

    def do_create_asset_white_zbrush(self):
        import lxkatana.fnc.objects as ktn_fnc_objects

        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')

        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-look-ass-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-look-ass-file'
        else:
            raise TypeError()

        look_ass_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword_0)
        look_ass_file_path = look_ass_file_rsv_unit.get_exists_result(version=version)
        if look_ass_file_path:
            ktn_fnc_objects.FncImporterForLookAssOld(
                option=dict(
                    file=look_ass_file_path,
                    auto_white_zbrush_assign=True,
                    look_pass='white_zbrush'
                )
            ).set_run()

    def set_front_camera(self):
        import lxbasic.log as bsc_log

        import lxbasic.core as bsc_core

        import lxusd.core as usd_core

        import lxkatana.dcc.objects as ktn_dcc_objects

        #
        s = usd_core.UsdStageOpt()
        geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-geometry-usd-var-file'
        )
        #
        geometry_usd_var_file_path_hi = geometry_usd_var_file_rsv_unit.get_result(
            version='latest',
            variants_extend=dict(var='hi')
        )
        if geometry_usd_var_file_path_hi:
            s.append_sublayer(geometry_usd_var_file_path_hi)
            #
            file_properties = geometry_usd_var_file_rsv_unit.generate_properties_by_result(
                geometry_usd_var_file_path_hi
            )
            version_hi = file_properties.get('version')
            geometry_usd_var_file_path_shape = geometry_usd_var_file_rsv_unit.get_exists_result(
                version=version_hi,
                variants_extend=dict(var='shape')
            )
            if geometry_usd_var_file_path_shape:
                s.append_sublayer(geometry_usd_var_file_path_shape)
            else:
                bsc_log.Log.trace_method_warning(
                    u'front camera setup',
                    u'file="{}" is non-exists'.format(geometry_usd_var_file_path_shape)
                )
        #
        s.do_flatten()
        #
        g = s.compute_geometry_args('/master')
        #
        (x, y, z), (c_x, c_y, c_z), (w, h, d) = g
        #
        w += .1
        h += .2
        c_y += .1
        #
        (t_x, t_y, t_z), (r_x, r_y, r_z), (s_x, s_y, s_z) = bsc_core.CameraMtd.compute_front_transformation(
            geometry_args=((x, y, z), (c_x, c_y, c_z), (w, h, d)),
            angle=1,
        )
        #
        dcc_camera = ktn_dcc_objects.Node('cameras')
        #
        dcc_camera.set('cameras.front.translate', (t_x, t_y, t_z))
        dcc_camera.set('cameras.front.rotate', (r_x, r_y, r_z))
        dcc_camera.set('cameras.front.scale', (s_x, s_y, s_z))
        #
        width, height = int(w*50), int(h*50)
        #
        dcc_camera.set(
            'cameras.front.render_resolution', '{}x{}'.format(width, height)
        )

    def set_front_camera_for_assess(self):
        import lxbasic.log as bsc_log

        import lxbasic.core as bsc_core

        import lxusd.core as usd_core

        import lxkatana.dcc.objects as ktn_dcc_objects

        #
        s = usd_core.UsdStageOpt()
        geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-geometry-usd-var-file'
        )
        # ensure all usd file use same version
        geometry_usd_var_file_path_hi = geometry_usd_var_file_rsv_unit.get_result(
            version='latest',
            variants_extend=dict(var='hi')
        )
        if geometry_usd_var_file_path_hi:
            s.append_sublayer(geometry_usd_var_file_path_hi)
            #
            file_properties = geometry_usd_var_file_rsv_unit.generate_properties_by_result(
                geometry_usd_var_file_path_hi
            )
            version_hi = file_properties.get('version')
            geometry_usd_var_file_path_shape = geometry_usd_var_file_rsv_unit.get_exists_result(
                version=version_hi,
                variants_extend=dict(var='shape')
            )
            if geometry_usd_var_file_path_shape:
                s.append_sublayer(geometry_usd_var_file_path_shape)
            else:
                bsc_log.Log.trace_method_warning(
                    u'front camera setup',
                    u'file="{}" is non-exists'.format(geometry_usd_var_file_path_shape)
                )
        #
        s.do_flatten()
        #
        g = s.compute_geometry_args('/master')
        #
        (x, y, z), (c_x, c_y, c_z), (w, h, d) = g
        #
        w += .1
        h += .2
        c_y += .1
        #
        (t_x, t_y, t_z), (r_x, r_y, r_z), (s_x, s_y, s_z) = bsc_core.CameraMtd.compute_front_transformation(
            geometry_args=((x, y, z), (c_x, c_y, c_z), (w, h, d)),
            angle=1,
            mode=1
        )
        #
        dcc_camera = ktn_dcc_objects.Node('cameras')
        #
        dcc_camera.set('cameras.front.translate', (t_x, t_y, t_z))
        dcc_camera.set('cameras.front.rotate', (r_x, r_y, r_z))
        dcc_camera.set('cameras.front.scale', (s_x, s_y, s_z))
        #
        multipy = 4
        #
        width, height = int(w*50*multipy), int(h*50*multipy)
        #
        p = float(height)/float(width)
        width = max(min(width, 4096), 512)
        height = int(p*width)
        #
        dcc_camera.set(
            'cameras.front.render_resolution', '{}x{}'.format(width, height)
        )

    @staticmethod
    def do_reload_asset_usd():
        import lxkatana.dcc.objects as ktn_dcc_objects

        ktn_dcc_objects.AssetWorkspaceOld().set_set_usd_reload()
