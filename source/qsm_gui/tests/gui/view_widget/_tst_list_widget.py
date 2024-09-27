# coding:utf-8
import os

os.environ['PATH'] += ';Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin'

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
        self._d._view_model.set_item_sort_keys(['name', 'gui_name', 'gui_name_chs'])
        self._d._view_model.set_item_check_enable(True)
        self._d._view_model.set_item_drag_enable(True)
        self._d._view_model.set_item_lock_enable(True)
        self._d._view_model.set_item_frame_size(222, 222)
        self.add_widget(self._d)
        for i in range(10):
            i_path = '/test_aaaaaaaaaaaaaaaa{}'.format(i)
            i_create_flag, i_item = self._d._view._view_model.create_item(i_path)
            # i_item._item_model.set_icon_name('file/file')
            i_item._item_model.set_tool_tip('TEST-{}'.format(i))
            i_item._item_model.register_keyword_filter_keys(['TEST-{}'.format(i), u'测试'])
            if i% 3:
                i_item._item_model.set_locked(True)

            i_item._item_model.register_sort_dict(
                dict(
                    name='TEST-{}'.format(i),
                    gui_name='TEST {}'.format(str(i).zfill(4)),
                    gui_name_chs=u'测试 ｛｝'.format(str(i).zfill(4)),
                )
            )

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
                    image_sequence='Z:/libraries/lazy-resource/all/motion_test/ceshi_jichu_paobu_run_female_anim/preview/images/image.%04d.jpg'
                )
            ]
        elif index%3:
            return [
                item, dict(
                    video='Z:/temporaries/dynamic_gpu/test_1.mov'
                )
            ]
        elif index%4:
            return [
                item, dict(
                    audio='Z:/temporaries/tst_wav/751427__flavioconcini__fx-sound.wav'
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
            elif 'video' in property_dict:
                item._item_model.set_video(property_dict['video'])
            elif 'image' in property_dict:
                item._item_model.set_image(property_dict['image'])
            elif 'audio' in property_dict:
                item._item_model.set_audio(property_dict['audio'])

            # item._item_model.refresh_force()


def test():
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 960))
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
