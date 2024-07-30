# coding:utf-8
import time

import random

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.qt.graphs as gui_qt_graphs

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.scripts as prx_scripts

import qsm_general.core as qsm_gnl_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        self._wgt = gui_qt_graphs.QtComposition()
        self.add_widget(self._wgt)

        post_cycles = range(1, 5)
        starts = range(1, 96)

        args = [
            ('sam_walk_macho_forward', 33),
            ('sam_run_turn_left', 33),
            ('sam_walk_forward', 33),
            ('sam_walk_sneak_turn_right', 33),
            ('sam_run_forward', 33),
            ('sam_walk_sneak_forward', 33)
        ]

        random.seed(1)

        node = None
        for i in range(10):
            i_text, i_source_count = random.choice(args)
            i_post_cycle = random.choice(post_cycles)
            if node is not None:
                i_start = node._track_model.clip_end+1
            else:
                i_start = 1
            # i_start = random.choice(starts)

            i_node = self._wgt._graph._create_node_(
                key='{}_{}'.format(i_text, i), start=i_start, source_start=0, source_end=i_source_count-1,
                pre_cycle=0, post_cycle=i_post_cycle,
                layer_index=i
            )
            # i_node._set_name_text_(i_text)

            # if node is not None:
            #     i_connection = self._wgt._graph._create_connection_()
            #     node._add_start_connection_(i_connection)
            #     i_node._add_end_connection_(i_connection)
            node = i_node

        self._wgt._graph._translate_graph_to_(0, 0)
        self._wgt._graph._scale_graph_to_(0.1, 1)


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 720))
    w.show_window_auto()

    sys.exit(app.exec_())
