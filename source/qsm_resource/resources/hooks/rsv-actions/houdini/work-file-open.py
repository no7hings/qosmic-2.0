# coding:utf-8
import lxhoudini.dcc.objects as hou_dcc_objects
#
file_path = session.rsv_unit.get_result(
    version='latest'
)
if file_path:
    hou_dcc_objects.Scene.set_file_open_with_dialog(file_path)
