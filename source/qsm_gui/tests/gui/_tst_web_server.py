# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.qt.core as gui_qt_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = gui_qt_core.QtWebServerForDcc(self._qt_widget)
        self._d._start_(
            'localhost', 12306
        )

        # self._qt_widget._show_notice_(
        #     # 'playblast is completed do you want to play it?'
        #     'status=normal&message=%E6%8B%8D%E5%B1%8F%E7%BB%93%E6%9D%9F%E4%BA%86%2C+%E6%98%AF%E5%90%A6%E6%89%93%E5%BC%80%E8%A7%86%E9%A2%91%3F&ok_python_script=import+os%3B+os.startfile%28%22Z%3A%2Ftemeporaries%2Fdongchangbao%2Fplayblast_tool%2F%E8%91%A3%E6%98%8C%E5%AE%9D%2Ftest.export.v010.mov%22%29&title=%E9%80%9A%E7%9F%A5'
        # )


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
