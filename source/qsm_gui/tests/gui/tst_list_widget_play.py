# coding:utf-8
import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxbasic.cv.core as bsc_cv_core

import lxbasic.storage as bsc_storage


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        s = gui_prx_widgets.PrxVSplitter()
        self.add_widget(s)

        self._prx_list_view = gui_prx_widgets.PrxListView()
        s.add_widget(self._prx_list_view)
        self._prx_list_view.set_item_event_override_flag(True)

        for i in range(100):
            i = 'Z:/libraries/lazy-resource/all/motion_test/ceshi_jichu_paobu_nan_anim/preview/images/image.%04d.jpg'
            i_qt_item = self._prx_list_view.create_item_()
            i_qt_item_widget = gui_qt_widgets.QtItemWidgetForList()
            self._prx_list_view.assign_item_widget(i_qt_item, i_qt_item_widget)

            i_qt_item_widget._set_image_path_(
                'Z:/libraries/lazy-resource/all/motion_test/ceshi_jichu_paobu_nan_anim/thumbnail.jpg'
            )

            i_qt_item_widget._set_image_sequence_path_(i)


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((720, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
