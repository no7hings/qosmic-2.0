# coding:utf-8
# maya
from ...core.wrap import *

from ... import core as mya_core

from ... import abstracts as mya_abstracts

from . import node_for_dag as mya_dcc_obj_node_for_dag

from . import node_for_geometry as mya_dcc_obj_node_for_geometry


class Groups(mya_abstracts.AbsMyaNodes):
    DCC_NODE_CLS = mya_dcc_obj_node_for_dag.Group

    def __init__(self, *args):
        super(Groups, self).__init__(*args)

    @classmethod
    def get_paths(cls, reference=True, paths_exclude=None):
        def set_exclude_filter_fnc_(paths):
            if paths_exclude is not None:
                [paths.remove(_i) for _i in paths_exclude if _i in paths]
            return paths

        _ = mya_core.MyaUtil.get_all_group_paths()
        if paths_exclude is not None:
            return set_exclude_filter_fnc_(_)
        if reference is True:
            return _
        return set_exclude_filter_fnc_(
            [i for i in _ if not cmds.referenceQuery(i, isNodeReferenced=1)]
        )


class Shapes(mya_abstracts.AbsMyaNodes):
    DCC_NODE_CLS = mya_dcc_obj_node_for_dag.Shape

    def __init__(self, *args):
        super(Shapes, self).__init__(*args)

    @classmethod
    def get_paths(cls, reference=True, paths_exclude=None):
        def set_exclude_filter_fnc_(paths):
            if paths_exclude is not None:
                [paths.remove(_i) for _i in paths_exclude if _i in paths]
            return paths

        _ = mya_core.MyaUtil.get_all_shape_paths()
        if paths_exclude is not None:
            return set_exclude_filter_fnc_(_)
        if reference is True:
            return _
        return set_exclude_filter_fnc_(
            [i for i in _ if not cmds.referenceQuery(i, isNodeReferenced=1)]
        )


class Geometries(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = [
        'mesh',
        'nurbsCurve',
        'nurbsSurface'
    ]
    #
    DCC_NODE_CLS = mya_dcc_obj_node_for_dag.Shape

    def __init__(self, *args):
        super(Geometries, self).__init__(*args)


class Meshes(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = [
        'mesh',
    ]
    #
    DCC_NODE_CLS = mya_dcc_obj_node_for_geometry.Mesh

    def __init__(self, *args):
        super(Meshes, self).__init__(*args)
