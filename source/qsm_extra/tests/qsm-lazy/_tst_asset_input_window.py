# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets

import qsm_lazy.gui.proxy.widgets as w

import os


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        btn = gui_prx_widgets.PrxPressButton()
        self.add_widget(btn)
        btn.set_name('Test')

        btn.connect_press_clicked_to(self.test)

    def test(self):
        wgt = w.PrxWindowForAssetInput()
        wgt.show_window_auto(size=(480, 96))

        if wgt.get_result() is True:
            print(wgt.get_entity())


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    os.environ['QSM_UI_LANGUAGE'] = 'chs'

    app = wrap.QtWidgets.QApplication(sys.argv)

    window = W()
    window.set_definition_window_size((720, 480))
    window.show_window_auto()

    sys.exit(app.exec_())
