# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log
# maya
from ...core.wrap import *

from ... import core as mya_core

from ... import abstracts as mya_abstracts
# maya dcc objects
from . import utility as mya_dcc_obj_utility

from . import node_for_dag as mya_dcc_obj_node_for_dag


class Material(mya_abstracts.AbsMyaNode):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    DCC_CONNECTION_CLS = mya_dcc_obj_utility.Connection
    #
    SHADING_NODE_TYPES = ['mesh', 'pgYetiMaya', 'nurbsHair']
    OBJ_TYPE = 'shadingEngine'

    def __init__(self, path):
        super(Material, self).__init__(path)

    def get_assign_dict(self):
        dic = {}
        _ = cmds.sets(self.path, query=1)
        if _:
            paths = [i for i in cmds.ls(_, leaf=1, noIntermediate=1, long=1)]
            for i_arg in paths:
                # Object Group
                show_type = cmds.ls(i_arg, showType=1)[1]
                if show_type in self.SHADING_NODE_TYPES:
                    dic.setdefault('obj', []).append(i_arg)
                # Component Object Group
                elif show_type == 'float3':
                    # check component is whole
                    i_path, i_comp_name = i_arg.split('.')
                    face_count = cmds.polyEvaluate(i_path, face=1)
                    whole_obj_cmp_name = 'f[0:{}]'.format(face_count-1)
                    if i_comp_name == whole_obj_cmp_name:
                        dic.setdefault('obj', []).append(i_path)
                    else:
                        dic.setdefault('obj_cmp', []).append(i_arg)
        return dic

    def get_assign_nodes(self):
        list_ = []
        _ = cmds.sets(self.path, query=1)
        if _:
            paths = [i for i in cmds.ls(_, leaf=1, noIntermediate=1, long=1)]
            for i_arg in paths:
                # Object Group
                show_type = cmds.ls(i_arg, showType=1)[1]
                if show_type in self.SHADING_NODE_TYPES:
                    list_.append(mya_dcc_obj_node_for_dag.Shape(i_arg))
                elif show_type == 'float3':
                    # check component is whole
                    i_path, i_comp_name = i_arg.split('.')
                    face_count = cmds.polyEvaluate(i_path, face=1)
                    whole_obj_cmp_name = 'f[0:{}]'.format(face_count-1)
                    if i_comp_name == whole_obj_cmp_name:
                        list_.append(mya_dcc_obj_node_for_dag.Shape(i_path))
        return list_

    def set_create(self, type_name):
        if self.get_is_exists() is False:
            mya_core.CmdObjOpt._create_material_(
                self.name, type_name
            )
            bsc_log.Log.trace_method_result(
                'shader create',
                u'obj="{}"'.format(self.path)
            )


class Shader(mya_abstracts.AbsMyaNode):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    DCC_CONNECTION_CLS = mya_dcc_obj_utility.Connection
    #
    CATEGORY_DICT = {}

    def __init__(self, path):
        super(Shader, self).__init__(path)

    def set_create(self, obj_type):
        if self.get_is_exists() is False:
            name = self.name
            bsc_log.Log.trace_method_result(
                self.KEY,
                'create node: "{}"'.format(self.path)
            )
            category = mya_core.ShaderCategory.get(obj_type, 'utility')
            kwargs = dict(
                name=name,
                skipSelect=1
            )
            if category == 'shader':
                kwargs['asShader'] = 1
            elif category == 'texture':
                kwargs['asTexture'] = 1
            elif category == 'light':
                kwargs['asLight'] = 1
            elif category == 'utility':
                kwargs['asUtility'] = 1
            #
            result = cmds.shadingNode(
                obj_type, **kwargs
            )
            return result


class AndShader(Shader):
    CATEGORY_DICT = {}

    def __init__(self, path):
        super(AndShader, self).__init__(path)

    def set_create(self, obj_type):
        if self.get_is_exists() is False:
            name = self.name
            bsc_log.Log.trace_method_result(
                self.KEY,
                u'create node: "{}"'.format(self.path)
            )
            category = mya_core.ShaderCategory.get(obj_type, 'utility')
            kwargs = dict(
                name=name,
                skipSelect=1
            )
            if category == 'shader':
                kwargs['asShader'] = 1
            elif category == 'texture':
                kwargs['asTexture'] = 1
            elif category == 'light':
                kwargs['asLight'] = 1
            elif category == 'utility':
                kwargs['asUtility'] = 1
            # noinspection PyArgumentList
            result = cmds.shadingNode(
                obj_type, **kwargs
            )
            return result
