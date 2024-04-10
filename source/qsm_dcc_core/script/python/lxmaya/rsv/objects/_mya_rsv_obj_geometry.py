# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxmaya.dcc.objects as mya_dcc_objects

import lxmaya.fnc.objects as mya_fnc_objects


class UsdCmdBasic(object):
    @classmethod
    def _set_usd_export_(cls, root, location, file_path, start_frame, end_frame):
        # noinspection PyUnresolvedReferences
        import maya.mel as mel

        cmd_str = u'paMaUsdExport "{}" "{}" "{}" {} {}'.format(
            root, location, file_path, start_frame, end_frame
        )
        # args "meshuv, curve, verbose"
        cmd_str += u' {} 1 0 0'
        bsc_log.Log.trace_method_result(
            'usd export',
            u'file="{}", location="{}", frames="{}-{}" is started'.format(
                file_path, location, start_frame, end_frame
            )
        )
        #
        mel.eval(cmd_str)
        #
        bsc_log.Log.trace_method_result(
            'usd export',
            u'file="{}", location="{}", frames="{}-{}" is completed'.format(
                file_path, location, start_frame, end_frame
            )
        )


class RsvDccGeometryHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccGeometryHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def do_export_asset_geometry_usd(self, version_scheme='match'):
        """
        :param version_scheme:
        :return:
        """
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        pathsep = rsv_scene_properties.get('dcc.pathsep')
        #
        if version_scheme == 'match':
            version = self._rsv_scene_properties.get('version')
        elif version_scheme == 'new':
            version = version_scheme
        #
        mya_root_dag_opt = bsc_core.PthNodeOpt(root).translate_to(
            pathsep=pathsep
        )
        dcc_root = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if dcc_root.get_is_exists() is True:
            if workspace == rsv_scene_properties.get('workspaces.release'):
                keyword = 'asset-geometry-usd-payload-file'
            elif workspace == rsv_scene_properties.get('workspaces.temporary'):
                keyword = 'asset-temporary-geometry-usd-payload-file'
            else:
                raise TypeError()

            rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword)
            file_path = rsv_unit.get_result(version=version)

            mya_fnc_objects.FncExporterForGeometryUsdNew(
                option=dict(
                    file=file_path,
                    renderable_locations=[
                        '/master/mod/hi',
                        '/master/mod/lo',
                    ],
                    auxiliary_locations=[
                        '/master/grm',
                        '/master/cfx',
                        '/master/efx',
                        '/master/misc'
                    ],
                )
            ).execute()
        else:
            raise RuntimeError()

    def do_export_asset_geometry_uv_map_usd(self, version_scheme='match'):
        import lxusd.rsv.objects as usd_rsv_objects

        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        step = rsv_scene_properties.get('step')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-geometry-usd-uv_map-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-geometry-usd-uv_map-file'
        else:
            raise TypeError()
        #
        file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=keyword)
        file_path = file_rsv_unit.get_result(version=version)

        usd_rsv_objects.RsvTaskOverrideUsdCreator(
            self._rsv_task
        ).create_geometry_uv_map_at(
            file_path
        )

    def set_asset_geometry_abc_export(self, version_scheme='match'):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        pathsep = rsv_scene_properties.get('dcc.pathsep')
        #
        if version_scheme == 'match':
            version = self._rsv_scene_properties.get('version')
        elif version_scheme == 'new':
            version = version_scheme
        #
        mya_root_dag_opt = bsc_core.PthNodeOpt(root).translate_to(
            pathsep=pathsep
        )
        dcc_root = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if dcc_root.get_is_exists() is True:
            if workspace == rsv_scene_properties.get('workspaces.source'):
                keyword = 'asset-source-geometry-abc-var-file'
            elif workspace == rsv_scene_properties.get('workspaces.release'):
                keyword = 'asset-geometry-abc-var-file'
            elif workspace == rsv_scene_properties.get('workspaces.temporary'):
                keyword = 'asset-temporary-geometry-abc-var-file'
            else:
                raise TypeError()
            # location_names = [i.name for i in dcc_root.get_children()]
            # use white list
            location_names = ['hi', 'shape', 'hair', 'aux']
            with bsc_log.LogProcessContext.create(maximum=len(location_names), label='export geometry in location') as g_p:
                for i_location_name in location_names:
                    g_p.do_update()
                    #
                    i_geometry_abc_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
                        keyword=keyword
                    )
                    i_geometry_usd_abc_file_path = i_geometry_abc_var_file_rsv_unit.get_result(
                        version=version, variants_extend=dict(var=i_location_name)
                    )
                    #
                    i_location = '{}/{}'.format(root, i_location_name)
                    i_sub_root_dag_path = bsc_core.PthNodeOpt(i_location)
                    i_mya_sub_root_dag_path = i_sub_root_dag_path.translate_to(
                        pathsep=pathsep
                    )
                    #
                    sub_root_mya_obj = mya_dcc_objects.Group(i_mya_sub_root_dag_path.path)
                    if sub_root_mya_obj.get_is_exists() is True:
                        mya_fnc_objects.FncExporterForGeometryAbc(
                            file_path=i_geometry_usd_abc_file_path,
                            root=i_location,
                            attribute_prefix=['pg'],
                            option={}
                        ).set_run()
        else:
            raise RuntimeError()


