# coding:utf-8
import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# arnold
import lxarnold.core as and_core
# maya
from .. import core as mya_core
# maya dcc
from ..dcc import objects as mya_dcc_objects

from ..dcc import operators as mya_dcc_operators


class ScpLibraryLook(object):
    class UserDatas(object):
        ColorChoice = 'color_choice'
        ColorChoiceWeight = 'color_choice_weight'
        ColorHsvOffset = 'color_hsv_offset'
        #
        ColorHOffset = 'color_h_offset'
        ColorSOffset = 'color_s_offset'
        ColorVOffset = 'color_v_offset'

    def __init__(self, location):
        self._location = location
        self._group = mya_dcc_objects.Group(
            bsc_core.PthNodeOpt(self._location).translate_to('|').get_path()
        )

    def rename_look(self, prefix_name):
        """
import lxmaya

lxmaya.set_reload()

import lxmaya.scripts as mya_scripts

import lxmaya.dcc.objects as mya_dcc_objects

mya_scripts.ScpLibraryLook('/geometries').rename_look(
    'tree_g001_rsc'
)
        :param prefix_name:
        :return:
        """
        exclude_obj_types = ['groupId', 'colorManagementGlobals', 'mesh', 'shadingEngine']

        materials = set()
        shaders = set()
        mesh_paths = self._group.get_all_shape_paths(include_obj_type=['mesh'])

        for i_mesh_path in mesh_paths:
            i_mesh_look_opt = mya_dcc_operators.MeshLookOpt(mya_dcc_objects.Mesh(i_mesh_path))
            i_materials = i_mesh_look_opt.get_materials()
            for j_material in i_materials:
                materials.add(j_material)
                j_source_objs = j_material.get_all_source_objs()
                for k_obj in j_source_objs:
                    shaders.add(k_obj)
        #
        index = 0
        for i_material in materials:
            i_new_name = '{}__{}_{}'.format(prefix_name, 'material', index).lower()
            try:
                i_material.set_rename(i_new_name)
            except:
                pass
            index += 1
        #
        index = 0
        for i_shader in shaders:
            i_type_name = i_shader.get_type_name()
            if i_shader.get_type_name() in exclude_obj_types:
                continue
            i_new_name = '{}__{}_{}'.format(prefix_name, i_type_name, index).lower()
            # noinspection PyBroadException
            try:
                i_shader.set_rename(i_new_name)
            except:
                pass
            index += 1

    @classmethod
    def create_user_datas(cls, prefix_name):
        """
import lxmaya

lxmaya.set_reload()

import lxmaya.scripts as mya_scripts

mya_scripts.ScpLibraryLook.create_user_datas()
        :return:
        """
        shaders = mya_dcc_objects.Nodes(['aiStandardSurface']).get_objs()

        ro_name = '{}__ro'.format(prefix_name)
        ro_path, ro_is_create = mya_dcc_objects.Shader(ro_name).get_dcc_instance(
            'aiUserDataColor'
        )
        ro = mya_dcc_objects.Node(ro_path)
        if ro_is_create is True:
            ro.set('attribute', cls.UserDatas.ColorChoice)
            ro.set('default', [0, 0, 0])

        ho_name = '{}__ho'.format(prefix_name)
        ho_path, ho_is_create = mya_dcc_objects.Shader(ho_name).get_dcc_instance(
            'aiUserDataColor'
        )
        ho = mya_dcc_objects.Node(ho_path)
        if ho_is_create is True:
            ho.set('attribute', cls.UserDatas.ColorHsvOffset)
            ho.set('default', [.5, .5, .5])

        for i_shader in shaders:
            if i_shader.get_port('subsurface').has_source() is True:
                i_color_port = i_shader.get_port('baseColor')
                i_color_source = i_color_port.get_source()
                i_cc_name = '{}__cc'.format(i_color_port.path.replace('.', '__').lower())

                i_cc_path, i_cc_is_create = mya_dcc_objects.Shader(i_cc_name).get_dcc_instance(
                    'osl_color_correct'
                )
                if i_cc_is_create is True:
                    pass
                i_cc = mya_dcc_objects.Node(i_cc_path)

                if i_color_source:
                    i_cc.get_port('input').set_source(i_color_source)

                i_cc.get_port('outColor').set_target(i_color_port)

                ro.get_port('outColor').set_target(i_cc.get_port('rgb_over'))
                ho.get_port('outColor.outColorR').set_target(i_cc.get_port('h_offset'))
                ho.get_port('outColor.outColorG').set_target(i_cc.get_port('s_offset'))
                ho.get_port('outColor.outColorB').set_target(i_cc.get_port('v_offset'))

    def get_all_materials(self):
        materials = set()
        mesh_paths = self._group.get_all_shape_paths(include_obj_type=['mesh'])
        for i_mesh_path in mesh_paths:
            i_mesh_look_opt = mya_dcc_operators.MeshLookOpt(mya_dcc_objects.Mesh(i_mesh_path))
            i_materials = i_mesh_look_opt.get_materials()
            for j_material in i_materials:
                materials.add(j_material)

        list_ = list(materials)
        list_.sort(key=lambda x: x.get_name())
        return list_

    def get_look_preview_data(self, texture_directory_path, resource_name):
        def get_surface_shader_fnc_(material_):
            for _i_key in surface_keys:
                _i_shader = material_.get_port(_i_key).get_source_obj()
                if _i_shader is not None:
                    return _i_shader
            return None

        def bake_texture_fnc(shader_, texture_type_, key_, seq_):
            _texture_file_path = '{}/{}_{}.{}.jpg'.format(
                texture_directory_path, resource_name, seq_, texture_type_
            )
            if bsc_storage.StgPathMtd.get_is_exists(_texture_file_path) is False:
                _diffuse_name = '{}_{}_{}'.format(resource_name, texture_type_, seq)
                cmds.convertSolidTx(
                    '{}.{}'.format(shader_.get_path(), key_),
                    name=_diffuse_name,
                    resolutionX=2048, resolutionY=2048,
                    samplePlane=1,
                    fileImageName=_texture_file_path,
                    fileFormat='jpg',
                    backgroundMode='extend'
                )
            return _texture_file_path

        def get_texture_file_path_fnc_(shader_, texture_type_, key_, seq_):
            _texture_file_path = '{}/{}_{}.{}.jpg'.format(
                texture_directory_path, resource_name, seq_, texture_type_
            )
            if bsc_storage.StgPathMtd.get_is_exists(_texture_file_path) is False:
                _texture_src = None
                _shaders = shader_.get_all_source_objs_at(key_)
                if _shaders:
                    for _i_shader in _shaders:
                        if _i_shader.get_type_name() in texture_c:
                            _texture_src = _i_shader.get(texture_c[_i_shader.get_type_name()])
                            break
                #
                if _texture_src:
                    _result = s.get_result(_texture_src)
                    if _result:
                        bsc_storage.StgFileOpt(_result).copy_to_file(_texture_file_path)
            return _texture_file_path
        # noinspection PyUnresolvedReferences
        import maya.cmds as cmds

        s = bsc_storage.StgFileSearchOpt(ignore_name_case=True, ignore_ext_case=True, ignore_ext=True)
        s.set_search_directories(['/production/library/resource/share/texture/plant-unorganized/jpg'])

        texture_c = {'file': 'fileTextureName', 'aiImage': 'filename'}
        surface_keys = ['aiSurfaceShader', 'surfaceShader']

        texture_method_dict = {
            'diffuse': (bake_texture_fnc, 'baseColor'),
            'roughness': (bake_texture_fnc, 'specularRoughness'),
            'normal': (get_texture_file_path_fnc_, 'normalCamera')
        }

        c = ctt_core.Content()

        bsc_storage.StgDirectoryOpt(texture_directory_path).set_create()

        materials = self.get_all_materials()
        for seq, i_material in enumerate(materials):
            i_surface_shader = get_surface_shader_fnc_(i_material)
            if i_surface_shader:
                for i_key, (i_mtd, i_atr) in texture_method_dict.items():
                    i_file_path = i_mtd(i_surface_shader, i_key, i_atr, seq)
                    c.set(
                        'materials.{}.{}'.format(i_material.get_name(), i_key), i_file_path
                    )

        return c.get_value()

    @staticmethod
    def collection_texture_fnc(s, shader, category_name, type_name, texture_type, key):
        directory_path = '/production/library/resource/share/texture/plant-search/{}/{}'.format(
            category_name, type_name, texture_type
        )
        texture_c = {'file': 'fileTextureName', 'aiImage': 'filename'}
        texture_src = None
        shaders = shader.get_all_source_objs_at(key)
        if shaders:
            for i_shader in shaders:
                if i_shader.get_type_name() in texture_c:
                    texture_src = i_shader.get(texture_c[i_shader.get_type_name()])
                    break
        #
        if texture_src:
            result = s.get_result(texture_src)
            if result:
                result_tgt = '{}/{}'.format(directory_path, bsc_storage.StgFileOpt(result).get_name())
                result_tgt_opt = bsc_storage.StgFileOpt(result_tgt)
                if result_tgt_opt.get_is_exists() is False:
                    bsc_storage.StgFileOpt(result).copy_to_file(result_tgt)
                return True, result_tgt
        return False, texture_src

    @staticmethod
    def find_surface_shader_fnc(material):
        surface_keys = ['aiSurfaceShader', 'surfaceShader']
        for i_key in surface_keys:
            i_shader = material.get_port(i_key).get_source_obj()
            if i_shader is not None:
                return i_shader
        return None

    def get_texture_search_data(self, category_name, type_name):
        s = bsc_storage.StgFileSearchOpt(ignore_name_case=True, ignore_ext_case=True, ignore_ext=True)
        s.set_search_directories(['/production/library/resource/share/texture/plant-unorganized/jpg'])

        texture_method_dict = {
            'diffuse': (self.collection_texture_fnc, 'baseColor'),
        }

        c = ctt_core.Content()

        materials = self.get_all_materials()
        for seq, i_material in enumerate(materials):
            i_surface_shader = self.find_surface_shader_fnc(i_material)
            if i_surface_shader:
                for i_key, (i_mtd, i_atr) in texture_method_dict.items():
                    i_state, i_file_path = i_mtd(s, i_surface_shader, category_name, type_name, i_key, i_atr)
                    if i_state is True:
                        c.set(
                            'textures.{}.{}'.format(i_material.get_name(), i_key), i_file_path
                        )
                    else:
                        c.set(
                            'textures.{}.{}'.format(i_material.get_name(), i_key), None
                        )
                        j = bsc_storage.StgFileOpt('/production/library/resource/.data/3d_plant_proxy/texture-lost.json')
                        d_p = j.set_read()
                        d_p[i_file_path] = ''
                        j.set_write(d_p)
        return c.get_value()

    def split_meshes_by_subsets(self, customize_attributes):
        """
import lxmaya

lxmaya.set_reload()

import lxmaya.scripts as mya_scripts

mya_scripts.ScpLibraryLook('/geometries').split_meshes_by_subsets()
        :return:
        """
        mesh_paths = self._group.get_all_shape_paths(include_obj_type=['mesh'])
        for i_mesh_path in mesh_paths:
            i_shape_opt = mya_core.CmdShapeOpt(i_mesh_path)
            i_shape_opt.assign_render_properties(and_core.AndGeometryProperties.AdaptiveSubdivision)
            i_mesh_opt = mya_core.Om2MeshOpt(i_mesh_path)
            i_render_properties = i_shape_opt.get_render_properties()
            i_subsets = i_shape_opt.get_subsets_by_material_assign()
            if i_subsets:
                i_material_paths = i_subsets.keys()
                i_material_paths.sort()
                with bsc_log.LogProcessContext.create_as_bar(maximum=len(i_material_paths), label='mesh split') as l_p:
                    for j_seq, j_material_path in enumerate(i_material_paths):
                        j_face_indices = i_subsets[j_material_path]
                        bsc_log.Log.debug('start at {}'.format(j_seq))
                        j_subset = i_mesh_opt.duplicate_faces_(j_face_indices)
                        j_subset_shape_opt = mya_core.CmdShapeOpt(j_subset)
                        j_subset_shape_opt.rename_transform('{}_{}'.format(i_shape_opt.get_transform_name(), str(j_seq+1).zfill(3)))
                        j_subset_shape_opt.parent_transform_to_path(self._group.get_path())
                        j_subset_shape_opt.assign_material_to_path(j_material_path)
                        j_subset_shape_opt.assign_render_properties(i_render_properties)
                        j_subset_shape_opt.create_customize_attributes(customize_attributes)
                        #
                        l_p.do_update()
                #
                i_shape_opt.delete_transform()

    def auto_group_by_component(self, category_path, resource_path):
        component_yml_file_opt = bsc_storage.StgFileOpt(
            '/production/library/resource/.data/3d_plant_proxy/texture-component-mapper.yml'
        )
        search_json_file_opt = bsc_storage.StgFileOpt(
            '/production/library/resource/.data/3d_plant_proxy/texture-search.json'
        )
        data_0 = component_yml_file_opt.set_read()
        #
        if category_path not in data_0:
            raise KeyError()
        data_0_ = data_0[category_path]
        mapper = {i: k for k, v in data_0_.items() for i in v}
        #
        data_1 = search_json_file_opt.set_read()
        if resource_path not in data_1:
            raise KeyError()
        data_1_ = data_1[resource_path]
        if data_1_:
            location = self._location
            group = mya_dcc_objects.Group(bsc_core.PthNodeOpt(location).translate_to('|').get_path())
            for k, v in data_1_['textures'].items():
                i_material_path = k
                i_file_path = v['diffuse']
                i_file_opt = bsc_storage.StgFileOpt(i_file_path)
                i_name = i_file_opt.get_name_base()
                i_component_name = mapper[i_name]
                i_component_group = group.create_child(i_component_name)
                i_material = mya_dcc_objects.Material(i_material_path)
                for j_node in i_material.get_assign_nodes():
                    j_node.get_transform().set_parent(i_component_group)
