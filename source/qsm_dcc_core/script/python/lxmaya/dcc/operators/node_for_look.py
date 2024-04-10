# coding:utf-8
import collections

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxarnold.core as and_core
# maya
from ...core.wrap import *

from ... import core as mya_core
# maya dcc objects
from ..objects import node as mya_dcc_obj_node
# maya dcc operators
from . import node_for_geometry as mya_dcc_opt_geometry


class AbsLookOpt(object):
    def __init__(self, *args):
        self._obj = args[0]

    @property
    def obj(self):
        return self._obj

    def get_material_assign_is_default(self):
        return self.get_material_paths() == [u'initialShadingGroup']

    def get_material_paths(self):
        shape_path = self._obj.path
        return cmds.listConnections(
            shape_path, destination=1, source=0, type=mya_core.MyaNodeTypes.Material
        ) or []

    def get_materials(self):
        return [mya_dcc_obj_node.Node(i) for i in self.get_material_paths()]

    def set_default_material_assign(self):
        shape_path = self._obj.path
        value = 'initialShadingGroup'
        cmds.sets(shape_path, forceElement=value)
        bsc_log.Log.trace_method_result(
            'material-assign',
            u'assign="{}" >> "{}"'.format(shape_path, value)
        )

    # noinspection PyUnusedLocal
    def assign_materials(self, material_assigns, force=False):
        for key, value in material_assigns.items():
            if key == 'all':
                self.assign_material_to_path(value)
            else:
                self.__set_comp_material_(
                    key, value
                )

    def assign_material_to_path(self, material_path):
        shape_path = self._obj.path
        self._assign_material_to_path_(shape_path, material_path)

    def __set_comp_material_(self, comp_name, material_path):
        shape_path = self._obj.path
        comp_path = '.'.join([shape_path, comp_name])
        self._assign_material_to_path_(comp_path, material_path)

    @classmethod
    def _assign_material_to_path_(cls, geometry_path, material_path):
        if cmds.objExists(material_path) is True:
            _ = cmds.sets(material_path, query=1) or []
            _ = [cmds.ls(i, long=1)[0] for i in _]
            if geometry_path not in _:
                # noinspection PyBroadException
                try:
                    cmds.sets(geometry_path, forceElement=material_path)
                    bsc_log.Log.trace_method_result(
                        'material-assign',
                        u'assign="{}" >> "{}"'.format(geometry_path, material_path)
                    )
                except Exception:
                    bsc_core.ExceptionMtd.set_print()
                    bsc_log.Log.trace_method_error(
                        'material-assign',
                        u'assign="{}" >> "{}"'.format(geometry_path, material_path)
                    )
        else:
            bsc_log.Log.trace_method_warning(
                'material-assign',
                'material-obj="{}" is non-exists'.format(material_path)
            )

    def set_properties(self, properties):
        for key, value in properties.items():
            self._obj.get_port(key).set(value)

    def assign_render_visibilities(self, visibilities, renderer='arnold'):
        for key, value in visibilities.items():
            self._obj.get_port(key).set(value)

    @mya_core.MyaModifier.undo_debug_run
    def set_surface_shader(self, shader_path):
        shape_path = self._obj.path
        if cmds.objExists(shader_path) is True:
            material_path = '{}_SG'.format(shader_path)
            exists_material_paths = self.get_material_paths()
            if exists_material_paths:
                _ = exists_material_paths[-1]
                if _ != 'initialShadingGroup':
                    material_path = _
            #
            if cmds.objExists(material_path) is False:
                cmds.sets(renderable=1, noSurfaceShader=1, empty=1, n=material_path)
            #
            cmds.connectAttr(shader_path+'.outColor', material_path+'.surfaceShader')
            cmds.sets(shape_path, forceElement=material_path)

    def set_displacement_shader(self, shader_path):
        shape_path = self._obj.path
        if cmds.objExists(shader_path) is True:
            material_path = '{}_SG'.format(shader_path)
            exists_material_paths = self.get_material_paths()
            if exists_material_paths:
                _ = exists_material_paths[-1]
                if _ != 'initialShadingGroup':
                    material_path = _
            #
            if cmds.objExists(material_path) is False:
                cmds.sets(renderable=1, noSurfaceShader=1, empty=1, n=material_path)
            #
            cmds.connectAttr(shader_path+'.displacement', material_path+'.displacementShader')
            cmds.sets(shape_path, forceElement=material_path)


class ShapeLookOpt(AbsLookOpt):
    def __init__(self, *args):
        super(ShapeLookOpt, self).__init__(*args)


