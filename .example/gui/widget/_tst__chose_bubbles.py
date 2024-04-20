# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets

import lxgui.qt.core as gui_qt_core


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self.create_window_action_for(self._test, 'tab')

    def _test(self):

        b = qt_widgets.QtBubbleAsChoose(gui_qt_core.GuiQtDcc.get_qt_main_window())
        b._set_tips_('choose a scheme for build texture')
        b._set_texts_(['material', 'shader', 'group'])

        b._do_popup_start_()

        print b._get_result_()


if __name__ == '__main__':
    import sys

    from lxgui.qt import wrap
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.set_window_show()
    #
    sys.exit(app.exec_())
