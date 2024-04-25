# coding:utf-8
import lxgeneral.dcc.objects as gnl_dcc_objects

import lxkatana.dcc.objects as ktn_dcc_objects


def post_method_fnc_(file_path_):
    import lxkatana.fnc.objects as ktn_fnc_objects

    ktn_fnc_objects.FncCreatorForLookWorkspaceOld().set_run()


file_path = session.rsv_unit.get_result(
    version='new'
)
file_ = gnl_dcc_objects.StgFile(file_path)
if file_.get_is_exists() is False:
    ktn_dcc_objects.Scene.new_file_with_dialog(
        file_path,
        post_method_fnc_
    )
