# coding:utf-8
import qsm_maya.core as qsm_mya_core

import qsm_maya.adv as qsm_mya_adv


class FileDragAction:
    @classmethod
    def reference_one(cls, file_path, auto_namespace=False, move_to_mouse=False):
        pos = qsm_mya_core.ViewportProject.compute_point_at_mouse()
        namespace = qsm_mya_core.SceneFile.reference_file(file_path, auto_namespace=auto_namespace)

        if namespace and qsm_mya_adv.AdvOpt.check_is_valid(namespace):
            adv_opt = qsm_mya_adv.AdvOpt(namespace)
            if move_to_mouse is True:
                if pos:
                    adv_opt.move_to(pos)
            adv_opt.select_main()
    
    @classmethod
    def import_one(cls, file_path, auto_namespace=False, move_to_mouse=False):
        pos = qsm_mya_core.ViewportProject.compute_point_at_mouse()
        namespace = qsm_mya_core.SceneFile.import_scene(file_path, auto_namespace=auto_namespace)

        if namespace and qsm_mya_adv.AdvOpt.check_is_valid(namespace):
            adv_opt = qsm_mya_adv.AdvOpt(namespace)
            if move_to_mouse is True:
                if pos:
                    adv_opt.move_to(pos)
            adv_opt.select_main()


