# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        button = gui_prx_widgets.PrxPressButton()
        self.add_widget(button)
        button.set_name('TEST')
        button.connect_press_clicked_to(self._test)

    def _test(self):
        cmd_script = r'rez-env maya-2020 mtoa qsm_dcc_main -- mayabatch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"option_hook_key=dcc-process/maya-cache-process&method=mesh_count_generate&method_option=5DA2DA2DC08299EE68F3A28F7BD1AF78\\\")\")"'
        # cmd_script = r'rez-env maya-2020 mtoa qsm_dcc_main -- mayabatch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"option_hook_key=dcc-process/maya-cache-process&method=mesh_count_generate&method_option=E87227F21ADA6910DB7866EBA4C314F7\\\")\")"'

        task_window = gui_prx_widgets.PrxSprcTaskWindow()

        task_window.show_window_auto(exclusive=False)
        task_window.submit(
            'TEST',
            'test-0',
            cmd_script,
            check_memory_prc_name='mayabatch.exe'
        )


if __name__ == '__main__':
    import sys

    import os

    from lxgui.qt.core import wrap

    os.environ['QSM_UI_LANGUAGE'] = 'chs'

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()

    sys.exit(app.exec_())
