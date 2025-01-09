# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.dcc.objects as ktn_dcc_objects

wsp = ktn_dcc_objects.AssetWorkspaceOld()

dcc_node = ktn_dcc_objects.Node('master__layer')

dcc_main_node = ktn_dcc_objects.Node('layer_switch')

dcc_backdrop_node = ktn_dcc_objects.Node('layer_switch_backdrop')

d_size = 480, 320

print wsp._set_node_layout_by_backdrop_(

    dcc_node, dcc_main_node, dcc_backdrop_node, d_size
)