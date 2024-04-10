# coding:utf-8


def main(session):
    import sys

    import lxgui.qt.core as gui_qt_core

    import lxcontent.core as ctt_core

    app = gui_qt_core.QtWidgets.QApplication(sys.argv)
    d = ctt_core.Content(
        value='/l/temp/td/dongchangbao/qt_test/_tst__draw_data.yml'
    )
    gui_qt_core.QtPixmapDrawer.get_image_by_data(d, '/l/temp/td/dongchangbao/qt_test/test_1.png')
    app.exit(0)
    sys.exit(0)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
