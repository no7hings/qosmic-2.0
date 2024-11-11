# coding:utf-8
import functools

from qsm_lazy_tool.workspace.gui.abstracts import unit_for_task_release as _abs_unit_for_task_publish

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_general.process as qsm_dcc_process

import qsm_maya.core as qsm_mya_core


class GuiNodeOptForCfxRigRelease(_abs_unit_for_task_publish.AbsGuiNodeOptForTaskRelease):
    def on_dcc_select_node(self):
        selected_items = self._qt_tree_widget._view_model.get_selected_items()
        if selected_items:
            list_ = []
            for i in selected_items:
                i_node = i._item_model.get_assign_data('node')
                if i_node:
                    list_.append(i_node)

            qsm_mya_core.Selection.set(list_)
        else:
            qsm_mya_core.Selection.clear()

    def __init__(self, *args, **kwargs):
        super(GuiNodeOptForCfxRigRelease, self).__init__(*args, **kwargs)

        self._qt_tree_widget._view.item_select_changed.connect(
            self.on_dcc_select_node
        )

    def do_gui_refresh_all(self, force=False):
        pass


class PrxToolsetForCfxRigRelease(_abs_unit_for_task_publish.AbsPrxToolsetForTaskRelease):
    UNIT_KEY = 'cfx_rig'

    GUI_NODE_OPT_CLS = GuiNodeOptForCfxRigRelease

    def _delay_fnc(self, task_window):
        pass

    def on_release(self):
        images = self._prx_options_node.get('images')
        if self._task_release_opt is not None:
            args = self._task_release_opt.release_scene_src(images=images)
            if args:
                release_scene_src_path_new, version_new = args
                method = 'cfx_rig_release'
                cmd_script = qsm_dcc_process.MayaTaskProcess.generate_cmd_script_by_option_dict(
                    method,
                    dict(
                        scene_src=release_scene_src_path_new
                    )
                )

                task_window = gui_prx_widgets.PrxSprcTaskWindow()
                if task_window._language == 'chs':
                    task_window.set_window_title('解算预设发布')
                    task_window.set_tip(
                        '解算预设在后台发布，请耐心等待；\n'
                        '这个过程可能会让MAYA前台操作产生些许卡顿；\n'
                        '如需要终止任务，请点击“关闭”'
                    )
                else:
                    task_window.set_window_title('CFX Rig Release')

                task_window.show_window_auto(exclusive=False)

                task_window.submit(
                    method,
                    '[cfx_rig-release][v{}]'.format(version_new),
                    cmd_script,
                )

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForCfxRigRelease, self).__init__(*args, **kwargs)
