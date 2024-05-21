# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets

import lxgui.qt.core as gui_qt_core


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = gui_qt_core.QtWebSocketServer(self._qt_widget)

        self._qt_widget._show_message_(
            # 'playblast is completed do you want to play it?'
            '拍屏结束了，是否播放文件'
        )


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