class RsvDccGeometryExtraHookOpt(
    utl_rsv_obj_abstract.AbsRsvObjHookOpt,
    UsdCmdBasic
):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccGeometryExtraHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def do_export_asset_geometry_usd(self, version_scheme='match'):
        """
        :param version_scheme:
        :return:
        """
        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        pathsep = rsv_scene_properties.get('dcc.pathsep')
        #
        if version_scheme == 'match':
            version = self._rsv_scene_properties.get('version')
        elif version_scheme == 'new':
            version = version_scheme
        #
        mya_root_dag_opt = bsc_core.PthNodeOpt(root).translate_to(
            pathsep=pathsep
        )
        dcc_root = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if dcc_root.get_is_exists() is True:
            if workspace == rsv_scene_properties.get('workspaces.source'):
                keyword = 'asset-source-geometry-usd-var-file'
            elif workspace == rsv_scene_properties.get('workspaces.release'):
                keyword = 'asset-geometry-usd-var-file'
            elif workspace == rsv_scene_properties.get('workspaces.temporary'):
                keyword = 'asset-temporary-geometry-usd-var-file'
            else:
                raise TypeError()
            #
            start_frame, end_frame = dcc_root.get('pg_start_frame'), dcc_root.get('pg_end_frame')
            # location_names = [i.name for i in dcc_root.get_children()]
            # use white list
            location_names = ['hi', 'shape', 'hair', 'aux']
            with bsc_log.LogProcessContext.create(
                    maximum=len(location_names), label='export geometry-extra in location'
                    ) as g_p:
                for i_location_name in location_names:
                    g_p.do_update()
                    #
                    if start_frame is not None and end_frame is not None:
                        pass
                    else:
                        pass

    def set_asset_geometry_proxy_usd_export(self):
        pass


class RsvDccShotGeometryHookOpt(
    utl_rsv_obj_abstract.AbsRsvObjHookOpt,
    UsdCmdBasic
):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccShotGeometryHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_shot_geometry_usd_export(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        asset_shot = self._hook_option_opt.get('shot')
        shot_asset = self._hook_option_opt.get('shot_asset')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-shot_asset-geometry-usd-var-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-shot_asset-geometry-usd-var-dir'
        else:
            raise TypeError()

        cache_frames = self._hook_option_opt.get('cache_shot_frames')
        start_frame, end_frame = bsc_core.RawTextOpt(cache_frames).to_frame_range()

        asset_shot_geometry_usd_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )

        asset_shot_geometry_usd_directory_path = asset_shot_geometry_usd_directory_rsv_unit.get_result(
            version=version,
            variants_extend=dict(
                asset_shot=asset_shot,
                shot_asset=shot_asset,
            )
        )
        self._set_shot_geometry_usd_export_(
            shot_asset, asset_shot_geometry_usd_directory_path, start_frame, end_frame
        )

    def set_asset_shot_geometry_abc_export(self):
        pass

    @classmethod
    def _set_shot_geometry_usd_export_(cls, shot_asset, directory_path, start_frame, end_frame):
        location_names = [
            'hi',
            'shape',
            # 'hair',
            'aux',
        ]
        #
        reference_dict = mya_dcc_objects.References().get_reference_dict_()
        if shot_asset in reference_dict:
            namespace, root, obj = reference_dict[shot_asset]
            with bsc_log.LogProcessContext.create_as_bar(maximum=len(location_names), label='usd export') as l_p:
                for i_location_name in location_names:
                    i_location = '{}|{}:{}'.format(root, namespace, i_location_name)
                    if mya_dcc_objects.Node(i_location).get_is_exists() is True:
                        i_file_path = '{}/{}.usd'.format(directory_path, i_location_name)
                        cls._set_usd_export_(
                            root, i_location, i_file_path, start_frame, end_frame
                        )
                    l_p.do_update()
        else:
            raise RuntimeError(
                bsc_log.Log.trace_method_error(
                    'usd export',
                    'namespace="{}" is non-exists'.format(shot_asset)
                )
            )


class RsvDccShotHairHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccShotHairHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_shot_xgen_export(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        asset_shot = self._hook_option_opt.get('shot')
        shot_asset = self._hook_option_opt.get('shot_asset')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-shot_asset-component-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-shot_asset-component-dir'
        else:
            raise TypeError()
        #
        cache_frames = self._hook_option_opt.get('cache_shot_frames')
        start_frame, end_frame = bsc_core.RawTextOpt(cache_frames).to_frame_range()
        #
        component_usd_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        component_usd_directory_path = component_usd_directory_rsv_unit.get_result(
            version=version,
            variants_extend=dict(
                asset_shot=asset_shot,
                shot_asset=shot_asset,
            )
        )
        self._set_shot_xgen_export_(
            shot_asset, component_usd_directory_path, start_frame, end_frame
        )

    @classmethod
    def _set_xgen_export_(cls, root, directory_path, start_frame, end_frame):
        # noinspection PyUnresolvedReferences
        from pgmaya import exporters

        with bsc_log.LogContext.create(
                'xgen export',
                'directory="{}", root="{}", frames="{}-{}"'.format(
                    directory_path, root, start_frame, end_frame
                )
        ):
            e = exporters.AniGrmExporter()
            args = dict(
                master=root,
                cacheDir=directory_path,
                start_frame=start_frame,
                end_frame=end_frame
            )
            e.run(args)

    @classmethod
    def _set_shot_xgen_export_(cls, shot_asset, directory_path, start_frame, end_frame):
        reference_dict = mya_dcc_objects.References().get_reference_dict_()
        if shot_asset in reference_dict:
            namespace, root, obj = reference_dict[shot_asset]
            cls._set_xgen_export_(root, directory_path, start_frame, end_frame)
        else:
            raise RuntimeError(
                bsc_log.Log.trace_method_error(
                    'usd export',
                    'namespace="{}" is non-exists'.format(shot_asset)
                )
            )
