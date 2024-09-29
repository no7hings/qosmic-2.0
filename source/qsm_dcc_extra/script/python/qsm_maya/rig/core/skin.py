# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core


class MeshSkinOpt(object):
    """
    smooth skin
    """
    def __init__(self, path_or_name):
        """
        use transform
        """
        if _mya_core.Node.is_exists(path_or_name) is False:
            raise RuntimeError()

        if _mya_core.Node.is_transform(path_or_name):
            self._transform_path = _mya_core.DagNode.to_path(path_or_name)
            _ = _mya_core.Transform.get_shape(path_or_name)
            if _mya_core.Node.is_mesh(_) is True:
                self._shape_path = _
            else:
                raise RuntimeError()
        elif _mya_core.Node.is_mesh(path_or_name):
            self._shape_path = _mya_core.DagNode.to_path(path_or_name)
            self._transform_path = _mya_core.Shape.get_transform(path_or_name)
        else:
            raise RuntimeError()

    def is_valid(self):
        return bool(self.get_skin_cluster())

    def get_skin_cluster(self):
        history = cmds.listHistory(self._transform_path)
        _ = cmds.ls(history, type='skinCluster') or []
        if _:
            return _[0]
        return None

    def get_joints(self):
        _ = self.get_skin_cluster()
        if _:
            return cmds.skinCluster(_, query=True, influence=True) or []
        return []

    def get_weights(self):
        skin_cluster = self.get_skin_cluster()
        if not skin_cluster:
            return {}

        weight_dict = {}

        vertex_count = cmds.polyEvaluate(self._shape_path, vertex=True)
        if vertex_count > 0:
            for i_vtx_id in range(vertex_count):
                i_vtx = "%s.vtx[%d]" % (self._transform_path, i_vtx_id)
                i_weights = cmds.skinPercent(skin_cluster, i_vtx, query=True, value=True)
                weight_dict[i_vtx] = i_weights

        return weight_dict

    def get_deficiency_weight_vertex_indices(self):
        skin_cluster = self.get_skin_cluster()
        if not skin_cluster:
            return {}

        list_ = []

        vertex_count = cmds.polyEvaluate(self._shape_path, vertex=True)
        if vertex_count > 0:
            for i_vtx_id in range(vertex_count):
                i_vtx = "%s.vtx[%d]"%(self._transform_path, i_vtx_id)
                i_weights = cmds.skinPercent(skin_cluster, i_vtx, query=True, value=True)
                if abs(sum(i_weights) - 1.0) > 1e-5:
                    list_.append(i_vtx_id)
        return list_

    @classmethod
    def test(cls):
        _ = cls('pSphere1')
        # print _.is_valid()
        # print _.get_skin_cluster()
        # print _.get_joints()
        print _.get_deficiency_weight_vertex_indices()
