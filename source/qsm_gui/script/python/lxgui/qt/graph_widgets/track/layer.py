# coding=utf-8
# gui
from .... import core as _gui_core
# qt
from ...core.wrap import *

from ... import core as _qt_core
# base
from ..base import graph as _bsc_graph


class QtTrackLayer(
    _bsc_graph.QtSbjLayer
):

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        pass

    def _set_coord_model_(self, model):
        self._coord_model = model

    def __init__(self, *args, **kwargs):
        super(QtTrackLayer, self).__init__(*args, **kwargs)

        self._coord_model = None
        self._graph = None

        self._layer_rect = QtCore.QRect()

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)
        self._draw_layer_basic_(painter)

    def _update_from_graph_(self, rect, translate, scale):
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

        self._coord_model.update(translate, scale, h)

        self._layer_rect.setRect(x, y, w, h)

        self._refresh_widget_all_()

    def _set_graph_(self, widget):
        self._graph = widget

    def _step_coord_to_layer_(self, y):
        return self._coord_model.step_coord_loc(y)

    def _draw_layer_basic_(self, painter):
        x, y, w, h = self._layer_rect.x(), self._layer_rect.y(), self._layer_rect.width(), self._layer_rect.height()

        c = self._coord_model.unit_count

        for i in range(c):
            i_layer_index = self._coord_model.compute_draw_index_at(i)
            i_y = self._coord_model.compute_draw_coord_at(i)
            i_rect = QtCore.QRect(x, i_y, w, self._coord_model.unit_size)
            if i_layer_index % 2:
                i_rgba =_gui_core.GuiRgba.Dark
                painter._set_border_color_(i_rgba)
                painter._set_background_color_(i_rgba)
                painter.drawRect(i_rect)

            painter._set_border_color_(_gui_core.GuiRgba.DarkGray)
            painter._set_font_(_qt_core.QtFont.generate(size=10, italic=True))
            painter.drawText(
                i_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, str(i_layer_index)
            )
