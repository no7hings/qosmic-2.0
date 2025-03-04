# coding:utf-8
import lnx_resora.core as c

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.qt.core as gui_qt_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        directory_path = 'C:/Users/nothings/Documents/Megascans Library/Downloaded/3d'

        c.QuixelRegisterBatch.register_fnc(
            'resource_quixel_asset_29', directory_path, 'asset'
        )


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
