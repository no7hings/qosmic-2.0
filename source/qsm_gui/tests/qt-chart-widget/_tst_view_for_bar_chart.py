# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        data_0 = bsc_storage.StgFileOpt(
            'Z:/caches/temporary/.asset-cache/mesh-count/32M/BBCFACD7-1A0B-3EF1-B7FC-44EE86FACF8E.json'
        ).set_read()

        self._d = qt_widgets.QtViewForBarChart(self._qt_widget)
        data = data_0['mesh_count']['components']
        data['VALUE_LIMIT'] = dict(
            face=250000,
            face_per_world_area=25,
            triangle=500000,
            triangle_per_world_area=50,
        )
        self._d._set_data_(
            data_0['mesh_count']['components'],
            ['triangle', 'triangle_per_world_area'],
            data_key_names=['三角面数', '三角面数（单位面积）']
        )
        self._d._set_name_text_('TEST')
        self.add_widget(self._d)


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 480))
    w.show_window_auto()

    sys.exit(app.exec_())
