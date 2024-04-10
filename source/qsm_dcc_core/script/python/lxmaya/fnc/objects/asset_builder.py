# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.fnc.abstracts as bsc_fnc_abstracts
# maya
from ...core.wrap import *

from ... import core as mya_core
# maya dcc
from ...dcc import objects as mya_dcc_objects

from ...dcc import operators as mya_dcc_operators


class GeometryAlembicBlender(object):
    def __init__(self, src_root, tgt_root):
        self._src_root = bsc_core.PthNodeOpt(src_root).translate_to('|').to_string()
        self._tgt_root = bsc_core.PthNodeOpt(tgt_root).translate_to('|').to_string()

    def __set_meshes_blend_(self):
        self._set_meshes_connect_(
            self._get_mesh_dic_(mya_dcc_objects.Group(self._src_root).get_all_shape_paths(include_obj_type='mesh')),
            self._get_mesh_dic_(mya_dcc_objects.Group(self._tgt_root).get_all_shape_paths(include_obj_type='mesh'))
        )
        _ = '|'.join(self._src_root.split('|')[:2])
        if cmds.objExists(
                _
        ) is True:
            cmds.delete(_)

    @classmethod
    def _get_mesh_dic_(cls, mesh_paths):
        dic = {}
        for i_mesh_path in mesh_paths:
            mesh_opt = mya_dcc_operators.MeshOpt(mya_dcc_objects.Node(i_mesh_path))
            face_vertices_as_uuid = mesh_opt.get_face_vertices_as_uuid()
            dic.setdefault(
                face_vertices_as_uuid, []
            ).append(i_mesh_path)
        return dic

    @classmethod
    def _set_meshes_connect_(cls, src_dic, tgt_dic):
        for seq, (i_uuid, i_paths_src) in enumerate(src_dic.items()):
            i_path_src = i_paths_src[0]
            if i_uuid in tgt_dic:
                i_paths_tgt = tgt_dic[i_uuid]
                i_path_tgt = i_paths_tgt[0]
                cls._set_mesh_shape_blend_(seq, i_path_src, i_path_tgt)
                bsc_log.Log.trace_method_result(
                    'mesh connect',
                    'obj="{}"'.format(i_path_src)
                )
            else:
                bsc_log.Log.trace_method_warning(
                    'mesh connect',
                    'obj="{}" is non-matched founded'.format(i_path_src)
                )

    @classmethod
    def _set_blend_histories_clear_(cls, obj_path):
        _ = cmds.listConnections(obj_path, destination=0, source=1, type='tweak') or []
        [cmds.delete(i) for i in _ if cmds.objExists(i)]

    @classmethod
    def _set_shape_parent_(cls, src_shape_path, tgt_shape_path, blend_path):
        if cmds.objExists(src_shape_path) and cmds.objExists(tgt_shape_path):
            src_transform_path = cmds.listRelatives(src_shape_path, parent=1, fullPath=1)[0]
            tgt_transform_path = cmds.listRelatives(tgt_shape_path, parent=1, fullPath=1)[0]
            if src_transform_path != tgt_transform_path:
                tgt_shape_name = tgt_shape_path.split('|')[-1]
                new_shape_name = '{}_source'.format(tgt_shape_name)
                new_src_shape_path = '{}|{}'.format(src_transform_path, new_shape_name)
                #
                new_tgt_shape_path = '{}|{}'.format(tgt_transform_path, new_shape_name)
                cmds.rename(
                    src_shape_path, new_shape_name
                )
                cmds.parent(new_src_shape_path, tgt_transform_path, shape=1, add=1)
                cmds.setAttr('{}.intermediateObject'.format(new_tgt_shape_path), 1)
                cmds.delete(src_transform_path)
                cmds.connectAttr(
                    '{}.worldMesh[0]'.format(new_tgt_shape_path),
                    '{}.inputTarget[0].inputTargetGroup[0].inputTargetItem[6000].inputGeomTarget'.format(blend_path)
                )

    @classmethod
    def _set_mesh_shape_blend_(cls, seq, src_mesh_path, tgt_mesh_path):
        tgt_shape_name = src_mesh_path.split('|')[-1]
        bs = cmds.blendShape(
            src_mesh_path, tgt_mesh_path,
            name='{}_blend'.format(tgt_shape_name).format(seq),
            weight=(0, 1),
            origin='world',
            before=1
        )
        #
        if bs:
            cls._set_shape_parent_(
                src_mesh_path, tgt_mesh_path, bs[0]
            )
            # for i_b in bs:
            #     cls._set_blend_histories_clear_(i_b)

    def set_run(self):
        self.__set_meshes_blend_()


