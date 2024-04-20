# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects
#
import lxhoudini.dcc.objects as hou_dcc_objects


def post_method_fnc_(file_path_):
    # noinspection PyUnresolvedReferences
    import hou
    f = bsc_dcc_objects.StgFile(file_path_)
    cmd = "set -g {0}={1}".format('HIP', f.directory.path)
    hou.hscript(cmd)


rsv_task = session.rsv_obj
#
rsv_unit = rsv_task.get_rsv_unit(
    keyword='{branch}-source-maya-scene-src-file'.format(
        **session.variants
    )
)
#
file_path = rsv_unit.get_result(
    version='new'
)
file_ = bsc_dcc_objects.StgFile(file_path)
if file_.get_is_exists() is False:
    hou_dcc_objects.Scene.new_file_with_dialog(
        file_path,
        post_method_fnc_
    )
