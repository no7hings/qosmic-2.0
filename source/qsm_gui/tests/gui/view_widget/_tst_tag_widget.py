# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.view_widgets as gui_qt_vew_widgets

import lnx_screw.core as lnx_scr_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d_0 = gui_qt_vew_widgets.QtTagWidget(self._qt_widget)
        self.add_widget(self._d_0)
        self._d_0._view_model.set_item_color_enable(True)

        self._scr_stage = lnx_scr_core.Stage(
            'asset_test'
        )
        # self._scr_stage.connect()

        self._d_0.refresh.connect(self.test)

        # self.test()

    def test(self):
        self._d_0._view_model.restore()
        scr_entities = self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Tag,
        )
        scr_entity_paths = [x.path for x in scr_entities]
        leaf_path_set = set(bsc_core.BscNodePath.to_leaf_paths(scr_entity_paths))

        for i in scr_entities:
            i_path = i.path
            if i_path in leaf_path_set:
                i_flag, i_item = self._d_0._view_model.create_item(i_path)
                i_item._item_model.set_name(i.gui_name_chs)

                i_item._set_tool_tip_(i.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))
                i_scr_assigns = self._scr_stage.find_all(
                    entity_type=self._scr_stage.EntityTypes.Assign,
                    filters=[
                        ('type', 'is', 'tag_assign'),
                        ('target', 'is', i_path),
                    ]
                )
                i_path_set = set([x.source for x in i_scr_assigns])
                i_item._set_assign_path_set_(i_path_set)
                i_item._update_assign_path_set_to_ancestors()
            else:
                i_flag, i_item = self._d_0._view_model.create_group_item(i_path)
                i_item._item_model.set_name(i.gui_name_chs)

                i_item._set_expanded_(True)

                i_item._set_tool_tip_(i.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))

        flag, item = self._d_0._view_model.create_item('/test')
        item._item_model.set_name('TEST')


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((320, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
