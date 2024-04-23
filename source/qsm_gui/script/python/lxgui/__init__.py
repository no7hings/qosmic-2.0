# coding:utf-8


def do_reload():
    # noinspection PyUnresolvedReferences
    import QtSide
    qt_widgets = QtSide.QtWidgets.QApplication.topLevelWidgets()
    for i in qt_widgets:
        if hasattr(i, 'lynxi_window'):
            i.close()
            i.deleteLater()