class MeshLookOpt(AbsLookOpt):
    def __init__(self, *args):
        super(MeshLookOpt, self).__init__(*args)

    def get_material_assigns(self):
        material_assigns = collections.OrderedDict()
        transform_path = self._obj.transform.path
        shape_path = self._obj.path
        material_paths = self.get_material_paths()
        if material_paths:
            for material_path in material_paths:
                elements = cmds.sets(material_path, query=1)
                if elements:
                    element_paths = [i for i in cmds.ls(elements, leaf=1, noIntermediate=1, long=1)]
                    for element_path in element_paths:
                        show_type = cmds.ls(element_path, showType=1)[1]
                        value = material_path
                        value = mya_core.MyaUtil.get_path_with_namespace_clear(value)
                        #
                        key = None
                        if show_type in [mya_core.MyaNodeTypes.Mesh]:
                            if element_path == shape_path:
                                key = 'all'
                        elif show_type == 'float3':
                            if element_path.startswith(transform_path):
                                comp_name = element_path.split('.')[-1]
                                mesh_obj_opt = mya_dcc_opt_geometry.MeshOpt(self._obj)
                                if mesh_obj_opt.get_comp_name_is_whole(comp_name) is True:
                                    key = 'all'
                                else:
                                    key = comp_name
                        #
                        if key is not None:
                            material_assigns[key] = value
        return material_assigns

    def get_face_assign_comp_names(self):
        lis = []
        material_assigns = self.get_material_assigns()
        if material_assigns:
            for k, v in material_assigns.items():
                if k != 'all':
                    lis.append(k)
        return lis

    def get_render_properties(self, renderer='arnold'):
        properties = collections.OrderedDict()
        if renderer == 'arnold':
            for key in and_core.AndGeometryProperties.AllKeys:
                if key in and_core.AndGeometryProperties.MayaMapper:
                    dcc_port_path = and_core.AndGeometryProperties.MayaMapper[key]
                    port = self._obj.get_port(dcc_port_path)
                    if port.get_is_exists() is True:
                        value = port.get()
                        properties[key] = value
                    else:
                        bsc_log.Log.trace_warning(
                            'port: "{}" is Non-exists'.format(port.path)
                        )
        return properties

    def assign_render_properties(self, properties, renderer='arnold'):
        if renderer == 'arnold':
            for key, value in properties.items():
                if key in and_core.AndGeometryProperties.MayaMapper:
                    dcc_port_path = and_core.AndGeometryProperties.MayaMapper[key]
                    self._obj.get_port(dcc_port_path).set(value)

    def get_render_visibilities(self, renderer='arnold'):
        visibilities = collections.OrderedDict()
        if renderer == 'arnold':
            kwargs = {key: self._obj.get_port(v).get() for key, v in
                      and_core.AndVisibilities.MAYA_VISIBILITY_DICT.items()}
            value = and_core.AndVisibilities.get_visibility(**kwargs)
            visibilities[and_core.AndVisibilities.VISIBILITY] = value
            #
            value = self._obj.get_port(and_core.AndVisibilities.MAYA_AUTOBUMP_VISIBILITY).get()
            visibilities[and_core.AndVisibilities.AUTOBUMP_VISIBILITY] = value
        return visibilities

    def assign_render_visibilities(self, visibilities, renderer='arnold'):
        if renderer == 'arnold':
            kwargs = and_core.AndVisibilities.get_visibility_as_dict(visibilities[and_core.AndVisibilities.VISIBILITY])
            for key, value in kwargs.items():
                if key in and_core.AndVisibilities.MAYA_VISIBILITY_DICT:
                    dcc_port_path = and_core.AndVisibilities.MAYA_VISIBILITY_DICT[key]
                    self._obj.get_port(dcc_port_path).set(value)
            #
            port = self._obj.get_port(and_core.AndVisibilities.MAYA_AUTOBUMP_VISIBILITY)
            if port.get_is_exists() is True:
                port.set(visibilities[and_core.AndVisibilities.AUTOBUMP_VISIBILITY])

    def get_subsets_by_material_assign(self):
        """
import lxmaya

lxmaya.set_reload()

import lxmaya.dcc.objects as mya_dcc_objects

import lxmaya.dcc.operators as mya_dcc_operators

m = mya_dcc_objects.Mesh('mesh_001')

m_o = mya_dcc_operators.MeshLookOpt(m)

print m_o.get_subsets_by_material_assign()
        :return:
        """
        subset_dict = {}
        transform_path = self._obj.get_transform().get_name()
        shape_path = self._obj.path
        shading_engines = cmds.listConnections(
            shape_path, destination=1, source=0, type='shadingEngine'
        ) or []
        if len(shading_engines) > 1:
            for i_shading_engine in shading_engines:
                i_elements = cmds.sets(i_shading_engine, query=1)
                if i_elements:
                    i_element_paths = [i for i in cmds.ls(i_elements, leaf=1, noIntermediate=1, long=1)]
                    for j_element_path in i_element_paths:
                        if j_element_path.startswith(transform_path):
                            j_comp = j_element_path.split('.f[')[-1][:-1]
                            if ':' in j_comp:
                                j_ = j_comp.split(':')
                                j_indices = range(int(j_[0]), int(j_[1]))
                            else:
                                j_indices = [int(j_comp)]

                            subset_dict.setdefault(i_shading_engine, []).extend(j_indices)
        return subset_dict


