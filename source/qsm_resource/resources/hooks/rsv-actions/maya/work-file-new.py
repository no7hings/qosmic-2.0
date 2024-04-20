# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects

import lxmaya.dcc.objects as mya_dcc_objects


def post_method_fnc_(file_path_):
    pass


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
    mya_dcc_objects.Scene.new_file_with_dialog(
        file_path,
        post_method_fnc_
    )

