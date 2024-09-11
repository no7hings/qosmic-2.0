# coding=utf-8
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts

from . import sbj_base as _sbj_base


class QtConnection(
    QtWidgets.QWidget,
    _sbj_base.AbsQtConnectionDef,
    #
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
    #
    _qt_abstracts.AbsQtActionForSelectDef,
):
    def _refresh_widget_all_(self):
        self._update_node_geometry_()
        self._update_node_draw_properties_()
        self._refresh_widget_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self, rect):
        def add_cubic_fnc_(p_0, p_1, index):
            c1, c2 = (
                QtCore.QPointF((p_0.x()+p_1.x())/index, p_0.y()),
                QtCore.QPointF((p_0.x()+p_1.x())/index, p_1.y())
            )
            path.cubicTo(c1, c2, p_1)
            path.lineTo(p_1)
            path.cubicTo(c2, c1, p_0)
        #
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        #
        b_w = self._ng_draw_border_w
        #
        if self._ng_connection_dir == 0:
            self._ng_draw_connection_point_start.setX(x+b_w*2)
            self._ng_draw_connection_point_start.setY(y+b_w*2)
            #
            self._ng_draw_connection_point_end.setX(x+w-b_w*4)
            self._ng_draw_connection_point_end.setY(y+h-b_w*2)
        else:
            self._ng_draw_connection_point_start.setX(x+b_w*2)
            self._ng_draw_connection_point_start.setY(y+h-b_w*2)
            #
            self._ng_draw_connection_point_end.setX(x+w-b_w*2)
            self._ng_draw_connection_point_end.setY(y+b_w*2)
        #
        path = QtGui.QPainterPath(self._ng_draw_connection_point_start)
        #
        self._ng_draw_connection_path_curve = path
        #
        add_cubic_fnc_(
            self._ng_draw_connection_point_start,
            self._ng_draw_connection_point_end,
            [2, 1][self._ng_draw_connection_dir]
        )
        #
        p = self._ng_draw_connection_path_curve.pointAtPercent(0.25)
        a = self._ng_draw_connection_path_curve.angleAtPercent(0.25)
        if self._ng_draw_connection_dir == 1:
            a += 180
        r_ = self._ng_draw_border_w*4
        x_, y_ = p.x(), p.y()
        self._ng_draw_connection_coord_arrow = [
            gui_core.GuiEllipse2d.get_coord_at_angle_(center=(x_, y_), radius=r_, angle=90+a),
            gui_core.GuiEllipse2d.get_coord_at_angle_(center=(x_, y_), radius=r_, angle=210+a),
            gui_core.GuiEllipse2d.get_coord_at_angle_(center=(x_, y_), radius=r_, angle=330+a),
            gui_core.GuiEllipse2d.get_coord_at_angle_(center=(x_, y_), radius=r_, angle=90+a)
        ]
        self._ng_draw_connection_point = p

    def _get_ng_draw_connection_background_color_(self, start_point, end_point, draw_dir, is_selected, is_hovered):
        if is_hovered:
            start_color = end_color = QtGui.QColor(63, 255, 255, 255)
        else:
            if is_selected is True:
                start_color = end_color = QtGui.QColor(255, 127, 0, 255)
            else:
                if draw_dir == 1:
                    start_color = QtGui.QColor(63, 255, 127, 255)
                    end_color = QtGui.QColor(255, 63, 31, 255)
                else:
                    start_color = QtGui.QColor(255, 63, 31, 255)
                    end_color = QtGui.QColor(63, 255, 127, 255)
        #
        gradient = QtGui.QLinearGradient(start_point, end_point)
        gradient.setColorAt(0, start_color)
        gradient.setColorAt(1, end_color)
        brush = QtGui.QBrush(gradient)
        pen = QtGui.QPen(brush, self._ng_draw_connection_r)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        return pen, brush

    def __init__(self, *args, **kwargs):
        super(QtConnection, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_select_def_(self)

        self._init_connection_def_(self)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    pass
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    pass
                elif event.buttons() == QtCore.Qt.NoButton:
                    self._do_hover_move_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)

        painter.setRenderHints(
            painter.Antialiasing
        )
        #
        pen, brush = self._get_ng_draw_connection_background_color_(
            self._ng_draw_connection_point_start, self._ng_draw_connection_point_end,
            self._ng_draw_connection_dir,
            False, False
        )
        #
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPath(
            self._ng_draw_connection_path_curve
        )
        painter._draw_path_by_coords_(
            self._ng_draw_connection_coord_arrow
        )

    def _do_hover_move_(self, event):
        _point = event.pos()
