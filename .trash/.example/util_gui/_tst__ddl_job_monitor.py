# coding:utf-8
import lxgui.core as gui_core

job_id = '63046e26e127c602cc7542fe'


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtCore, QtWidgets

    #
    app = QtWidgets.QApplication(sys.argv)

    gui_core.GuiMonitorForDeadline.set_create(
        'test', job_id
    )

    sys.exit(app.exec_())
