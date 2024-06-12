# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import qsm_screw.core as qsm_scr_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = gui_prx_widgets.PrxTagFilterView(self._qt_widget)
        self.add_widget(self._d)

        self._scr_stage = qsm_scr_core.Stage(
            'Z:/libraries/screw/.database/node.db'
        )
        self._scr_stage.connect()

        for i in self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Tag,
            filters=[
                ('category', 'is', 'group')
            ]
        ):
            i_group = self._d.create_group(i.path, show_name=i.gui_name_chs)
            if i.path == '/':
                i_group._set_text_(i.gui_name_chs)

            i_group._set_expanded_(True)

            i_c = len(
                self._scr_stage.find_all(
                    entity_type=self._scr_stage.EntityTypes.Assign,
                    filters=[
                        ('type', 'is', 'tag_assign'),
                        ('target', 'startswith', i.path),
                    ]
                )
            )
            i_group._set_number_(i_c)
            i_group._set_tool_tip_(i.to_string())

        for i in self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Tag,
            filters=[('category', 'is', 'node')]
        ):
            i_node = self._d.create_node(i.path, show_name=i.gui_name_chs)
            i_c = len(
                self._scr_stage.find_all(
                    entity_type=self._scr_stage.EntityTypes.Assign,
                    filters=[
                        ('type', 'is', 'tag_assign'),
                        ('target', 'startswith', i.path),
                    ]
                )
            )
            i_node._set_number_(i_c)
            i_node._set_tool_tip_(i.to_string())


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((320, 480))
    w.set_window_show()
    #
    sys.exit(app.exec_())
