# coding:utf-8
import os

from lxgui.qt.core.wrap import *

import lxbasic.storage as bsc_storage

import lxgui.proxy.widgets as prx_widgets


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        b = prx_widgets.PrxPressItem()
        self.add_button(b)
        b.set_name('Test')

        f = '/l/prod/cjd/publish/assets/chr/nn_gongshifu/srf/surfacing/nn_gongshifu.srf.surfacing.v019/review/nn_gongshifu.srf.surfacing.v019.mov'
        f_o = '/data/f/vedio_to_thumbnail_test/test_1.jpg'

        self._timer = QtCore.QTimer(self.widget)
        self._sub_process = None
        if os.path.exists(f):
            thumbnail_file_path, cmds = bsc_storage.VdoFileOpt(f).generate_thumbnail_create_args()
            if cmds:
                pass
            else:
                pass

    def _update_(self):
        if self._sub_process is not None:
            self._sub_process.do_update()
            print self._sub_process.get_status()


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_window_show()
    #
    sys.exit(app.exec_())
