# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxgui.qt.widgets as qt_widgets

import lxgui.qt.widgets.entity.choose_and_completion as m

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_parsor.swap as lnx_prs_swap


class W(gui_prx_widgets.PrxBaseWindow):

    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = m.QtEntityChooseStack()
        self.add_widget(self._d)

        root = lnx_prs_swap.Swap.generate_root()

        name_texts = []
        gui_name_dict = {}
        tag_filter_dict = {}
        keyword_filter_dict = {}

        project = root.project('QSM_TST')
        for i in project.assets():
            i_name = i.name
            name_texts.append(i_name)
            i_gui_name = i.variants.get('entity_gui_name')
            i_gui_name = '测试'
            gui_name_dict[i_name] = i_gui_name
            tag_filter_dict[i_name] = ['All', i.variants['role']]
            keyword_filter_dict[i_name] = [i_name, i_gui_name]

        data = dict(
            type_text='asset',
            name_texts=name_texts,
            gui_name_dict=gui_name_dict,
            tag_filter_dict=tag_filter_dict,
            keyword_filter_dict=keyword_filter_dict
        )

        self._d._load_data(data)
        self._d._resize_current()


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
