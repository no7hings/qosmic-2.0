# coding:utf-8
import trimesh

import numpy as np

from trimesh.exchange import obj


# _ = obj.load_obj(
#     open('/data/e/workspace/lynxi/test/maya/vertex-color/test_mesh.obj', 'rb')
# )
#
# print _


mesh = trimesh.load_mesh(
    '/data/e/workspace/lynxi/test/maya/vertex-color/test_mesh.obj'
)


point = np.array([1.4, 0.5, -0.4])

direction = np.array([0, 0, -1])

hint = mesh.ray.intersects_location(point, direction)

print hint