# noinspection PyUnusedLocal
class FncBuilderForAssetOld(bsc_fnc_abstracts.AbsFncOptionBase):
    KEY = 'asset build'
    VAR_NAMES = ['hi', 'shape']
    #
    OPTION = dict(
        project='',
        asset='',
        #
        geometry_option='step=mod&task=modeling',
        look_option='step=srf&task=surfacing',
        #
        with_model_geometry=False,
        with_model_act_geometry_dyn=False,
        with_model_act_geometry_dyn_connect=False,
        model_act_properties=[],
        #
        with_surface_cfx_geometry=False,
        #
        with_groom_geometry=False,
        with_groom_grow_geometry=False,
        #
        with_surface_geometry_uv_map=False,
        with_surface_work_geometry_uv_map=False,
        uv_map_face_vertices_contrast=False,
        #
        with_surface_look=False,
        with_surface_work_look=False,
        with_surface_cfx_look=False,
        #
        with_surface_look_preview=False,
        with_surface_work_look_preview=False,
        #
        save_scene=False,
        #
        with_camera=False,
        with_light=False,
        #
        geometry_var_names=VAR_NAMES,
        #
        render_resolution=[2048, 2048]
    )

    def __init__(self, option=None):
        super(FncBuilderForAssetOld, self).__init__(option)

    @classmethod
    def _build_geometry_from_usd_(cls, rsv_task, enable, geometry_var_names):
        import lxmaya.fnc.objects as mya_fnc_objects

        if enable is True:
            root = None
            if rsv_task:
                g_p = bsc_log.LogProcessContext(maximum=len(geometry_var_names))
                for i_var_name in geometry_var_names:
                    g_p.do_update()
                    #
                    keyword = 'asset-geometry-usd-{}-file'.format(i_var_name)
                    model_geometry_usd_hi_file = rsv_task.get_rsv_unit(keyword=keyword)
                    model_geometry_usd_hi_file_path = model_geometry_usd_hi_file.get_result(version='latest')
                    if model_geometry_usd_hi_file_path:
                        ipt = mya_fnc_objects.FncImporterForGeometryUsd(
                            option=dict(
                                file=model_geometry_usd_hi_file_path,
                                location=root,
                                port_match_patterns=['pg_*']
                            )
                        )
                        ipt.execute()
                    else:
                        bsc_log.Log.trace_method_warning(
                            'asset-build',
                            'unit="{}" is non-exists'.format(keyword)
                        )
                #
                g_p.set_stop()

    @classmethod
    def _set_model_act_geometry_dyn_build_(
        cls, rsv_task, with_model_act_geometry_dyn, model_act_properties, geometry_var_names
    ):
        import lxusd.core as usd_core

        import lxmaya.fnc.objects as mya_fnc_objects

        if with_model_act_geometry_dyn is True:
            dyn_sub_root = '/dyn/master/hi'
            if rsv_task:
                keyword = 'asset-geometry-abc-hi-dyn-file'
                model__act_abc_dyn__file = rsv_task.get_rsv_unit(keyword=keyword)
                model__act_abc_dyn__file_path = model__act_abc_dyn__file.get_result(version='latest')
                if model__act_abc_dyn__file_path:
                    mya_fnc_objects.FncImporterForGeometryAbc(
                        option=dict(
                            file=model__act_abc_dyn__file_path,
                            location=dyn_sub_root,
                            hidden=True
                        )
                    ).execute()
                #
                root = '/master'
                #
                keyword = 'asset-component-registry-usd-file'
                model_act__usd_registry__file = rsv_task.get_rsv_unit(keyword=keyword)
                model_act__usd_registry__file_path = model_act__usd_registry__file.get_result(version='latest')
                if model_act__usd_registry__file_path:
                    usd_stage_opt = usd_core.UsdStageOpt(model_act__usd_registry__file_path)
                    usd_prim = usd_stage_opt.get_obj(root)
                    usd_prim_opt = usd_core.UsdPrimOpt(usd_prim)
                    #
                    customize_attributes = usd_prim_opt.get_customize_attributes(
                        includes=model_act_properties
                    )
                    if not customize_attributes:
                        start_frame, end_frame = usd_stage_opt.get_frame_range()
                        if start_frame != end_frame:
                            customize_attributes = dict(
                                pg_start_frame=start_frame,
                                pg_end_frame=end_frame
                            )
                    #
                    mya_core.CmdObjOpt(
                        bsc_core.PthNodeOpt(root).translate_to('|').to_string()
                    ).create_customize_attributes(customize_attributes)

    @classmethod
    def _set_model_act_geometry_dyn_connect_(cls, with_model_act_geometry_dyn_connect):
        GeometryAlembicBlender(
            '/dyn/master/hi', '/master/hi'
        ).set_run()

    @classmethod
    def _set_geometry_uv_map_build_by_usd_(
        cls, rsv_task, with_surface_geometry_uv_map, geometry_var_names, uv_map_face_vertices_contrast
    ):
        import lxmaya.fnc.objects as mya_fnc_objects

        if with_surface_geometry_uv_map is True:
            root = None
            if rsv_task:
                g_p = bsc_log.LogProcessContext(maximum=len(geometry_var_names))
                for i_var_name in geometry_var_names[:1]:
                    g_p.do_update()
                    #
                    keyword = 'asset-geometry-usd-{}-file'.format(i_var_name)
                    surface_geometry_hi_file = rsv_task.get_rsv_unit(keyword=keyword)
                    surface_geometry_hi_file_path = surface_geometry_hi_file.get_result(version='latest')
                    if surface_geometry_hi_file_path:
                        ipt = mya_fnc_objects.FncImporterForGeometryUsd(
                            option=dict(
                                file=surface_geometry_hi_file_path,
                                location=root,
                            )
                        )
                        ipt.import_uv_map(
                            uv_map_face_vertices_contrast
                        )
                    else:
                        bsc_log.Log.trace_method_warning(
                            'asset-build',
                            'unit="{}" is non-exists'.format(keyword)
                        )
                #
                g_p.set_stop()

    @classmethod
    def _set_work_geometry_uv_map_build_by_usd_(
        cls, rsv_task, with_surface_work_geometry_uv_map, geometry_var_names, uv_map_face_vertices_contrast
    ):
        import lxmaya.fnc.objects as mya_fnc_objects

        if with_surface_work_geometry_uv_map is True:
            root = None
            if rsv_task:
                g_p = bsc_log.LogProcessContext(maximum=len(geometry_var_names))
                for i_var_name in geometry_var_names[:1]:
                    g_p.do_update()
                    #
                    keyword = 'asset-source-geometry-usd-{}-file'.format(i_var_name)
                    work_surface_geometry_hi_file = rsv_task.get_rsv_unit(keyword=keyword)
                    work_surface_geometry_hi_file_path = work_surface_geometry_hi_file.get_result(version='latest')
                    if work_surface_geometry_hi_file_path:
                        ipt = mya_fnc_objects.FncImporterForGeometryUsd(
                            option=dict(
                                file=work_surface_geometry_hi_file_path,
                                location=root,
                            )
                        )
                        ipt.import_uv_map(uv_map_face_vertices_contrast)
                    else:
                        bsc_log.Log.trace_method_warning(
                            'asset-build',
                            'unit="{}" is non-exists'.format(keyword)
                        )
                #
                g_p.set_stop()

    @classmethod
    def _set_groom_geometry_build_(cls, rsv_task, with_groom_geometry, with_groom_grow_geometry):
        import lxmaya.fnc.objects as mya_fnc_objects

        if with_groom_geometry is True:
            if rsv_task:
                xgen_collection_directory_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-collection-dir')
                xgen_collection_directory_path_tgt = xgen_collection_directory_rsv_unit.get_exists_result()
                xgen_collection_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-file')
                xgen_collection_file_paths = xgen_collection_file_rsv_unit.get_latest_results()
                xgen_grow_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-grow-mesh-file')
                xgen_grow_file_paths = xgen_grow_file_rsv_unit.get_latest_results()
                if xgen_collection_file_paths:
                    if with_groom_grow_geometry is True:
                        option = dict(
                            # xgen
                            xgen_collection_file=xgen_collection_file_paths,
                            xgen_collection_directory=xgen_collection_directory_path_tgt,
                            xgen_location='/master/hair',
                            # grow
                            grow_file=xgen_grow_file_paths,
                            grow_location='/master/hair/hair_shape/hair_growMesh',
                        )
                    else:
                        option = dict(
                            # xgen
                            xgen_collection_file=xgen_collection_file_paths,
                            xgen_collection_directory=xgen_collection_directory_path_tgt,
                            xgen_location='/master/hair',
                        )
                    #
                    mya_fnc_objects.FncImporterForGeometryXgen(
                        option=option
                    ).execute()

    @classmethod
    def _set_look_build_by_ass_(cls, rsv_task, enable):
        import lxmaya.fnc.objects as mya_fnc_objects

        if enable is True:
            root = None
            if rsv_task:
                look_ass_file = rsv_task.get_rsv_unit(keyword='asset-look-ass-file')
                look_ass_file_path = look_ass_file.get_result(version='latest')
                if look_ass_file_path:
                    mya_fnc_objects.FncLookAssImporterNew(
                        option=dict(
                            file=look_ass_file_path,
                            location='/master',
                            look_pass='default',
                            name_join_time_tag=True,
                        )
                    ).execute()
                else:
                    bsc_log.Log.trace_method_warning(
                        cls.KEY,
                        'rsv-unit={} is non-exists'.format(look_ass_file)
                    )

    @classmethod
    def _set_look_preview_build_by_yml_(cls, rsv_task, with_surface_look_preview):
        import lxmaya.fnc.objects as mya_fnc_objects

        #
        if with_surface_look_preview is True:
            if rsv_task:
                look_yml_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-look-yml-file')
                look_yml_file_path = look_yml_file_rsv_unit.get_result(version='latest')
                if look_yml_file_path:
                    rsv_unit_properties = look_yml_file_rsv_unit.generate_properties_by_result(look_yml_file_path)
                    version = rsv_unit_properties.get('version')
                    mya_fnc_objects.FncImporterForLookYml(
                        option=dict(
                            file=look_yml_file_path
                        )
                    ).execute()

    @classmethod
    def _set_work_look_preview_build_by_yml_(cls, rsv_task, with_surface_work_look_preview):
        import lxmaya.fnc.objects as mya_fnc_objects

        #
        if with_surface_work_look_preview is True:
            if rsv_task:
                look_yml_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-source-look-yml-file')
                work_look_yml_file_path = look_yml_file_rsv_unit.get_result(version='latest')
                if work_look_yml_file_path:
                    mya_fnc_objects.FncImporterForLookYml(
                        option=dict(
                            file=work_look_yml_file_path
                        )
                    ).execute()

    @classmethod
    def _set_camera_build_by_abc_(cls, rsv_task, with_camera):
        import lxmaya.fnc.objects as mya_fnc_objects
        #
        if with_camera is True:
            if rsv_task is not None:
                dcc_data = rsv_task.get_rsv_project().get_dcc_data(application=bsc_core.SysApplicationMtd.get_current())
                location = dcc_data.get('camera_root')
                camera_main_abc_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-camera-main-abc-file')
                camera_main_abc_file_path = camera_main_abc_file_rsv_unit.get_result(version='latest')
                if camera_main_abc_file_path:
                    mya_fnc_objects.FncImporterForCameraAbc(
                        option=dict(
                            file=camera_main_abc_file_path,
                            location=location
                        )
                    ).set_run()

    @classmethod
    def _set_light_build_by_ass_(cls, rsv_task, with_light):
        if with_light is True:
            if rsv_task is not None:
                light_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-light-ass-file')
                light_ass_file_path = light_ass_file_rsv_unit.get_result(version='latest')
                if light_ass_file_path:
                    light_ass_file_opt = bsc_storage.StgFileOpt(light_ass_file_path)
                    obj = mya_dcc_objects.Shape(light_ass_file_opt.name_base)
                    if obj.get_is_exists() is False:
                        obj = obj.set_create('aiStandIn')
                    #
                    atr_raw = dict(
                        dso=light_ass_file_path,
                        # mode=6
                    )
                    [obj.get_port(k).set(v) for k, v in atr_raw.items()]

    @classmethod
    def _set_scene_save_(cls, rsv_asset, save_scene):
        if save_scene is True:
            if rsv_asset is not None:
                user_directory_path = bsc_storage.StgTmpBaseMtd.get_user_directory('builder')
                file_path = '{}/{}.ma'.format(
                    user_directory_path, '-'.join(rsv_asset.path.split('/')[1:]+[bsc_core.SysBaseMtd.get_time_tag()])
                    )

                mya_dcc_objects.Scene.save_to_file(file_path)

    @classmethod
    def _set_render_(cls, render_resolution):
        mya_dcc_objects.Scene.set_render_resolution(
            *render_resolution
        )

    def set_run(self):
        import lxresolver.core as rsv_core

        #
        with_model_geometry = self.get('with_model_geometry')
        with_model_act_geometry_dyn = self.get('with_model_act_geometry_dyn')
        with_model_act_geometry_dyn_connect = self.get('with_model_act_geometry_dyn_connect')
        model_act_properties = self.get('model_act_properties')
        #
        with_surface_cfx_geometry = self.get('with_surface_cfx_geometry')
        #
        with_groom_geometry = self.get('with_groom_geometry')
        with_groom_grow_geometry = self.get('with_groom_grow_geometry')
        #
        with_surface_geometry_uv_map = self.get('with_surface_geometry_uv_map')
        with_surface_work_geometry_uv_map = self.get('with_surface_work_geometry_uv_map')
        uv_map_face_vertices_contrast = self.get('uv_map_face_vertices_contrast')
        #
        with_surface_look = self.get('with_surface_look')
        with_surface_work_look = self.get('with_surface_work_look')
        with_surface_cfx_look = self.get('with_surface_cfx_look')
        #
        with_surface_look_preview = self.get('with_surface_look_preview')
        with_surface_work_look_preview = self.get('with_surface_work_look_preview')
        #
        with_camera = self.get('with_camera')
        with_light = self.get('with_light')
        #
        render_resolution = self.get('render_resolution')
        #
        save_scene = self.get('save_scene')
        #
        geometry_var_names = self.get('geometry_var_names')
        #
        project = self.get('project')
        asset = self.get('asset')
        #
        resolver = rsv_core.RsvBase.generate_root()
        rsv_project = resolver.get_rsv_project(project=project)
        #
        rsv_asset = rsv_project.get_rsv_resource(asset=asset)
        #
        model_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.model'),
            task=rsv_project.properties.get('asset_tasks.model')
        )
        model_act_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.model'),
            task=rsv_project.properties.get('asset_tasks.model_dynamic'),
        )
        groom_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.groom'),
            task=rsv_project.properties.get('asset_tasks.groom')
        )
        surface_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.surface'),
            task=rsv_project.properties.get('asset_tasks.surface')
        )
        surface_occ_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.surface'),
            task=rsv_project.properties.get('asset_tasks.surface_prv')
        )
        surface_cfx_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.surface'),
            task=rsv_project.properties.get('asset_tasks.surface_cfx')
        )
        #
        camera_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.camera'),
            task=rsv_project.properties.get('asset_tasks.camera')
        )
        light_rsv_task = rsv_project.get_rsv_task(
            asset='lightrig',
            step=rsv_project.properties.get('asset_steps.light_rig'),
            task=rsv_project.properties.get('asset_tasks.light_rig')
        )
        #
        method_args = [
            (self._build_geometry_from_usd_, (model_rsv_task, with_model_geometry, geometry_var_names)),
            (self._set_model_act_geometry_dyn_build_,
             (model_act_rsv_task, with_model_act_geometry_dyn, model_act_properties, geometry_var_names)),
            #
            (self._build_geometry_from_usd_, (surface_cfx_rsv_task, with_surface_cfx_geometry, geometry_var_names)),
            #
            (self._set_groom_geometry_build_, (groom_rsv_task, with_groom_geometry, with_groom_grow_geometry)),
            #
            (self._set_geometry_uv_map_build_by_usd_,
             (surface_rsv_task, with_surface_geometry_uv_map, geometry_var_names, uv_map_face_vertices_contrast)),
            (self._set_work_geometry_uv_map_build_by_usd_,
             (surface_rsv_task, with_surface_work_geometry_uv_map, geometry_var_names, uv_map_face_vertices_contrast)),
            #
            (self._set_look_build_by_ass_, (surface_rsv_task, with_surface_look)),
            (self._set_look_build_by_ass_, (surface_cfx_rsv_task, with_surface_cfx_look)),
            #
            (self._set_look_preview_build_by_yml_, (surface_occ_rsv_task, with_surface_look_preview)),
            (self._set_work_look_preview_build_by_yml_, (surface_occ_rsv_task, with_surface_work_look_preview)),
            #
            (self._set_model_act_geometry_dyn_connect_, (with_model_act_geometry_dyn_connect,)),
            #
            (self._set_camera_build_by_abc_, (camera_rsv_task, with_camera)),
            (self._set_light_build_by_ass_, (light_rsv_task, with_light)),
            #
            (self._set_render_, (render_resolution,)),
            #
            (self._set_scene_save_, (rsv_asset, save_scene)),
        ]
        if method_args:
            with bsc_log.LogProcessContext.create(
                maximum=len(method_args), label='execute geometry build method'
            ) as g_p:
                for i_method, i_args in method_args:
                    g_p.do_update()
                    #
                    i_method(*i_args)


