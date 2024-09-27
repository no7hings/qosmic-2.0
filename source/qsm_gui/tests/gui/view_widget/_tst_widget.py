# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = qt_widgets.QtTestForFit()
        self.add_widget(self._d)


def test():
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((320, 320))
    w.show_window_auto()

    sys.exit(app.exec_())


if __name__ == '__main__':
    import cProfile
    import os
    import pstats
    file_path = '{}/profile.profile'.format(os.path.dirname(__file__))
    cProfile.run('test()', file_path)

    p = pstats.Stats(file_path)
    p.strip_dirs().sort_stats('time').print_stats(10)
    # print p.get_top_level_stats()
