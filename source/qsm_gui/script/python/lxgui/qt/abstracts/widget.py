# coding:utf-8


class AbsQtWidgetCloseBaseDef(object):
    def _init_widget_close_base_def_(self, widget):
        self._widget = widget

        self._close_flag = False

    def _do_close_(self):
        self._close_flag = True
