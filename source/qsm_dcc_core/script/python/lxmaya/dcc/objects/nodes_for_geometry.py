# coding:utf-8
# maya
from ... import abstracts as mya_abstracts

from . import node_for_geometry as mya_dcc_obj_node_for_geometry


class Meshes(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = [
        'mesh',
    ]

    DCC_NODE_CLS = mya_dcc_obj_node_for_geometry.Mesh

    def __init__(self, *args):
        super(Meshes, self).__init__(*args)
