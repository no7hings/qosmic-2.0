# coding:utf-8
import collections

import os

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import fnmatch

import lxgui.proxy.widgets as gui_prx_widgets

y_f = '{}.yml'.format(os.path.splitext(__file__)[0])

c = bsc_storage.StgFileOpt(y_f).set_read()


class TestWindow(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self.set_definition_window_size([480, 480])
        self._test_()

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        return fnmatch.filter(
            ['test'], '*{}*'.format(args[0])
        )

    def _test_(self):
        filter_bar = gui_prx_widgets.PrxFilterBar()
        self.add_widget(filter_bar)

        filter_bar.set_completion_gain_fnc(self._value_completion_gain_fnc_)
        filter_bar.set_tip('test...')
        filter_bar.set_history_key('keyword-filter-test')

        guide_bar = gui_prx_widgets.PrxGuideBar()
        self.add_widget(guide_bar)
        # guide_bar.set_types(
        #     ['category_group', 'category', 'type']
        # )
        guide_bar.set_dict(
            collections.OrderedDict(
                [
                    ('/surface', None),
                    ('/surface/rock', None),
                    ('/surface/rock/clay', None),
                    ('/surface/rock/smooth', None),
                ]
            )
        )
        guide_bar.set_path(
            '/surface/rock'
        )

        tag_bar = gui_prx_widgets.PrxTagBar()
        self.add_widget(tag_bar)


if __name__ == '__main__':

    import sys
    #
    from lxgui.qt.core.wrap import *
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_window_show()
    #
    sys.exit(app.exec_())
