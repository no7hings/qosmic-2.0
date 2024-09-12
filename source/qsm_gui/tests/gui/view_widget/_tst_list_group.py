# coding:utf-8
import functools

import lxgui.qt.widgets as qt_widgets

import lxgui.qt.view_widgets as qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = qt_view_widgets.QtListWidget()
        self._d._view_model.set_sort_keys(['name', 'gui_name', 'gui_name_chs'])
        self.add_widget(self._d)
        for i in range(5000):
            i_item = self._d._view._view_model.create_item()
            i_item._item_model.set_name('TEST-{}'.format(i))
            i_item._item_model.set_tool_tip('TEST-{}'.format(i))
            i_item._item_model.apply_keyword_filter_keys(['TEST-{}'.format(i), u'测试'])

            i_item._item_model.update_sort_dict(
                dict(
                    name='TEST-{}'.format(i),
                    gui_name='TEST {}'.format(str(i).zfill(4)),
                    gui_name_chs=u'测试 ｛｝'.format(str(i).zfill(4)),
                )
            )

            i_item._item_model.set_show_fnc(
                functools.partial(self.cache_fnc, i_item, i),
                self.build_fnc
            )
        #
        # for i in range(2):
        #     i_wgt = self._d._create_one_('/TEST-{}'.format(i))
        #     for j in range(1000):
        #         j_item = i_wgt._create_item_()

    def cache_fnc(self, item, index):
        if index%2:
            return [
                item, dict(
                    image_sequence='Z:/libraries/lazy-resource/all/motion_test/ceshi_jichu_paobu_run_female_anim/preview/images/image.%04d.jpg'
                )
            ]
        else:
            return [
                item, dict(
                    image='Z:/libraries/lazy-resource/all/asset_test/QSM_TST_amanda/thumbnail.jpg'
                )
            ]

    def build_fnc(self, data):
        if data:
            item, property_dict = data
            if 'image_sequence' in property_dict:
                item._item_model.set_image_sequence(property_dict['image_sequence'])
            elif 'image' in property_dict:
                item._item_model.set_image(property_dict['image'])

            # item._item_model.refresh_force()


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 480))
    w.show_window_auto()

    sys.exit(app.exec_())
