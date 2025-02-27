# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class TestWindow(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)

    def _test_(self):
        wdt = gui_prx_widgets.PrxListView()
        wdt.do_clear()
        self.add_widget(wdt)
        for i in range(50):
            item_prx = wdt.create_item(name=str(i))
            item_prx.set_image('/data/f/vedio_test/laohu_da.rig.layout_rigging.v002.thumbnail.jpg')
            item_prx.set_icon_by_file('application/maya')
            item_prx.set_name(str(i).zfill(9))
            item_prx.set_gui_menu_data(
                [
                    ('Open folder', 'file/open-folder', None),
                ]
            )


if __name__ == '__main__':
    import time
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.show_window_auto()
    w._test_()
    #
    sys.exit(app.exec_())
