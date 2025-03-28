# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.qt.view_widgets as qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.qt.docker as qt_docker

import lxgui.qt.core as gui_qt_core


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap
    #
    app = wrap.QtWidgets.QApplication(sys.argv)

    w = qt_docker.QtDockerWindow()
    w._set_definition_window_size_((1280, 720))

    wgt_0 = qt_view_widgets.QtTreeWidget()
    w._create_center_widget(wgt_0)

    wgt_1 = qt_view_widgets.QtTreeWidget()
    w._create_left_docker('Left', wgt_1)

    wgt_2 = qt_view_widgets.QtTreeWidget()
    w._create_right_docker('Right', wgt_2)

    w._accept_corner()

    w._do_window_show_()
    #
    sys.exit(app.exec_())
