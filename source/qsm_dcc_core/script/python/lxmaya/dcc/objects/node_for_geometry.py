# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.dcc.abstracts as bsc_dcc_abstracts

import lxgui.core as gui_core
# maya
from ...core.wrap import *

from ... import core as mya_core
# maya dcc objects
from . import utility as mya_dcc_obj_utility

from . import node_for_dag as mya_dcc_obj_node_for_dag


class MeshComponent(bsc_dcc_abstracts.AbsGuiExtraDef):
    PATHSEP = '.'
    TYPE_DICT = {
        'f': 'face',
        'e': 'edge',
        'vtx': 'vertex'
    }

    def __init__(self, obj, name):
        self._obj = obj
        self._name = name
        keyword = self.name.split('[')[0]
        self._type = self.TYPE_DICT.get(keyword)

    @property
    def object(self):
        return self._obj

    def get_type(self):
        return self._type

    type = property(get_type)

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self.PATHSEP.join(
            [self.object.path, self.name]
        )

    @property
    def icon(self):
        return gui_core.GuiIcon.get('obj/{}'.format(self.get_type()))

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()


class Component(bsc_dcc_abstracts.AbsGuiExtraDef):
    PATHSEP = '.'
    TYPE_DICT = {
        'f': 'face',
        'e': 'edge',
        'vtx': 'vertex'
    }

    def __init__(self, path):
        self._path = path
        self._name = self._path.split('.')[-1]
        keyword = self.name.split('[')[0]
        self._type = self.TYPE_DICT.get(keyword)

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def icon(self):
        return gui_core.GuiIcon.get('obj/{}'.format(self.type))

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()


