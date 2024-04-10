# coding:utf-8
import lxbasic.core as bsc_core
# katana
from ... import core as ktn_core
# katana dcc
from ..objects import node as ktn_dcc_obj_node

from . import look as ktn_dcc_opt_look


class AssetWorkspaceOptOld(object):
    WHITE_SHADER_DICT = {
        'base_color': (1, .955, .905),
        #
        'specular': 0.75,
        'specular_roughness': 0.375,
        'specular_IOR': 1.33,
        #
        'sheen': 1,
        'sheen_color': (1, 0.985, 0.925),
        #
        'subsurface': 0.105,
        'subsurface_color': (1, 0.75, 0.25),
        'subsurface_radius': (0.8, 0.8, 0.8),
        'subsurface_scale': 0.125,
    }
    WHITE_DISP_GEOMETRY_PROPERTIES_DICT = dict(
        # invert_normals=False,
        smoothing=True,
        subdiv_type='catclark',
        subdiv_iterations=2,
        #
        # disp_padding=0,
        # disp_height=1,
        # disp_zero_value=0,
        # disp_autobump=True,
    )
    WHITE_ZBRUSH_GEOMETRY_PROPERTIES_DICT = dict(
        smoothing=True,
    )

    def __init__(self, workspace):
        self._workspace = workspace

    #
    @ktn_core.Modifier.undo_debug_run
    def set_auto_ambocc_assign(self, pass_name='default'):
        configure = self._workspace.get_configure(pass_name)
        # geometry_root = configure.get('option.geometry_root')
        material_root = configure.get('option.material_root')
        geometries = self._workspace.get_sg_geometries(pass_name)
        # update assign cache first
        self._workspace.set_ng_material_assigns_cache_update()
        for i_geometry in geometries:
            self._set_ambocc_assign_(i_geometry, pass_name)

    def _set_ambocc_assign_(self, geometry, pass_name):
        geometry_type_name = geometry.type_name
        dcc_material_assign = self._workspace.get_ng_material_assign_from_cache(
            geometry
        )
        if dcc_material_assign is None:
            name = '{}__override'.format(geometry.name)
            material_group_dcc_path = self._workspace.get_ng_material_group_path(
                name, pass_name
            )
            material_group_is_create, dcc_material_group = self._workspace.get_ng_material_group_force(
                material_group_dcc_path, pass_name
            )
            material_dcc_path = self._workspace.get_ng_material_path(
                name, pass_name
            )
            material_is_create, dcc_material = self._workspace.get_ng_material_force(
                material_dcc_path, pass_name
            )
            material_assign_dcc_path = self._workspace.get_ng_material_assign_path(
                name, pass_name
            )
            material_assign_is_create, dcc_material_assign = self._workspace.get_ng_material_assign_force(
                material_assign_dcc_path, pass_name
            )
            material_assign_dcc_opt = ktn_dcc_opt_look.MaterialAssignOpt(dcc_material_assign)
            material_assign_dcc_opt.assign_material(dcc_material)
            material_assign_dcc_opt.set_geometry_path_append(geometry.path)

            shader_dcc_name = '{}__surface__override'.format(dcc_material.name)
            shader_dcc_path = '{}/{}'.format(dcc_material.get_parent().path, shader_dcc_name)
            if geometry_type_name in ['renderer procedural']:
                color = (0.37, 0.08, 0.37)
                self._set_ambocc_create_(
                    dcc_material,
                    shader_dcc_path,
                    color
                )
            elif geometry_type_name in ['subdmesh']:
                self._set_opacity_lambert_create_(
                    dcc_material,
                    shader_dcc_path,
                )
        else:
            material_sg_path = dcc_material_assign.get_port(
                'args.materialAssign.value'
            ).get()
            if material_sg_path:
                material_dcc_name = bsc_core.PthNodeOpt(material_sg_path).name
                dcc_material = ktn_dcc_obj_node.Node(material_dcc_name)
                shader_dcc_name = '{}__surface__override'.format(dcc_material.name)
                shader_dcc_path = '{}/{}'.format(dcc_material.get_parent().path, shader_dcc_name)
                self._set_convert_to_occ_(dcc_material, shader_dcc_path)

    #
    @classmethod
    def _set_convert_to_occ_(cls, dcc_material, dcc_shader_path):
        dcc_shader = dcc_material.get_input_port('arnoldSurface').get_source_obj()
        if dcc_shader:
            dcc_shader_opt = ktn_dcc_opt_look.AndShaderOpt(dcc_shader)
            shader_type_name = dcc_shader_opt.get_type_name()
            if shader_type_name == 'lambert':
                cls._set_lambert_convert_to_occ_(dcc_shader_opt, dcc_shader_path)
            elif shader_type_name == 'standard_surface':
                cls._set_standard_surface_convert_to_occ_(dcc_shader_opt, dcc_shader_path)
            elif shader_type_name == 'standard_hair':
                cls._set_standard_hair_convert_to_occ_(dcc_shader_opt, dcc_shader_path)

    @classmethod
    def _set_lambert_convert_to_occ_(cls, dcc_shader_opt, dcc_shader_path):
        opacity_value = dcc_shader_opt.get('opacity')
        opacity_source = dcc_shader_opt.get_port_source('opacity')
        if opacity_source is None:
            if opacity_value == [1.0, 1.0, 1.0]:
                value = dcc_shader_opt.get('Kd_color')
                dcc_source = dcc_shader_opt.get_port_source('Kd_color')
                dcc_targets = dcc_shader_opt.get_port_targets('out')
                #
                dcc_occ = ktn_dcc_obj_node.Node(dcc_shader_path)
                dcc_occ_opt = ktn_dcc_opt_look.AndShaderOpt(dcc_occ)
                dcc_occ_opt.set_create('ambient_occlusion')
                dcc_occ_opt.set('white', value)
                dcc_occ_opt.set('far_clip', 10)
                if dcc_source is not None:
                    dcc_occ_opt.set_port_source('white', dcc_source, validation=True)
                    dcc_occ_opt.set_port_source('black', dcc_source, validation=True)
                if dcc_targets:
                    for i_dcc_target in dcc_targets:
                        dcc_occ_opt.set_port_target('out', i_dcc_target, validation=True)

    @classmethod
    def _set_standard_surface_convert_to_occ_(cls, dcc_shader_opt, dcc_shader_path):
        opacity_value = dcc_shader_opt.get('opacity')
        opacity_source = dcc_shader_opt.get_port_source('opacity')
        if opacity_source is None:
            if opacity_value == [1.0, 1.0, 1.0]:
                value = dcc_shader_opt.get('base_color')
                dcc_source = dcc_shader_opt.get_port_source('base_color')
                dcc_targets = dcc_shader_opt.get_port_targets('out')
                #
                dcc_occ = ktn_dcc_obj_node.Node(dcc_shader_path)
                dcc_occ_opt = ktn_dcc_opt_look.AndShaderOpt(dcc_occ)
                dcc_occ_opt.set_create('ambient_occlusion')
                dcc_occ_opt.set('white', value)
                dcc_occ_opt.set('far_clip', 10)
                if dcc_source is not None:
                    dcc_occ_opt.set_port_source('white', dcc_source, validation=True)
                    dcc_occ_opt.set_port_source('black', dcc_source, validation=True)
                if dcc_targets:
                    for i_dcc_target in dcc_targets:
                        dcc_occ_opt.set_port_target('out', i_dcc_target, validation=True)

    @classmethod
    def _set_standard_hair_convert_to_occ_(cls, dcc_shader_opt, dcc_shader_path):
        opacity_value = dcc_shader_opt.get('opacity')
        opacity_source = dcc_shader_opt.get_port_source('opacity')
        if opacity_source is None:
            if opacity_value == [1.0, 1.0, 1.0]:
                value = dcc_shader_opt.get('base_color')
                dcc_source = dcc_shader_opt.get_port_source('base_color')
                dcc_targets = dcc_shader_opt.get_port_targets('out')
                #
                dcc_occ = ktn_dcc_obj_node.Node(dcc_shader_path)
                dcc_occ_opt = ktn_dcc_opt_look.AndShaderOpt(dcc_occ)
                dcc_occ_opt.set_create('ambient_occlusion')
                dcc_occ_opt.set('white', value)
                dcc_occ_opt.set('far_clip', 10)
                if dcc_source is not None:
                    dcc_occ_opt.set_port_source('white', dcc_source, validation=True)
                    dcc_occ_opt.set_port_source('black', dcc_source, validation=True)
                if dcc_targets:
                    for i_dcc_target in dcc_targets:
                        dcc_occ_opt.set_port_target('out', i_dcc_target, validation=True)

    @classmethod
    def _set_occ_create_(cls, dcc_material, dcc_path, color):
        dcc_occ_opt = ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_obj_node.Node(dcc_path)
        )
        dcc_occ_opt.set_create('ambient_occlusion')
        dcc_occ_opt.set_port_target(
            'out', dcc_material.get_input_port('arnoldSurface'),
            validation=True
        )
        dcc_occ_opt.set('white', color)
        dcc_occ_opt.set('far_clip', 10)

    @classmethod
    def _set_opacity_lambert_create_(cls, dcc_material, dcc_path):
        dcc_shader_opt = ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_obj_node.Node(dcc_path)
        )
        dcc_shader_opt.set_create('lambert')
        dcc_shader_opt.set_port_target(
            'out', dcc_material.get_input_port('arnoldSurface'),
            validation=True
        )
        dcc_shader_opt.set('opacity', [0.0, 0.0, 0.0])

    #
    @ktn_core.Modifier.undo_debug_run
    def set_auto_white_disp_assign(self, pass_name='default'):
        configure = self._workspace.get_configure(pass_name)
        # geometry_root = configure.get('option.geometry_root')
        material_root = configure.get('option.material_root')
        geometries = self._workspace.get_sg_geometries(pass_name)
        # update assign cache first
        self._workspace.set_ng_material_assigns_cache_update()
        for i_geometry in geometries:
            self._set_white_disp_assign_(i_geometry, pass_name)

        dcc_look_pass, ktn_look_pass = self._workspace.get_ng_look_pass(pass_name)
        if ktn_look_pass is not None:
            dcc_look_pass.set(
                'look_pass.scheme', pass_name
            )

    def _set_white_disp_assign_(self, geometry, pass_name):
        geometry_type_name = geometry.type_name
        dcc_material_assign = self._workspace.get_ng_material_assign_from_cache(
            geometry
        )
        if dcc_material_assign is None:
            name = '{}__override'.format(geometry.name)
            material_group_dcc_path = self._workspace.get_ng_material_group_path(
                name, pass_name
            )
            material_group_is_create, dcc_material_group = self._workspace.get_ng_material_group_force(
                material_group_dcc_path, pass_name
            )
            material_dcc_path = self._workspace.get_ng_material_path(
                name, pass_name
            )
            material_is_create, dcc_material = self._workspace.get_ng_material_force(
                material_dcc_path, pass_name
            )
            material_assign_dcc_path = self._workspace.get_ng_material_assign_path(
                name, pass_name
            )
            material_assign_is_create, dcc_material_assign = self._workspace.get_ng_material_assign_force(
                material_assign_dcc_path, pass_name
            )
            material_assign_dcc_opt = ktn_dcc_opt_look.MaterialAssignOpt(dcc_material_assign)
            material_assign_dcc_opt.assign_material(dcc_material)
            material_assign_dcc_opt.set_geometry_path_append(geometry.path)

            shader_dcc_name = '{}__surface__override'.format(dcc_material.name)
            shader_dcc_path = '{}/{}'.format(dcc_material.get_parent().path, shader_dcc_name)
            if geometry_type_name in ['renderer procedural']:
                color = (1, 0.955, 0.905)
                self._set_plastic_create_(
                    dcc_material,
                    shader_dcc_path,
                    color
                )
            elif geometry_type_name in ['subdmesh']:
                self._set_white_create_(
                    dcc_material,
                    shader_dcc_path,
                )
        else:
            material_sg_path = dcc_material_assign.get_port(
                'args.materialAssign.value'
            ).get()
            if material_sg_path:
                material_dcc_name = bsc_core.PthNodeOpt(material_sg_path).name
                dcc_material = ktn_dcc_obj_node.Node(material_dcc_name)
                shader_dcc_name = '{}__surface__override'.format(dcc_material.name)
                shader_dcc_path = '{}/{}'.format(dcc_material.get_parent().path, shader_dcc_name)
                if geometry_type_name in ['renderer procedural']:
                    self._set_convert_to_plastic_(dcc_material, shader_dcc_path, (1, 0.955, 0.905))
                elif geometry_type_name in ['subdmesh']:
                    self._set_convert_to_white_disp_(dcc_material, shader_dcc_path)

    @classmethod
    def _set_plastic_create_(cls, dcc_material, dcc_path, color):
        dcc_shader_opt = ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_obj_node.Node(dcc_path)
        )
        is_create = dcc_shader_opt.set_create('utility')
        if is_create is True:
            dcc_shader_opt.set_port_target(
                'out', dcc_material.get_input_port('arnoldSurface'),
                validation=True
            )
            dcc_shader_opt.set('shade_mode', '4')
            dcc_shader_opt.set('color', color)
        return dcc_shader_opt

    @classmethod
    def _set_convert_to_plastic_(cls, dcc_material, dcc_shader_path, color):
        dcc_shader = dcc_material.get_input_port('arnoldSurface').get_source_obj()
        if dcc_shader:
            dcc_shader_opt = ktn_dcc_opt_look.AndShaderOpt(dcc_shader)
            dcc_targets = dcc_shader_opt.get_port_targets('out')
            #
            dcc_plastic_opt = cls._set_plastic_create_(
                dcc_material, dcc_shader_path, color
            )

    @classmethod
    def _set_ambocc_create_(cls, dcc_material, dcc_path, color):
        dcc_shader_opt = ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_obj_node.Node(dcc_path)
        )
        dcc_shader_opt.set_create('utility')
        dcc_shader_opt.set_port_target(
            'out', dcc_material.get_input_port('arnoldSurface'),
            validation=True
        )
        dcc_shader_opt.set('shade_mode', '3')
        dcc_shader_opt.set('color', color)

    @classmethod
    def _set_white_create_(cls, dcc_material, dcc_path):
        dcc_shader_opt = ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_obj_node.Node(dcc_path)
        )
        is_create = dcc_shader_opt.set_create('standard_surface')
        if is_create is True:
            dcc_shader_opt.set_port_target(
                'out', dcc_material.get_input_port('arnoldSurface'),
                validation=True
            )
            for k, v in cls.WHITE_SHADER_DICT.items():
                dcc_shader_opt.set(k, v)
        return dcc_shader_opt

    @classmethod
    def _set_displacement_fix_(cls, dcc_shader_opt):
        dcc_shader_opt.set('output_min', 1), dcc_shader_opt.set('output_max', 0)
        dcc_shader_opt.set('contrast_pivot', 0.5)
        return dcc_shader_opt

    @classmethod
    def _set_convert_to_white_disp_(cls, dcc_material, dcc_shader_path):
        dcc_surface_shader = dcc_material.get_input_port('arnoldSurface').get_source_obj()
        if dcc_surface_shader:
            cls._set_white_create_(dcc_material, dcc_shader_path)
        #
        dcc_displacement_shader = dcc_material.get_input_port('arnoldDisplacement').get_source_obj()
        if dcc_displacement_shader:
            dcc_displacement_shader_opt = ktn_dcc_opt_look.AndShaderOpt(dcc_displacement_shader)
            # cls._set_displacement_fix_(dcc_displacement_shader_opt)

    @classmethod
    def _set_convert_to_white_zbrush_(cls, dcc_material, dcc_shader_path):
        dcc_surface_shader = dcc_material.get_input_port('arnoldSurface').get_source_obj()
        if dcc_surface_shader:
            cls._set_white_create_(dcc_material, dcc_shader_path)

    #
    @ktn_core.Modifier.undo_debug_run
    def set_auto_white_zbrush_assign(self, pass_name='default'):
        configure = self._workspace.get_configure(pass_name)
        # geometry_root = configure.get('option.geometry_root')
        material_root = configure.get('option.material_root')
        geometries = self._workspace.get_sg_geometries(pass_name)
        # update assign cache first
        self._workspace.set_ng_material_assigns_cache_update()
        for i_geometry in geometries:
            self._set_white_zbrush_assign_(i_geometry, pass_name)

        dcc_look_pass, ktn_look_pass = self._workspace.get_ng_look_pass(pass_name)
        if ktn_look_pass is not None:
            dcc_look_pass.set(
                'look_pass.scheme', pass_name
            )

    def _set_white_zbrush_assign_(self, geometry, pass_name):
        geometry_type_name = geometry.type_name
        dcc_material_assign = self._workspace.get_ng_material_assign_from_cache(
            geometry
        )
        if dcc_material_assign is None:
            name = '{}__override'.format(geometry.name)
            material_group_dcc_path = self._workspace.get_ng_material_group_path(
                name, pass_name
            )
            material_group_is_create, dcc_material_group = self._workspace.get_ng_material_group_force(
                material_group_dcc_path, pass_name
            )
            material_dcc_path = self._workspace.get_ng_material_path(
                name, pass_name
            )
            material_is_create, dcc_material = self._workspace.get_ng_material_force(
                material_dcc_path, pass_name
            )
            material_assign_dcc_path = self._workspace.get_ng_material_assign_path(
                name, pass_name
            )
            material_assign_is_create, dcc_material_assign = self._workspace.get_ng_material_assign_force(
                material_assign_dcc_path, pass_name
            )
            material_assign_dcc_opt = ktn_dcc_opt_look.MaterialAssignOpt(dcc_material_assign)
            material_assign_dcc_opt.assign_material(dcc_material)
            material_assign_dcc_opt.set_geometry_path_append(geometry.path)

            shader_dcc_name = '{}__surface__override'.format(dcc_material.name)
            shader_dcc_path = '{}/{}'.format(dcc_material.get_parent().path, shader_dcc_name)
            if geometry_type_name in ['renderer procedural']:
                color = (1, 0.955, 0.905)
                self._set_plastic_create_(
                    dcc_material,
                    shader_dcc_path,
                    color
                )
            elif geometry_type_name in ['subdmesh']:
                self._set_white_create_(
                    dcc_material,
                    shader_dcc_path,
                )
        else:
            i_sg_material_path = dcc_material_assign.get_port(
                'args.materialAssign.value'
            ).get()
            if i_sg_material_path:
                material_dcc_name = bsc_core.PthNodeOpt(i_sg_material_path).name
                dcc_material = ktn_dcc_obj_node.Node(material_dcc_name)
                shader_dcc_name = '{}__surface__override'.format(dcc_material.name)
                shader_dcc_path = '{}/{}'.format(dcc_material.get_parent().path, shader_dcc_name)
                if geometry_type_name in ['renderer procedural']:
                    self._set_convert_to_plastic_(dcc_material, shader_dcc_path, (1, 0.955, 0.905))
                elif geometry_type_name in ['subdmesh']:
                    self._set_convert_to_white_zbrush_(dcc_material, shader_dcc_path)

    #
    @ktn_core.Modifier.undo_debug_run
    def set_auto_geometry_properties_assign(self, pass_name='default', geometry_properties=None):
        geometries = self._workspace.get_sg_geometries(pass_name)
        self._workspace.set_ng_property_assigns_cache_update()
        for i_geometry in geometries:
            i_geometry_type_name = i_geometry.type_name
            i_dcc_property_assign = self._workspace.get_ng_property_assign_from_cache(i_geometry)
            if i_dcc_property_assign is not None:
                if i_geometry_type_name in ['subdmesh']:
                    self._workspace._set_arnold_geometry_properties_(
                        i_dcc_property_assign,
                        geometry_properties
                    )
