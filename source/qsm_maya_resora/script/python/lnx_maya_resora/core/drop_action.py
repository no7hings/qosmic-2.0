# coding:utf-8
import lxgui.core as gui_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.adv as qsm_mya_adv


class SceneDropAction:
    @classmethod
    def reference_one(cls, file_path, auto_namespace=False, move_to_mouse=False, pos=None):
        namespace = qsm_mya_core.SceneFile.reference_file(file_path, auto_namespace=auto_namespace)
        if namespace and qsm_mya_adv.AdvOpt.check_is_valid(namespace):
            adv_opt = qsm_mya_adv.AdvOpt(namespace)
            if move_to_mouse is True:
                if pos:
                    adv_opt.move_to(pos)
            adv_opt.select_main()
    
    @classmethod
    def import_one(cls, file_path, auto_namespace=False, move_to_mouse=False, pos=None):
        namespace = qsm_mya_core.SceneFile.import_scene(file_path, auto_namespace=auto_namespace)
        if namespace and qsm_mya_adv.AdvOpt.check_is_valid(namespace):
            adv_opt = qsm_mya_adv.AdvOpt(namespace)
            if move_to_mouse is True:
                if pos:
                    adv_opt.move_to(pos)
            adv_opt.select_main()

    @classmethod
    def load_one(cls, file_path, auto_namespace=False, move_to_mouse=False):
        w = gui_core.GuiDialogForChooseAsBubble.create(
            [
                'import',
                'reference',
                'open'
            ],
            'load maya scene, choose one scheme to continue'
        )
        scheme = w.get_result()
        if scheme:
            pos = qsm_mya_core.ViewportProject.compute_point_at_mouse()
            if scheme == 'reference':
                cls.reference_one(file_path, auto_namespace=auto_namespace, move_to_mouse=move_to_mouse, pos=pos)
            elif scheme == 'import':
                cls.import_one(file_path, auto_namespace=auto_namespace, move_to_mouse=move_to_mouse, pos=pos)
            elif scheme == 'open':
                qsm_mya_core.SceneFile.open_with_dialog(file_path)


class VideoDropAction:
    @classmethod
    def reference_one(cls, file_path):
        pass

    @classmethod
    def import_one(cls, file_path):
        pass

    @classmethod
    def load_one(cls, file_path):
        pass



