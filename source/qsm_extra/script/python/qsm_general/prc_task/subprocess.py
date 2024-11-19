# coding:utf-8


class SubprocessTaskSubmit:
    @classmethod
    def execute_one(
        cls,
        task_name, cmd_script, completed_fnc,
        window_title, window_title_chs,
        tip=None, tip_chs=None
    ):
        import lxgui.proxy.widgets as gui_prx_widgets

        task_window = gui_prx_widgets.PrxSprcTaskWindow()
        if task_window._language == 'chs':
            task_window.set_window_title(window_title_chs)
            task_window.set_tip(
                tip_chs or (
                    '正在运行{}任务，请耐心等待；\n'
                    '这个过程可能会让MAYA前台操作产生些许卡顿，但是依然可以继续进行制作；\n'
                    '如需要终止任务，请点击“关闭”。'
                ).format(window_title_chs)
            )
        else:
            task_window.set_window_title(window_title)
            task_window.set_tip(
                tip or (
                    '{} Task is running, please wait patiently;\n'
                    'This process may cause some lag in MAYA foreground operation, but you can still continue to make;\n'
                    'If you need to terminate the task, please click "Close". '
                ).format(window_title)
            )

        task_window.submit(
            'playblast',
            task_name,
            cmd_script,
            completed_fnc=completed_fnc,
        )

        task_window.show_window_auto(exclusive=False)