class Mesh(mya_dcc_obj_node_for_dag.Shape):
    COMPONENT_CLS = MeshComponent
    DCC_PORT_CLS = mya_dcc_obj_utility.Port

    def __init__(self, path):
        super(Mesh, self).__init__(path)

    @staticmethod
    def _to_int_array_reduce(array):
        lis = []
        #
        maximum, minimum = max(array), min(array)
        #
        start, end = None, None
        count = len(array)
        index = 0
        #
        array.sort()
        for seq in array:
            if index > 0:
                pre = array[index-1]
            else:
                pre = None
            #
            if index < (count-1):
                nex = array[index+1]
            else:
                nex = None
            #
            if pre is None and nex is not None:
                start = minimum
                if seq-nex != -1:
                    lis.append(start)
            elif pre is not None and nex is None:
                end = maximum
                if seq-pre == 1:
                    lis.append((start, end))
                else:
                    lis.append(end)
            elif pre is not None and nex is not None:
                if seq-pre != 1 and seq-nex != -1:
                    lis.append(seq)
                elif seq-pre == 1 and seq-nex != -1:
                    end = seq
                    lis.append((start, end))
                elif seq-pre != 1 and seq-nex == -1:
                    start = seq
            #
            index += 1
        #
        return lis

    @classmethod
    def _get_comp_names_(cls, indices, comp_key):
        lis = []
        if indices:
            reduce_ids = cls._to_int_array_reduce(indices)
            if len(reduce_ids) == 1:
                if isinstance(reduce_ids[0], tuple):
                    return ['{}[{}:{}]'.format(comp_key, *reduce_ids[0])]
            for i in reduce_ids:
                if isinstance(i, int):
                    lis.append('{}[{}]'.format(comp_key, i))
                elif isinstance(i, tuple):
                    lis.append('{}[{}:{}]'.format(comp_key, *i))
        #
        return lis

    @classmethod
    def _get_face_comp_names_(cls, indices):
        return cls._get_comp_names_(indices, 'f')

    @classmethod
    def _get_edge_comp_names_(cls, indices):
        return cls._get_comp_names_(indices, 'e')

    @classmethod
    def _get_vertex_comp_names_(cls, indices):
        return cls._get_comp_names_(indices, 'vtx')

    def get_component(self, cmp_name):
        return self.COMPONENT_CLS(
            self, cmp_name
        )

    # normal locked
    def get_vertex_normal_locked_comp_names(self):
        index_list = []
        dag_path = om2.MGlobal.getSelectionListByName(self.path).getDagPath(0)
        m2_mesh = om2.MFnMesh(dag_path)
        for vertexId in xrange(m2_mesh.numVertices):
            if m2_mesh.isNormalLocked(vertexId):
                index_list.append(vertexId)
        return self._get_vertex_comp_names_(index_list)

    # topology

    @mya_core.MyaModifier.undo_debug_run
    def get_face_zero_area_comp_names(self):
        pre_selection_paths = cmds.ls(selection=1, long=1) or []
        #
        cmds.select(self.path)
        #
        mini_value = .0
        maxi_value = .00001
        cmds.polySelectConstraint(mode=3, type=8, geometricarea=1, geometricareabound=(mini_value, maxi_value))
        cmds.polySelectConstraint(mode=0, type=8, geometricarea=0)
        #
        _ = cmds.ls(selection=1, long=1) or []
        if pre_selection_paths:
            cmds.select(pre_selection_paths)
        else:
            cmds.select(clear=1)
        return [i.split(self.COMPONENT_CLS.PATHSEP)[-1] for i in _]

    @mya_core.MyaModifier.undo_debug_run
    def get_edge_zero_length_comp_names(self):
        pre_selection_paths = cmds.ls(selection=1, long=1) or []
        #
        cmds.select(self.path)
        #
        mini_value = .0
        maxi_value = .00001
        cmds.polySelectConstraint(mode=3, type=0x8000, length=1, lengthbound=(mini_value, maxi_value))
        cmds.polySelectConstraint(mode=0, type=0x8000, length=0)
        #
        _ = cmds.ls(selection=1, long=1) or []
        if pre_selection_paths:
            cmds.select(pre_selection_paths)
        else:
            cmds.select(clear=1)
        return [i.split(self.COMPONENT_CLS.PATHSEP)[-1] for i in _]

    @mya_core.MyaModifier.undo_debug_run
    def get_face_n_side_comp_names(self):
        pre_selection_paths = cmds.ls(selection=1, long=1) or []
        #
        cmds.select(self.path)
        #
        cmds.polySelectConstraint(mode=3, type=8, size=3)
        cmds.polySelectConstraint(mode=0, type=8, size=0)
        #
        _ = cmds.ls(selection=1, long=1) or []
        if pre_selection_paths:
            cmds.select(pre_selection_paths)
        else:
            cmds.select(clear=1)
        return [i.split(self.COMPONENT_CLS.PATHSEP)[-1] for i in _]

    @mya_core.MyaModifier.undo_debug_run
    def get_face_non_triangulable_comp_names(self):
        pre_selection_paths = cmds.ls(selection=1, long=1) or []
        #
        cmds.select(self.path)
        #
        cmds.polySelectConstraint(mode=3, type=8, topology=1)
        cmds.polySelectConstraint(mode=0, type=8, topology=0)
        #
        _ = cmds.ls(selection=1, long=1) or []
        if pre_selection_paths:
            cmds.select(pre_selection_paths)
        else:
            cmds.select(clear=1)
        return [i.split(self.COMPONENT_CLS.PATHSEP)[-1] for i in _]

    @mya_core.MyaModifier.undo_debug_run
    def get_face_holed_comp_names(self):
        pre_selection_paths = cmds.ls(selection=1, long=1) or []
        #
        cmds.select(self.path)
        #
        cmds.polySelectConstraint(mode=3, type=8, holes=1)
        cmds.polySelectConstraint(mode=0, type=8, holes=0)
        #
        _ = cmds.ls(selection=1, long=1) or []
        if pre_selection_paths:
            cmds.select(pre_selection_paths)
        else:
            cmds.select(clear=1)
        return [i.split(self.COMPONENT_CLS.PATHSEP)[-1] for i in _]

    @mya_core.MyaModifier.undo_debug_run
    def get_face_lamina_comp_names(self):
        pre_selection_paths = cmds.ls(selection=1, long=1) or []
        #
        cmds.select(self.path)
        #
        cmds.polySelectConstraint(mode=3, type=8, topology=2)
        cmds.polySelectConstraint(mode=0, type=8, topology=0)
        #
        _ = cmds.ls(selection=1, long=1) or []
        if pre_selection_paths:
            cmds.select(pre_selection_paths)
        else:
            cmds.select(clear=1)
        return [i.split(self.COMPONENT_CLS.PATHSEP)[-1] for i in _]

    @classmethod
    def _get_mesh_open_edge_indices_(cls, path, round_count=8):
        lis_ = []
        #
        border_edge_indices = []
        edge_coincide_dic = {}
        om2_mesh_edge_itr = om2.MItMeshEdge(om2.MGlobal.getSelectionListByName(path).getDagPath(0))
        edge_indices = range(om2_mesh_edge_itr.count())
        for edge_index in edge_indices:
            om2_mesh_edge_itr.setIndex(edge_index)
            if om2_mesh_edge_itr.onBoundary() is True:
                border_edge_indices.append(edge_index)
                #
                point_key_lis = []
                for j in range(2):
                    point = om2_mesh_edge_itr.point(j)
                    x, y, z = round(point.x, round_count), round(point.y, round_count), round(point.z, round_count)
                    point_key_lis.append((x, y, z))
                #
                point_key_lis.sort()
                #
                edge_coincide_dic.setdefault(tuple(point_key_lis), []).append(edge_index)
        #
        for k, v in edge_coincide_dic.items():
            if len(v) > 1:
                for j in v:
                    lis_.append(j)
        #
        for j in border_edge_indices:
            if j not in lis_:
                pass
        #
        return lis_

    # open-edge
    def get_edge_open_comp_names(self):
        _ = self._get_mesh_open_edge_indices_(self.path)
        return self._get_edge_comp_names_(_)

    # non-manifold
    def get_edge_non_manifold_comp_names(self):
        _ = cmds.polyInfo(self.path, nonManifoldEdges=1) or []
        return [i.split(self.COMPONENT_CLS.PATHSEP)[-1] for i in _]

    #
    def get_vertex_non_manifold_comp_names(self):
        _ = cmds.polyInfo(self.path, nonManifoldVertices=1) or []
        return [i.split(self.COMPONENT_CLS.PATHSEP)[-1] for i in _]

    # map
    @mya_core.MyaModifier.undo_debug_run
    def get_map_face_non_uv_comp_names(self):
        pre_selection_paths = cmds.ls(selection=1, long=1) or []
        #
        cmds.select(self.path)
        #
        cmds.polySelectConstraint(mode=3, type=8, textured=2)
        cmds.polySelectConstraint(mode=0, type=8, textured=0)
        #
        _ = cmds.ls(selection=1, long=1) or []
        if pre_selection_paths:
            cmds.select(pre_selection_paths)
        else:
            cmds.select(clear=1)
        return [i.split(self.COMPONENT_CLS.PATHSEP)[-1] for i in _]

    @mya_core.MyaModifier.undo_debug_run
    def get_map_face_zero_area_comp_names(self):
        pre_selection_paths = cmds.ls(selection=1, long=1) or []
        #
        cmds.select(self.path)
        #
        mini_value = .0
        # maxi value must set -1
        maxi_value = .00001
        cmds.polySelectConstraint(mode=3, type=8, geometricarea=1, geometricareabound=(0.0, 1000000.0))
        cmds.polySelectConstraint(mode=3, type=8, texturedarea=1, texturedareabound=(mini_value, maxi_value))
        cmds.polySelectConstraint(mode=0, type=8, texturedarea=0, geometricarea=0)
        #
        _ = cmds.ls(selection=1, long=1) or []
        if pre_selection_paths:
            cmds.select(pre_selection_paths)
        else:
            cmds.select(clear=1)
        return [i.split(self.COMPONENT_CLS.PATHSEP)[-1] for i in _]

    #
    def get_display_smooth_iterations(self):
        return self.get_port('displaySmoothMesh').get()

    def set_uv_maps_transfer_to(self, tgt_obj_path, clear_history=False):
        src_obj_path = self.path
        _ = cmds.transferAttributes(
            src_obj_path, tgt_obj_path, transferUVs=2
        )
        if clear_history is True:
            cmds.delete(tgt_obj_path, constructionHistory=1)
        #
        bsc_log.Log.trace_method_result(
            'mesh-uv-transfer',
            u'obj="{}" > "{}"'.format(src_obj_path, tgt_obj_path)
        )

    def set_box_create(self, division):
        if self.get_is_exists() is False:
            _ = cmds.polyCube(
                w=10, h=10, d=10,
                sw=division, sh=division, sd=division
            )
            if _:
                box = _[0]
                obj = self.__class__(box)
                transform = obj.transform
                transform.set_rename(self.transform.name)
                transform._update_path_()
                transform.parent_to_path(self.transform.get_parent_path())

    def get_visible(self):
        return self.get_port('visibility').get()

    def set_visible(self, boolean):
        self.get_port('visibility').set(boolean)


class Curve(mya_dcc_obj_node_for_dag.Shape):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port

    def __init__(self, path):
        super(Curve, self).__init__(path)


class Geometry(mya_dcc_obj_node_for_dag.Shape):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port

    def __init__(self, path):
        super(Geometry, self).__init__(path)


class XgenPalette(mya_dcc_obj_node_for_dag.Shape):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port

    def __init__(self, path):
        super(XgenPalette, self).__init__(path)


class XgenSplineGuide(mya_dcc_obj_node_for_dag.Shape):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port

    def __init__(self, path):
        super(XgenSplineGuide, self).__init__(path)
