# coding:utf-8
import lxkatana.dcc.objects as ktn_dcc_objects
#
file_path = session.rsv_unit.get_result(
    version='latest'
)
if file_path:
    ktn_dcc_objects.Scene.set_file_open_with_dialog(file_path)
