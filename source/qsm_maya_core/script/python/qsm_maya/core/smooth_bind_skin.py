# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class SmoothBindSkin:
    @classmethod
    def create(cls, joints, meshes, **kwargs):
        kwargs_over = dict(
            # This flag sets the binding method.
            # 0 - Closest distance between a joint and a point of the geometry.
            # 1 - Closest distance between a joint, considering the skeleton hierarchy, and a point of the geometry.
            # 2 - Surface heat map diffusion.
            # 3 - Geodesic voxel binding. geomBind command must be called after creating a skinCluster with this method.
            bindMethod=0,
            # This flag set the skinning method.
            # 0 - classical linear skinning (default).
            # 1 - dual quaternion (volume preserving),
            # 2 - a weighted blend between the two.
            skinMethod=0,
            normalizeWeights=1,
            maximumInfluences=4,
            obeyMaxInfluences=1,
            dropoffRate=4.0,
            removeUnusedInfluence=1,
            toSelectedBones=1,
            # Tells the command to not deform objects on the current selection list
            ignoreSelected=1,
            # Used to specify the name of the node being created.
            # name='mySkinCluster'
        )
        kwargs_over.update(kwargs)
        cmds.skinCluster(*joints+meshes, **kwargs)