class XgenDescriptionLookOpt(AbsLookOpt):
    def __init__(self, *args):
        super(XgenDescriptionLookOpt, self).__init__(*args)

    def get_material_assigns(self):
        material_assigns = collections.OrderedDict()
        shape_path = self._obj.path
        material_paths = self.get_material_paths()
        if material_paths:
            for material_path in material_paths:
                elements = cmds.sets(material_path, query=1)
                if elements:
                    element_paths = [i for i in cmds.ls(elements, leaf=1, noIntermediate=1, long=1)]
                    for element_path in element_paths:
                        if element_path == shape_path:
                            value = material_path
                            value = mya_core.MyaUtil.get_path_with_namespace_clear(value)
                            key = 'all'
                            material_assigns[key] = value
        return material_assigns

    def get_render_properties(self, renderer='arnold'):
        properties = collections.OrderedDict()
        if renderer == 'arnold':
            for key in and_core.AndHairProperties.ALL:
                if key in and_core.AndHairProperties.MAYA_XGEN_DESCRIPTION_DICT:
                    value = and_core.AndHairProperties.MAYA_XGEN_DESCRIPTION_DICT[key]
                    port = self._obj.get_port(value)
                    if port.get_is_exists() is True:
                        value = port.get()
                        properties[key] = value
                    else:
                        bsc_log.Log.trace_warning(
                            'port: "{}" is Non-exists'.format(port.path)
                        )
        return properties

    def set_properties(self, properties, renderer='arnold'):
        if renderer == 'arnold':
            for key, value in properties.items():
                if key in and_core.AndHairProperties.MAYA_XGEN_DESCRIPTION_DICT:
                    dcc_port_path = and_core.AndHairProperties.MAYA_XGEN_DESCRIPTION_DICT[key]
                    port = self._obj.get_port(dcc_port_path)
                    if port.get_is_exists() is True:
                        port.set(value)

    def get_render_visibilities(self, renderer='arnold'):
        visibilities = collections.OrderedDict()
        if renderer == 'arnold':
            kwargs = {k: self._obj.get_port(v).get() for k, v in and_core.AndVisibilities.MAYA_VISIBILITY_DICT.items()}
            value = and_core.AndVisibilities.get_visibility(**kwargs)
            visibilities[and_core.AndVisibilities.VISIBILITY] = value
        return visibilities

    def assign_render_visibilities(self, visibilities, renderer='arnold'):
        if renderer == 'arnold':
            kwargs = and_core.AndVisibilities.get_visibility_as_dict(visibilities[and_core.AndVisibilities.VISIBILITY])
            for key, value in kwargs.items():
                if key in and_core.AndVisibilities.MAYA_VISIBILITY_DICT:
                    dcc_port_path = and_core.AndVisibilities.MAYA_VISIBILITY_DICT[key]
                    self._obj.get_port(dcc_port_path).set(value)


class ObjsLookOpt(object):
    SHAPE_TYPE_NAMES = [
        'mesh',
        'xgmDescription'
    ]
    TEXTURE_REFERENCE_TYPE_NAMES = [
        'file',
        'aiImage',
        'osl_window_box',
        'osl_window_box_s'
    ]

    def __init__(self, objs):
        self._objs = objs

    def get_material_paths(self):
        set_ = set([])
        for i_obj in self._objs:
            if i_obj.type in self.SHAPE_TYPE_NAMES:
                i_shape_look_opt = ShapeLookOpt(i_obj)
                i_material_paths = i_shape_look_opt.get_material_paths()
                for j_path in i_material_paths:
                    set_.add(j_path)
        return list(set_)

    def get_texture_reference_paths(self):
        def rcs_fnc_(obj_path_):
            _ = cmds.listConnections(obj_path_, destination=0, source=1) or []
            for _i in _:
                _obj_type_name = cmds.nodeType(_i)
                if _obj_type_name in self.TEXTURE_REFERENCE_TYPE_NAMES:
                    lis.append(_i)
                if _i not in keys:
                    keys.append(_i)
                    rcs_fnc_(_i)

        #
        keys = []
        lis = []
        #
        material_paths = self.get_material_paths()
        for i_path in material_paths:
            rcs_fnc_(i_path)

        return lis
