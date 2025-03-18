# coding:utf-8
import json

import qsm_general.dotfile as qsm_gnl_dotfile


ma = qsm_gnl_dotfile.MayaAscii(
    'X:/QSM_TST/A001/A001_001/动画/通过文件/A001_001_002.ma'
)

print(ma.get_modify_time())

print(ma.get_nodes())

print(ma.get_references())

print(ma.get_reference_files())

print(ma.get_fps())

print(ma.get_frame_range())

print(json.dumps(ma.get_reference_files()))

# print ma.get_node_dict()
