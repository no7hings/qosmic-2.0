# coding:utf-8
import functools

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_lazy.montage.scripts as qsm_lzy_mtg_scripts


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    @staticmethod
    def _start_delay(window, scr_stage_key, src_entities):
        process_args = []
        for i_scr_entity in src_entities:
            i_scr_entity_path = i_scr_entity.path
            i_opt = qsm_lzy_mtg_scripts.StlConvertionOpt(
                scr_stage_key, i_scr_entity_path
            )
            i_args = i_opt.generate_args()
            if i_args:
                i_task_name, i_cmd_script, i_cache_file_path = i_args
                if i_cmd_script is not None:
                    process_args.append(
                        (i_task_name, i_cmd_script, i_opt)
                    )
                else:
                    pass

        if process_args:
            window.show_window_auto(exclusive=False)
            for i_args in process_args:
                i_task_name, i_cmd_script, i_opt = i_args
                window.submit(
                    i_task_name,
                    i_cmd_script,
                    completed_fnc=functools.partial(i_opt.register)
                )
        else:
            window.close_window()

    def execute(self):
        window = self._session.find_window()
        if window is not None:
            page = window.gui_get_current_page()
            node_opt = page._gui_node_opt
            scr_stage_key = self._option_opt.get('stage_key')

            src_entities = node_opt.gui_get_checked_or_selected_scr_entities()
            if src_entities:
                window = gui_prx_widgets.PrxSubprocessWindow()
                if window._language == 'chs':
                    window.set_window_title('动作生成（用于拼接）')
                    window.set_tip(
                        '正在运行动作生成程序，请耐心等待；\n'
                        '如需要终止任务，请点击“关闭”。'
                    )
                else:
                    window.set_window_title('Motion Convert')

                window.run_fnc_delay(
                    functools.partial(
                        self._start_delay,
                        window, scr_stage_key, src_entities
                    ),
                    500
                )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
