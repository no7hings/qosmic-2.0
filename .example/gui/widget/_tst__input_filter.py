# coding:utf-8
import fnmatch

import lxbasic.core as bsc_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets

import lxbasic.shotgun as bsc_shotgun


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._wgt = qt_widgets.QtInputAsFilter()
        self._wgt._set_history_key_('gui.input-filter-test')

        self._wgt._set_input_completion_buffer_fnc_(
            self._value_completion_gain_fnc_
        )

        self.add_widget(self._wgt)

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        return fnmatch.filter(
            ['test', 'testA'], '*{}*'.format(args[0])
        )


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.set_window_show()
    #
    sys.exit(app.exec_())
