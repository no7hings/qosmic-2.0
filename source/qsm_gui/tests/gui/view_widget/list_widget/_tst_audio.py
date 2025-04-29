# coding:utf-8
import os

import random

os.environ['PATH'] += ';Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin'

os.environ['QSM_UI_LANGUAGE'] = 'chs'

import functools

import lxgui.qt.widgets as qt_widgets

import lxgui.qt.view_widgets as gui_qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._names = [
            '一', '二', '三', '四', '五', '六', '七', '八', '九', '十'
        ]
        self._indices = range(10)

        self._d = gui_qt_view_widgets.QtListWidget()
        self._d._set_item_sort_enable(True)
        self._d._set_item_group_enable(True)
        self._d._view_model.set_item_group_keys(['category'])
        self._d._set_item_check_enable(True)
        self._d._view_model.set_item_category_enable(True)
        self._d._view_model.set_item_drag_enable(True)
        self._d._view_model.set_item_lock_enable(True)
        self._d._view_model.set_item_frame_size(120, 120)
        self.add_widget(self._d)

        self.test()

        self._d.refresh.connect(self.test)

    def test(self):
        self._d._view_model.restore()

        random.seed(0)

        for i in range(10):
            i_path = '/test_{}'.format(i)
            i_create_flag, i_item = self._d._view._view_model.create_item(i_path)
            # i_item._item_model.set_icon_name('file/file')
            i_item._item_model.set_tool_tip('TEST-{}'.format(i))
            i_item._item_model.register_keyword_filter_keys(['TEST-{}'.format(i), u'测试'])

            i_item._item_model.set_group_dict(
                dict(
                    category='分类-{}'.format(random.choice(self._indices))
                )
            )

            i_name = '{}{}{}'.format(
                random.choice(self._names), random.choice(self._names), random.choice(self._names)
            )

            i_item._item_model.set_name(i_name)
            i_item._item_model.set_drag_data(
                dict(file='Z:/libraries/lazy-resource/all/asset_test/QSM_TST_amanda/thumbnail.jpg')
            )

            i_item._item_model.set_show_fnc(
                functools.partial(self.cache_fnc, i_item, i),
                self.build_fnc
            )

    def cache_fnc(self, item, index):
        if index%2:
            return [
                item, dict(
                    audio='Z:/temporaries/tst_wav/751427__flavioconcini__fx-sound.wav'
                )
            ]
        if index%3:
            return [
                item, dict(
                    audio='Z:/temporaries/tst_wav/751748__scpsea__ender-jaguar-growl-and-moaning.mp3'
                )
            ]
        else:
            return [
                item, dict(
                    audio='Z:/temporaries/tst_wav/751515__recalltv__happy-piano-tag.mp3'
                )
            ]

    def build_fnc(self, data):
        if data:
            item, property_dict = data
            item._item_model.set_image(
                'Z:/caches/temporary/.audio-cache/13Q/FAB87DAD-4C43-3124-9A42-C6131007B596.png', source_type='audio'
            )
            if 'audio' in property_dict:
                item._item_model.set_audio(property_dict['audio'], delay_flag=False)

            # item._item_model.refresh_force()


def test():
    import sys

    from lxgui.qt.core import wrap

    # f.setDefaultFormat(f)
    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 960))
    w.show_window_auto()

    sys.exit(app.exec_())


if __name__ == '__main__':
    import cProfile
    import os
    import pstats
    # file_path = '{}/profile.profile'.format(os.path.dirname(__file__))
    # cProfile.run('test()', file_path)
    #
    # p = pstats.Stats(file_path)
    # p.strip_dirs().sort_stats('time').print_stats(10)
    # print p.get_top_level_stats()
    test()