class FncBuilderForAssetNew(bsc_fnc_abstracts.AbsFncOptionBase):
    KEY = 'asset build'
    OPTION = dict(
        project='',
        asset='',
        #
        root='/master',
        # data
        with_geometry=False,
        with_geometry_uv_map=False,
        with_look=False,
        with_surface_preview=False,
        # key
        with_model=False,
        with_model_dynamic=False,
        model_act_properties=['pg_start_frame', 'pg_end_frame'],
        # model
        model_space='release',  # or 'work'
        model_elements=[
            'renderable',
            'auxiliary'
        ],
        #
        with_groom=False,
        with_groom_grow=False,
        # groom
        groom_space='release',  # or 'work'
        groom_elements=[
            'renderable'
        ],
        #
        with_surface=False,
        # surface
        surface_space='release',  # or 'work'
        surface_elements=[
            'renderable'
        ]
    )

    def __init__(self, option=None):
        super(FncBuilderForAssetNew, self).__init__(option)
        import lxresolver.core as rsv_core

        #
        project = self.get('project')
        asset = self.get('asset')
        #
        resolver = rsv_core.RsvBase.generate_root()
        rsv_project = resolver.get_rsv_project(project=project)
        #
        self._rsv_asset = rsv_project.get_rsv_resource(asset=asset)
        #
        self._model_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.model'),
            task=rsv_project.properties.get('asset_tasks.model')
        )
        self._model_dynamic_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.model'),
            task=rsv_project.properties.get('asset_tasks.model_dynamic')
        )
        self._groom_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.groom'),
            task=rsv_project.properties.get('asset_tasks.groom')
        )
        self._surface_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.surface'),
            task=rsv_project.properties.get('asset_tasks.surface')
        )
        self._surface_prv_rsv_task = rsv_project.get_rsv_task(
            asset=asset,
            step=rsv_project.properties.get('asset_steps.surface'),
            task=rsv_project.properties.get('asset_tasks.surface_prv')
        )

    @classmethod
    def build_model_geometry_fnc(cls, rsv_task, space):
        if rsv_task is not None:
            import lxmaya.fnc.objects as mya_fnc_objects

            #
            if space == 'work':
                keyword = 'asset-source-geometry-usd-payload-file'
            elif space == 'release':
                keyword = 'asset-geometry-usd-payload-file'
            else:
                raise RuntimeError()
            rsv_unit = rsv_task.get_rsv_unit(keyword=keyword)
            file_path = rsv_unit.get_result(version='latest')
            if file_path:
                mya_fnc_objects.FncImporterForGeometryNew(
                    option=dict(
                        file=file_path,
                        root='/master',
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
                        port_match_patterns=['pg_*']
                    )
                ).execute()

    @classmethod
    def build_model_dynamic_geometry_fnc(cls, rsv_task, space, property_names):
        if rsv_task:
            dyn_sub_root = '/dyn/master/hi'
            import lxusd.core as usd_core

            import lxmaya.fnc.objects as mya_fnc_objects

            #
            keyword = 'asset-geometry-abc-hi-dyn-file'
            model__act_abc_dyn__file = rsv_task.get_rsv_unit(keyword=keyword)
            model__act_abc_dyn__file_path = model__act_abc_dyn__file.get_result(version='latest')
            if model__act_abc_dyn__file_path:
                mya_fnc_objects.FncImporterForGeometryAbc(
                    option=dict(
                        file=model__act_abc_dyn__file_path,
                        location=dyn_sub_root,
                        hidden=True
                    )
                ).execute()
                #
                GeometryAlembicBlender(
                    '/dyn/master/hi', '/master/hi'
                ).set_run()
            #
            root = '/master'
            #
            keyword = 'asset-component-registry-usd-file'
            usd_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword)
            usd_file_path = usd_file_rsv_unit.get_result(version='latest')
            if usd_file_path:
                usd_stage_opt = usd_core.UsdStageOpt(usd_file_path)
                usd_prim = usd_stage_opt.get_obj(root)
                usd_prim_opt = usd_core.UsdPrimOpt(usd_prim)
                #
                customize_attributes = usd_prim_opt.get_customize_attributes(
                    includes=property_names
                )
                if not customize_attributes:
                    start_frame, end_frame = usd_stage_opt.get_frame_range()
                    if start_frame != end_frame:
                        customize_attributes = dict(
                            pg_start_frame=start_frame,
                            pg_end_frame=end_frame
                        )
                #
                mya_core.CmdObjOpt(
                    bsc_core.PthNodeOpt(root).translate_to('|').to_string()
                ).create_customize_attributes(customize_attributes)

    @classmethod
    def build_groom_geometry_fnc(cls, rsv_task, space, with_groom_grow):
        import lxmaya.fnc.objects as mya_fnc_objects

        if rsv_task:
            xgen_collection_directory_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-collection-dir')
            xgen_collection_directory_path_tgt = xgen_collection_directory_rsv_unit.get_exists_result()
            xgen_collection_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-file')
            xgen_collection_file_paths = xgen_collection_file_rsv_unit.get_latest_results()
            xgen_grow_file_rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-xgen-grow-mesh-file')
            xgen_grow_file_paths = xgen_grow_file_rsv_unit.get_latest_results()
            if xgen_collection_file_paths:
                if with_groom_grow is True:
                    option = dict(
                        # xgen
                        xgen_collection_file=xgen_collection_file_paths,
                        xgen_collection_directory=xgen_collection_directory_path_tgt,
                        xgen_location='/master/hair',
                        # grow
                        grow_file=xgen_grow_file_paths,
                        grow_location='/master/hair/hair_shape/hair_growMesh',
                    )
                else:
                    option = dict(
                        # xgen
                        xgen_collection_file=xgen_collection_file_paths,
                        xgen_collection_directory=xgen_collection_directory_path_tgt,
                        xgen_location='/master/hair',
                    )
                #
                mya_fnc_objects.FncImporterForGeometryXgen(
                    option=option
                ).execute()

    @classmethod
    def build_surface_geometry_uv_map_fnc(cls, rsv_task, space):
        if rsv_task is not None:
            import lxmaya.fnc.objects as mya_fnc_objects

            #
            if space == 'work':
                keyword = 'asset-source-geometry-usd-payload-file'
            elif space == 'release':
                keyword = 'asset-geometry-usd-payload-file'
            else:
                raise RuntimeError()
            rsv_unit = rsv_task.get_rsv_unit(keyword=keyword)
            file_path = rsv_unit.get_result(version='latest')
            if file_path:
                mya_fnc_objects.FncImporterForGeometryNew(
                    option=dict(
                        file=file_path,
                        root='/master',
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
                        port_match_patterns=['pg_*'],
                        #
                        uv_map_only=True
                    )
                ).execute()

    @classmethod
    def build_surface_look_fnc(cls, rsv_task, space):
        if rsv_task:
            import lxmaya.fnc.objects as mya_fnc_objects

            #
            if space == 'work':
                keyword = 'asset-source-look-ass-file'
            elif space == 'release':
                keyword = 'asset-look-ass-file'
            else:
                raise RuntimeError()
            #
            rsv_unit = rsv_task.get_rsv_unit(keyword=keyword)
            file_path = rsv_unit.get_result(version='latest')
            if file_path:
                mya_fnc_objects.FncLookAssImporterNew(
                    option=dict(
                        file=file_path,
                        location='/master',
                        look_pass='default',
                        name_join_time_tag=True,
                    )
                ).execute()
            else:
                bsc_log.Log.trace_method_warning(
                    cls.KEY,
                    'rsv-unit={} is non-exists'.format(rsv_unit)
                )

    @classmethod
    def build_surface_look_preview_fnc(cls, rsv_task, space):
        if rsv_task:
            import lxmaya.fnc.objects as mya_fnc_objects

            #
            if space == 'work':
                keyword = 'asset-source-look-yml-file'
            elif space == 'release':
                keyword = 'asset-look-yml-file'
            else:
                raise RuntimeError()
            #
            rsv_unit = rsv_task.get_rsv_unit(keyword=keyword)
            file_path = rsv_unit.get_result(version='latest')
            if file_path:
                mya_fnc_objects.FncImporterForLookYml(
                    option=dict(
                        file=file_path
                    )
                ).execute()
            else:
                bsc_log.Log.trace_method_warning(
                    cls.KEY,
                    'file is not found'
                )

        else:
            bsc_log.Log.trace_method_warning(
                cls.KEY,
                'task is not found'
            )

    def execute(self):
        method_args = []
        # geometry
        if self.get('with_geometry') is True:
            if self.get('with_model') is True:
                method_args.append(
                    (self.build_model_geometry_fnc, (self._model_rsv_task, self.get('model_space')))
                )
            if self.get('with_model_dynamic') is True:
                method_args.append(
                    (self.build_model_dynamic_geometry_fnc,
                     (self._model_dynamic_rsv_task, self.get('model_space'), self.get('model_act_properties')))
                )
            if self.get('with_groom') is True:
                method_args.append(
                    (self.build_groom_geometry_fnc,
                     (self._groom_rsv_task, self.get('groom_space'), self.get('with_groom_grow')))
                )
        # geometry uv map
        if self.get('with_geometry_uv_map') is True:
            if self.get('with_surface') is True:
                method_args.append(
                    (self.build_surface_geometry_uv_map_fnc, (self._surface_rsv_task, self.get('surface_space')))
                )
        #
        if self.get('with_look') is True:
            # either surface_preview or surface
            # check surface preview first
            if self.get('with_surface_preview') is True:
                method_args.append(
                    (self.build_surface_look_preview_fnc, (self._surface_prv_rsv_task, self.get('surface_space')))
                )
            elif self.get('with_surface') is True:
                method_args.append(
                    (self.build_surface_look_fnc, (self._surface_rsv_task, self.get('surface_space')))
                )
        #
        if method_args:
            with bsc_log.LogProcessContext.create(
                maximum=len(method_args), label='execute asset build method'
            ) as g_p:
                for i_mtd, i_args in method_args:
                    g_p.do_update()
                    #
                    i_mtd(*i_args)


if __name__ == '__main__':
    pass
