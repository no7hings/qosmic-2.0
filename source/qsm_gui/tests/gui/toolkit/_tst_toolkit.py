# coding:utf-8
import lxgui.qt.toolkit as gui_qt_toolkit

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_screw.core as lnx_scr_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = gui_qt_toolkit.QtToolTabWidget()

        self.add_widget(self._d)

        for i in range(5):
            i_tool_page = gui_qt_toolkit.QtToolPage()
            i_path = '/page_{}'.format(i)
            self._d.model.add_page(i_path, i_tool_page)
            i_tool_page.model.set_label('Page-{}'.format(i))
            i_tool_page.model.set_tool_tip('Test')

            for j in range(5):
                j_tool_group = gui_qt_toolkit.QtToolGroup()
                i_tool_page.model.add_group(j_tool_group)
                j_tool_group.model.set_label('Group-{}-{}'.format(i, j))
                j_tool_group.model.set_column_count(2)

                if j%2:
                    j_tool_group.model.set_expanded(True)

                for k in range(5):
                    k_tool = gui_qt_toolkit.QtTool()
                    j_tool_group.model.add_tool(k_tool)
                    k_tool.model.set_label('Tool-{}-{}-{}'.format(i, j, k))
                    if k%2:
                        k_tool.model.set_menu_data(
                            [
                                ('Test', None, None)
                            ]
                        )


def test():
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 480))
    w.show_window_auto()

    sys.exit(app.exec_())


if __name__ == '__main__':
    # import cProfile
    # import os
    # import pstats
    # file_path = '{}/profile.profile'.format(os.path.dirname(__file__))
    # cProfile.run('test()', file_path)
    #
    # p = pstats.Stats(file_path)
    # p.strip_dirs().sort_stats('time').print_stats(10)
    # print p.get_top_level_stats()
    test()
