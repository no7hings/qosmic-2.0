# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class MeshReduce(object):

    @classmethod
    def reduce_off(cls, path, percentage):
        cmds.polyReduce(
            path,
            version=1,
            termination=0,
            percentage=percentage,
            symmetryPlaneX=0,
            symmetryPlaneY=1,
            symmetryPlaneZ=0,
            symmetryPlaneW=0,
            keepQuadsWeight=0,
            vertexCount=0,
            triangleCount=0,
            sharpness=0,
            keepColorBorder=0,
            keepFaceGroupBorder=0,
            keepHardEdge=1,
            keepCreaseEdge=1,
            keepBorderWeight=0.5,
            keepMapBorderWeight=1,
            keepColorBorderWeight=0.5,
            keepFaceGroupBorderWeight=0.5,
            keepHardEdgeWeight=0.5,
            keepCreaseEdgeWeight=0.5,
            useVirtualSymmetry=0,
            symmetryTolerance=0.01,
            vertexMapName='',
            replaceOriginal=1,
            cachingReduce=1,
            constructionHistory=0
        )
        cmds.polyTriangulate(path, constructionHistory=0)
        cmds.delete(path, constructionHistory=1)
        cmds.select(clear=1)
