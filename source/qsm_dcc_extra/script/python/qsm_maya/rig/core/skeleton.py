# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core


class Joint(object):
    @classmethod
    def find_skin_clusters(cls, path):
        return _mya_core.NodeConnection.find_all_target_nodes(
            path, 'skinCluster'
        )

    @classmethod
    def find_influenced_meshes(cls, path):
        skin_clusters = cls.find_skin_clusters(path)
        list_ = []
        for i_skin_cluster in skin_clusters:
            i_mesh_paths = cmds.skinCluster(i_skin_cluster, query=True, geometry=True)
            for j_shape_path in i_mesh_paths:
                j_transform_path = _mya_core.Shape.get_transform(j_shape_path)
                j_vertex_count = cmds.polyEvaluate(j_shape_path, vertex=1)
                has_weight = False
                for k in range(j_vertex_count):
                    k_vertex = j_transform_path+".vtx[{}]".format(k)
                    k_weights = cmds.skinPercent(
                        i_skin_cluster, k_vertex, query=True, transform=path
                    )
                    if k_weights > 0:
                        has_weight = True
                        break

                if has_weight is True:
                    list_.append(
                        _mya_core.DagNode.to_path(j_shape_path)
                    )

        return list(set(list_))

