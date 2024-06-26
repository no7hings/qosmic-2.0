# coding:utf-8
import qsm_general.dotfile as gnl_dotfile


ma = gnl_dotfile.MayaAscii(
    'Z:/libraries/lazy-resource/all/maya_cfx/unnamed/maya/unnamed.maya_node_graph.ma'
)

print ma.get_all_nodes()
