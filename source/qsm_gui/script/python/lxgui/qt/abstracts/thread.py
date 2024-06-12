# coding:utf-8


class AbsQtThreadExtraDef(object):
    def _init_thread_extra_def_(self, widget):
        self._widget = widget

        self._ts = []

    def _do_thread_quit_(self):
        for seq, i in enumerate(self._ts):
            i.do_quit()
            del self._ts[seq]
