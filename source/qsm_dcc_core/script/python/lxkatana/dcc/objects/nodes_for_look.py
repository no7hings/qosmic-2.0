# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# katana
from ...core.wrap import *

from ... import core as ktn_core

from ... import abstracts as ktn_abstracts

from . import node_for_look as ktn_dcc_obj_node_for_look


class Materials(ktn_abstracts.AbsKtnObjs):
    DCC_TYPES_INCLUDE = [
        'NetworkMaterial'
    ]
    DCC_NODE_CLS = ktn_dcc_obj_node_for_look.Material

    def __init__(self, *args):
        super(Materials, self).__init__(*args)

    @classmethod
    def get_material_dict(cls):
        dic_0 = {}
        objs = cls.get_objs()
        for obj in objs:
            if obj.get_parent().ktn_obj.isBypassed() is True:
                continue
            key = obj.get_port('sceneGraphLocation').get()
            #
            dic_0.setdefault(
                key, []
            ).append(obj)
        #
        dic = {}
        #
        for k, v in dic_0.items():
            nme_objs = [i for i in v if i.get_parent().type == 'NetworkMaterialEdit']
            nmc_objs = [i for i in v if i.get_parent().type == 'NetworkMaterialCreate']
            #
            if nme_objs:
                dic[k] = nme_objs[0]
            else:
                # if len(nmc_objs) > 1:
                #     print nmc_objs
                dic[k] = nmc_objs[0]
        return dic

    @classmethod
    def get_nmc_material_dict(cls):
        dic_0 = {}
        objs = cls.get_objs()
        for obj in objs:
            if obj.get_parent().ktn_obj.isBypassed() is True:
                continue
            #
            key = obj.get_port('sceneGraphLocation').get()
            dic_0.setdefault(
                key, []
            ).append(obj)
        #
        dic = {}
        #
        for k, v in dic_0.items():
            nmc_objs = [i for i in v if i.get_parent().type == 'NetworkMaterialCreate']
            if nmc_objs:
                dic[k] = nmc_objs[0]
        return dic

    @classmethod
    def get_nme_material_dict(cls):
        dic_0 = {}
        objs = cls.get_objs()
        for obj in objs:
            if obj.get_parent().ktn_obj.isBypassed() is True:
                continue
            #
            key = obj.get_port('sceneGraphLocation').get()
            dic_0.setdefault(
                key, []
            ).append(obj)
        #
        dic = {}
        #
        for k, v in dic_0.items():
            nme_objs = [i for i in v if i.get_parent().type == 'NetworkMaterialEdit']
            if nme_objs:
                dic[k] = nme_objs[0]
        return dic

    @classmethod
    def pre_run_fnc(cls):
        _ = NodegraphAPI.GetAllNodesByType('NetworkMaterialEdit') or []
        if _:
            gp = bsc_log.LogProcessContext(maximum=len(_))
            #
            for i_ktn_obj in _:
                gp.do_update()
                # noinspection PyBroadException
                try:
                    ktn_core.NGNmeOpt(i_ktn_obj).set_contents_update()
                except Exception:
                    bsc_core.ExceptionMtd.set_print()
                    #
                    bsc_log.Log.trace_error(
                        'materials update "NetworkMaterialEdit" "{}" is failed'.format(i_ktn_obj.getName())
                    )
            #
            gp.set_stop()


class AndShaders(ktn_abstracts.AbsKtnObjs):
    DCC_TYPES_INCLUDE = [
        'ArnoldShadingNode'
    ]
    DCC_NODE_CLS = ktn_dcc_obj_node_for_look.AndShader

    def __init__(self, *args):
        super(AndShaders, self).__init__(*args)

    @classmethod
    def get_texture_references(cls, **kwargs):
        lis = []
        _ = cls.get_objs(**kwargs)
        for i in _:
            if i.get_port('nodeType').get() == 'image':
                lis.append(i)
        return lis

    @classmethod
    def get_standard_surfaces(cls, **kwargs):
        lis = []
        _ = cls.get_objs(**kwargs)
        for i in _:
            if i.get_port('nodeType').get() == 'standard_surface':
                lis.append(i)
        return lis

    @classmethod
    def pre_run_fnc(cls):
        _ = NodegraphAPI.GetAllNodesByType('NetworkMaterialEdit') or []
        if _:
            for i_ktn_obj in _:
                # noinspection PyBroadException
                try:
                    ktn_core.NGNmeOpt(i_ktn_obj).set_contents_update()
                except Exception:
                    bsc_core.ExceptionMtd.set_print()
                    #
                    bsc_log.Log.trace_error(
                        'shaders update "NetworkMaterialEdit" "{}" is failed'.format(i_ktn_obj.getName())
                    )
