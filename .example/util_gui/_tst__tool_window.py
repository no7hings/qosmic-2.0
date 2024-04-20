# coding:utf-8
import threading

import time

import lxbasic.log as bsc_log

import lxgui.proxy.widgets as prx_widgets

if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = prx_widgets.PrxBaseWindow()
    w.set_window_show()

    c_0 = 5
    c_1 = 10
    c_2 = 20
    with bsc_log.LogProcessContext.create(maximum=c_0, label='main') as g_p_0:
        for i_0 in range(c_0):
            time.sleep(.04)
            with bsc_log.LogProcessContext.create(maximum=c_1, label='sub-{}'.format(i_0)) as g_p_1:
                g_p_0.do_update()
                for i_1 in range(c_1):
                    g_p_1.do_update()
                    time.sleep(.02)
                    with bsc_log.LogProcessContext.create(maximum=c_2, label='sub-sub-{}'.format(i_1)) as g_p_2:
                        for i_2 in range(c_2):
                            g_p_2.do_update()
                            time.sleep(.01)

    sys.exit(app.exec_())
