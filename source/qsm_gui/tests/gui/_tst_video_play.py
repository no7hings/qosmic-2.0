# coding:utf-8
import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxbasic.cv.core as bsc_cv_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = gui_qt_widgets.QtVideoPlayWidget(self._qt_widget)
        self.add_widget(self._d)
        self._d._set_video_path_(
            'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.mov'
        )


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((320, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
