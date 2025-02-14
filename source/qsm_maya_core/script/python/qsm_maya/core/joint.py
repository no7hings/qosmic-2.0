# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import attribute as _attribute

from . import shape as _shape


class Joint:
    @classmethod
    def find_skin_clusters(cls, path):
        # must connect to influenceColor[*]
        return _attribute.NodeAttribute.get_target_nodes(
            path, 'objectColorRGB', 'skinCluster'
        )

    @classmethod
    def find_influenced_meshes(cls, path):
        skin_clusters = cls.find_skin_clusters(path)
        list_ = []
        for i_skin_cluster in skin_clusters:
            i_geometry_paths = cmds.skinCluster(i_skin_cluster, query=True, geometry=True) or []
            for j_shape_path in i_geometry_paths:
                # check is mesh
                if _shape.Shape.is_mesh_type(j_shape_path) is False:
                    continue

                j_transform_path = _shape.Shape.get_transform(j_shape_path)
                j_vertex_count = cmds.polyEvaluate(j_shape_path, vertex=1)
                if j_vertex_count > 0:
                    has_weight = False
                    for k_vtx_id in range(j_vertex_count):
                        k_vtx = j_transform_path+".vtx[{}]".format(k_vtx_id)
                        k_weights = cmds.skinPercent(
                            i_skin_cluster, k_vtx, query=True, transform=path
                        )
                        if k_weights > 0:
                            has_weight = True
                            break

                    if has_weight is True:
                        list_.append(
                            _shape.Shape.to_path(j_shape_path)
                        )

        return list(set(list_))

