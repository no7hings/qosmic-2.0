# coding:utf-8
import qsm_general.dotfile as qsm_gnl_dotfile


ma = qsm_gnl_dotfile.MayaAscii(
    'X:/QSM_TST/A001/A001_001/动画/通过文件/A001_001_003.ma'
)

print ma.get_modify_time()

print ma.get_nodes()

print ma.get_references()

print ma.get_fps()

print ma.get_frame_range()

# print ma.get_node_dict()
