# coding:utf-8
import functools

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_lazy_resource.scripts as lzy_rsc_scripts


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    @staticmethod
    def _start_delay(window, task_window, scr_stage_name, scr_entities):
        process_args = []
        with window.gui_progressing(maximum=len(scr_entities)) as g_p:
            for i_scr_entity in scr_entities:
                i_scr_entity_path = i_scr_entity.path
                i_opt = lzy_rsc_scripts.MoCapFbxMotionGenerate(
                    scr_stage_name, i_scr_entity_path
                )
                i_args = i_opt.generate_args()
                if i_args:
                    i_task_name, i_cmd_script = i_args
                    if i_cmd_script is not None:
                        process_args.append(
                            (i_task_name, i_cmd_script, i_opt)
                        )
                    else:
                        i_opt.register()

                g_p.do_update()

        if process_args:
            task_window.show_window_auto(exclusive=False)
            for i_args in process_args:
                i_task_name, i_cmd_script, i_opt = i_args
                task_window.submit(
                    'motion_generate',
                    i_task_name,
                    i_cmd_script,
                    completed_fnc=functools.partial(i_opt.register),
                )
        else:
            task_window.close_window()

    def execute(self):
        window = self._session.find_window()
        if window is not None:
            page = window.gui_get_current_page()
            node_opt = page._gui_node_opt
            scr_stage_name = self._option_opt.get('stage_name')

            scr_entities = node_opt.gui_get_checked_or_selected_scr_entities()
            if scr_entities:
                task_window = gui_prx_widgets.PrxSprcTaskWindow()
                task_window.set_thread_maximum(4)
                if task_window._language == 'chs':
                    task_window.set_window_title('生成动作（MoCap fbx）')
                    task_window.set_tip(
                        '正在生成动作，请耐心等待；\n'
                        '如需要终止任务，请点击“关闭”。'
                    )
                else:
                    task_window.set_window_title('Motion Convert')

                task_window.run_fnc_delay(
                    functools.partial(
                        self._start_delay,
                        window, task_window, scr_stage_name, scr_entities
                    ),
                    500
                )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
