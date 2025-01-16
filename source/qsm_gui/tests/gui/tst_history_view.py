# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = qt_widgets.QtViewForHistoryEntity(self._qt_widget)

        self.add_widget(self._d)

        import qsm_lazy_backstage.core as lzy_bks_core

        p = lzy_bks_core.NoticePool.generate()
        p.do_update()

        self._d._restore_()

        for i in p.get_entities():
            i_time_text = i.get('time')
            i_group_name = bsc_core.DateTime.to_period(
                i_time_text,
                # 'chs'
            )
            i_wgt = self._d._prepend_item_(
                i.id, i_group_name, i.get('name')
            )
            i_wgt._set_time_text_(i_time_text)
            i_wgt._set_associated_entity_id_(
                i.get('task')
            )
            i_wgt._set_storage_path_(
                i.get('file')
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
