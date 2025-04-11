# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxgui.qt.widgets as qt_widgets

import lxgui.qt.widgets.entity.account as m

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_parsor.swap as lnx_prs_swap


class W(gui_prx_widgets.PrxBaseWindow):

    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = m.QtAccountWidget()
        self.add_widget(self._d)
        
        root = lnx_prs_swap.Swap.generate_root()

        self._d._model.load_entity(root.current_user())


def test():
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((720, 480))
    w.show_window_auto()

    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
    # import cProfile
    # import os
    # import pstats
    # file_path = '{}/profile.profile'.format(os.path.dirname(__file__))
    # cProfile.run('test()', file_path)
    #
    # p = pstats.Stats(file_path)
    # p.strip_dirs().sort_stats('time').print_stats(10)
    # # print p.get_top_level_stats()
