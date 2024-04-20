# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._f = qt_widgets.QtBubbleAsChoice(self._qt_widget)
        self._f._setup_()

        # self.add_widget(self._f)
        self._f._set_texts_(
            [
                '/Department/Surface/Python A',
                'Python B',
                'Python C',
                'Python D',
                'Python E',
                'Python F',
                'Python G',
                'Python H',
                'Maya A',
                'Maya B',
                'Maya C',
                'Maya D',
                'Maya E',
                'Maya F',
                'Maya G',
                'Maya H',
                'Katana A',
                'Katana B',
                'Katana C',
                'Katana D',
                'Katana E',
                'Katana F',
                'Katana G',
                'Katana H',
                'Houdini A',
                'Houdini B',
            ]
        )

        self.create_window_action_for(self._f._start_, 'tab')


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.set_window_show()
    #
    sys.exit(app.exec_())
