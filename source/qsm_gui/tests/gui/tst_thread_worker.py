# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.scripts as prx_scripts


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = prx_widgets.PrxPressButton(self._qt_widget)
        self._d.set_name('Test')

        self.add_widget(self._d)

        create_cmds = [
            r'rez-env python27 -- python -c "import time; time.sleep(5); print \"{}\""'.format(x) for x in range(15)
        ]

        mtd = prx_scripts.GuiThreadWorker(self)
        mtd.execute(self._d, create_cmds)


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.set_window_show()
    #
    sys.exit(app.exec_())
