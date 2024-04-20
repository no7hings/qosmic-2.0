# coding:utf-8
import lxbasic.log as bsc_log

import lxgui.proxy.widgets as prx_widgets

import lxgui.proxy.core as gui_prx_core

import lxgui.qt_for_opengl.widgets as gui_qt_ogl_widgets

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.core as bsc_dcc_core

bsc_log.Log.TEST = True


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self.set_definition_window_size([512+4, 512+22])

        v = gui_qt_ogl_widgets.QtGLWidget()

        self.add_widget(v)


if __name__ == '__main__':
    bsc_dcc_core.OcioSetup(
        bsc_storage.StgPathMapper.map_to_current(
            '/job/PLE/bundle/thirdparty/aces/1.2'
        )
    ).set_run()

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(W)

