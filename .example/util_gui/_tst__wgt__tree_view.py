# coding:utf-8
import lxgui.proxy.widgets as utl_prx_widgets

import lxresolver.core as rsv_core


class TestWindow(utl_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        tool_bar = utl_prx_widgets.PrxHToolBar()
        self.add_widget(tool_bar)
        tool_bar.set_expanded(True)
        tool_group_0 = utl_prx_widgets.PrxHToolBox()
        tool_bar.add_widget(tool_group_0)
        tool_bar.set_left_alignment()

        tool = utl_prx_widgets.PrxIconPressButton()
        tool_group_0.add_widget(tool)
        tool.set_icon_name('application/python')

        tool_group_1 = utl_prx_widgets.PrxHToolBox()
        tool_bar.add_widget(tool_group_1)
        tool_group_1.set_size_mode(1)

        tool = utl_prx_widgets.PrxFilterBar()
        tool_group_1.add_widget(tool)
        # r = rsv_core.RsvBase.generate_root()
        # n = utl_prx_widgets.PrxNode('root')
        # self.add_widget(n)
        # assets = r.get_rsv_resources(
        #     project='cgm', branch='asset'
        # )
        # p = n.add_port(
        #     utl_prx_widgets.PrxRsvObjChoosePort(
        #         'test'
        #     )
        # )
        # p.set(
        #     assets
        # )


if __name__ == '__main__':
    import time
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_window_show()
    #
    sys.exit(app.exec_())
