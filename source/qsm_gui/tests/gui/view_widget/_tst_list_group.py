# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.qt.view_widgets as qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = qt_view_widgets.QtListWidget()
        self.add_widget(self._d)
        for i in range(5000):
            i_item = self._d._view._view_model.create_item()
            i_item._item_model.set_name('Test-{}'.format(i))
            i_item._item_model.set_tool_tip('Test-{}'.format(i))
            i_item._item_model.apply_keyword_filter_keys(['Test-{}'.format(i), u'测试'])

            if i % 2:
                i_item._item_model.set_image_sequence(
                    'Z:/libraries/lazy-resource/all/motion_test/ceshi_jichu_paobu_run_female_anim/preview/images/image.%04d.jpg'
                )
            else:
                i_item._item_model.set_image('Z:/libraries/lazy-resource/all/asset_test/QSM_TST_amanda/thumbnail.jpg')
        #
        # for i in range(2):
        #     i_wgt = self._d._create_one_('/TEST-{}'.format(i))
        #     for j in range(1000):
        #         j_item = i_wgt._create_item_()


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 480))
    w.show_window_auto()

    sys.exit(app.exec_())
