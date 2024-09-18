# coding:utf-8
import functools

import lxgui.qt.widgets as qt_widgets

import lxbasic.core as bsc_core

import lxgui.qt.view_widgets as qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.storage as bsc_storage

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

import qsm_lazy.screw.core as qsm_scr_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        scr_stage = qsm_scr_core.Stage('asset_test')

        self._d = qt_view_widgets.QtTreeWidget()
        # self._d._view_model.set_item_sort_keys(['name', 'gui_name', 'gui_name_chs'])
        self.add_widget(self._d)
        # self._d._view._set_view_header_([('name', 4), ('index', 4)], 320-48)
        # self._d._view_model.create_root()

        scr_entities = scr_stage.find_all(
            scr_stage.EntityTypes.Type,
        )
        leaf_entity_path_set = set(
            bsc_core.BscPath.to_leaf_paths([x.path for x in scr_entities])
        )
        for i_scr_entity in scr_entities:
            i_path = i_scr_entity.path
            i_path_opt = bsc_core.BscPathOpt(i_path)
            i_name = i_path_opt.get_name()
            i_flag, i_item = self._d._view._view_model.create_item(i_path)
            i_item.setExpanded(True)
            i_item._item_model.set_icon_name(i_scr_entity.gui_icon_name)
            i_item._item_model.set_name(i_scr_entity.gui_name_chs)
            i_item._item_model.register_keyword_filter_keys([i_name, i_scr_entity.gui_name, i_scr_entity.gui_name_chs])
            if i_path in leaf_entity_path_set:
                i_scr_assigns = scr_stage.find_all(
                    entity_type=scr_stage.EntityTypes.Assign,
                    filters=[
                        ('type', 'is', 'type_assign'),
                        ('target', 'is', i_path),
                    ]
                )
                i_item._item_model.set_assign_path_set(set([x.source for x in i_scr_assigns]))
                i_item._item_model._update_assign_path_set_to_ancestors()
                # i_item.setSizeHint(0, QtCore.QSize(40, 40))
        for i in range(100):
            i_path = '/test_{}'.format(i)
            i_flag, i_item = self._d._view._view_model.create_item(i_path)
            i_item._item_model.set_icon_name('tree/folder')
            for j in range(100):
                j_path = '{}/test_{}_{}'.format(i_path, i, j)
                j_flag, j_item = self._d._view._view_model.create_item(j_path)
                j_item._item_model.set_icon_name('tree/file')

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


def test():
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 480))
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
