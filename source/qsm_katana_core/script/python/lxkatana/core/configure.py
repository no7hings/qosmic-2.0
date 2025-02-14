# coding:utf-8
import os


class KtnBase(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))

    DATA_ROOT = '{}/.data'.format(ROOT)


class KtnNodeTypes(object):
    Mesh = 'subdmesh'
    Curve = 'curves'

    GEOMETRY_TYPES = [
        'subdmesh',
        'renderer procedural',
        'pointcloud',
        'polymesh',
        'curves'
    ]
