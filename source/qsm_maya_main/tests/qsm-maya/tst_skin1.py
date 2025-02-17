# coding:utf-8
import maya.cmds as cmds


def get_influenced_meshes(joint_name):
    # 获取所有的skinCluster节点
    skin_clusters = cmds.ls(type='skinCluster')
    influenced_meshes = []

    for skin_cluster in skin_clusters:
        # 获取skinCluster绑定的所有骨骼
        joints = cmds.skinCluster(skin_cluster, query=True, influence=True)
        if joint_name in joints:
            # 获取受影响的Mesh
            meshes = cmds.skinCluster(skin_cluster, query=True, geometry=True)
            influenced_meshes.extend(meshes)

    return list(set(influenced_meshes))


# 使用示例：获取受名为"joint1"的骨骼影响的Mesh
joint_name = "joint1"
meshes = get_influenced_meshes(joint_name)
print("Influenced meshes by {}: {}".format(joint_name, meshes))
