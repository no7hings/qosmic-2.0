# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import qsm_lazy.screw.core as qsm_lzy_scr_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d_0 = gui_prx_widgets.PrxTagInput(self._qt_widget)
        self.add_widget(self._d_0)
        self._d_1 = gui_prx_widgets.PrxTagInput(self._qt_widget)
        self.add_widget(self._d_1)

        self._scr_stage = qsm_lzy_scr_core.Stage(
            'maya_cfx'
        )
        # self._scr_stage.connect()

        self.connect_refresh_action_for(self.test)

        self.test()

    def test(self):
        self._d_0.restore()
        self._d_1.restore()
        for i in self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Tag,
            filters=[
                ('category', 'is', 'group'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_group = self._d_0.create_group(i.path, show_name=i.gui_name_chs)

            i_group._set_expanded_(True)

            i_group._set_tool_tip_(i.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))

        for i in self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Tag,
            filters=[
                ('category', 'is', 'node'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_node = self._d_0.create_node(i.path, show_name=i.gui_name_chs)

            i_node._set_tool_tip_(i.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))



        for i in self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Type,
            filters=[
                ('category', 'is', 'group'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_group = self._d_1.create_group(i.path, show_name=i.gui_name_chs)

            i_group._set_expanded_(True)

            i_group._set_tool_tip_(i.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))

        for i in self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Type,
            filters=[
                ('category', 'is', 'node'),
                ('kind', 'is not', 'unavailable')
            ]
        ):
            i_node = self._d_1.create_node(i.path, show_name=i.gui_name_chs)

            i_node._set_tool_tip_(i.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))



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
