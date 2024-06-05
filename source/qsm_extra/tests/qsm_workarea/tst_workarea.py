# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_gui.proxy.widgets as qsm_widgets

import qsm_workarea.gui.widgets as qsm_workarea_widgets


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        wgt = qt_widgets.QtWidget()
        self.add_widget(wgt)
        lot = qt_widgets.QtVBoxLayout(wgt)
        lot._set_align_top_()

        c = qsm_workarea_widgets.PrxUnitForWorkarea()
        lot.addWidget(c.widget)

        # c.set_root('Z:/projects/QSM_TST/assets/chr/sam/workarea/user.nothings/rig.rigging')
        # c.setup(
        #     dict(
        #         location='Z:/projects',
        #         entity='QSM_TST',
        #         step='dev',
        #         task='developing',
        #         ext='.ma',
        #         artist='nothings',
        #     )
        # )
        c.setup(
            dict(
                location='Z:/projects/QSM_TST/assets/chr',
                entity='sam',
                step='rig',
                task='rigging',
                ext='.ma',
                artist='nothings',
            )
        )



if __name__ == '__main__':
    import sys
    # noinspection PyUnresolvedReferences
    from QtSide import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((500, 720))
    w.set_window_show()
    #
    sys.exit(app.exec_())
