# coding:utf-8
import enum

import math
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

from .. import base as _base

from .. import model as _model


# connection
class ConnectionGui(
    QtWidgets.QGraphicsPathItem,
    _base._QtSbjBase,
):
    class Regions(enum.IntEnum):
        Source = 0
        Target = 1

    ENTITY_TYPE = _base.EntityTypes.Connection

    @classmethod
    def _calculate_midpoint_and_angle(cls, p0, p1, p2, p3):
        t = 0.5

        mid_x = (1-t)**3*p0.x()+3*(1-t)**2*t*p1.x()+3*(1-t)*t**2*p2.x()+t**3*p3.x()
        mid_y = (1-t)**3*p0.y()+3*(1-t)**2*t*p1.y()+3*(1-t)*t**2*p2.y()+t**3*p3.y()
        _mid_p = QtCore.QPointF(mid_x, mid_y)

        dx = 3*(1-t)**2*(p1.x()-p0.x())+6*(1-t)*t*(p2.x()-p1.x())+3*t**2*(p3.x()-p2.x())
        dy = 3*(1-t)**2*(p1.y()-p0.y())+6*(1-t)*t*(p2.y()-p1.y())+3*t**2*(p3.y()-p2.y())

        _tangent_angle = math.atan2(dy, dx)
        return _mid_p, _tangent_angle

    def __init__(self, source_port=None, target_port=None):
        super(ConnectionGui, self).__init__()
        self.setZValue(0)
        # allow to select?
        # self.setFlags(self.ItemIsSelectable)

        self._source_port = source_port
        self._target_port = target_port
        self._arrow_size = 12
        self._mid_p = QtCore.QPointF()
        self._tangent_angle = 0
        self._pen_w = 2

        self._default_color = _base._QtColors.Connection

        self._set_color(self._default_color)

        self._model = _model.ConnectionModel(self)

        self._start_p = QtCore.QPointF()
        self._end_p = QtCore.QPointF()

        self._hover_enable = False
        self._hover_flag = False
        self._hover_region = None

    def _set_hover_enable(self, boolean):
        self._hover_enable = boolean
        self.setAcceptHoverEvents(boolean)

    def _set_color(self, color):
        self.setPen(self._to_pen(color))

    def _set_default_color(self, color):
        self._default_color = color
        self._set_color(self._default_color)

    def _to_pen(self, color):
        pen = QtGui.QPen(color, self._pen_w)
        pen.setCapStyle(QtCore.Qt.SquareCap)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        return pen

    def _update_h(self, start_point=None, end_point=None):
        if start_point:
            self._start_p = QtCore.QPointF(start_point)
        elif self._source_port:
            source_port_item = self._source_port._gui
            start = source_port_item.scenePos()
            out_rect = source_port_item.rect()
            out_w, out_h = out_rect.width(), out_rect.height()
            self._start_p = QtCore.QPointF(start.x()+out_w/2-1, start.y()+out_h/2)
        else:
            self._start_p = QtCore.QPointF()
        if end_point:
            self._end_p = QtCore.QPointF(end_point)
        elif self._target_port:
            target_port_item = self._target_port._gui
            end = target_port_item.scenePos()
            ipt_rect = target_port_item.rect()
            ipt_w, ipt_h = ipt_rect.width(), ipt_rect.height()
            self._end_p = QtCore.QPointF(end.x()+ipt_w/2-1, end.y()+ipt_h/2)
        else:
            self._end_p = QtCore.QPointF()

        path = QtGui.QPainterPath()
        path.moveTo(self._start_p)
        dx = (self._end_p.x()-self._start_p.x())*0.5
        ctrl1 = QtCore.QPointF(self._start_p.x()+dx, self._start_p.y())
        ctrl2 = QtCore.QPointF(self._end_p.x()-dx, self._end_p.y())
        path.cubicTo(ctrl1, ctrl2, self._end_p)

        self.setPath(path)

        self._mid_p, self._tangent_angle = self._calculate_midpoint_and_angle(self._start_p, ctrl1, ctrl2, self._end_p)

    def _update_v(self, start_point=None, end_point=None):
        if start_point:
            self._start_p = QtCore.QPointF(start_point)
        elif self._source_port:
            source_port_item = self._source_port._gui
            start = source_port_item.scenePos()
            out_rect = source_port_item.boundingRect()
            out_w, out_h = out_rect.width(), out_rect.height()
            self._start_p = QtCore.QPointF(start.x()+out_w/2-1, start.y()+out_h/2)
        else:
            self._start_p = QtCore.QPointF()
        if end_point:
            self._end_p = QtCore.QPointF(end_point)
        elif self._target_port:
            target_port_item = self._target_port._gui
            end = target_port_item.scenePos()
            ipt_rect = target_port_item.boundingRect()
            ipt_w, ipt_h = ipt_rect.width(), ipt_rect.height()
            self._end_p = QtCore.QPointF(end.x()+ipt_w/2-1, end.y()+ipt_h/2)
        else:
            self._end_p = QtCore.QPointF()

        path = QtGui.QPainterPath()
        path.moveTo(self._start_p)

        dy = (self._end_p.y()-self._start_p.y())*0.5
        ctrl1 = QtCore.QPointF(self._start_p.x(), self._start_p.y()+dy)
        ctrl2 = QtCore.QPointF(self._end_p.x(), self._end_p.y()-dy)

        path.cubicTo(ctrl1, ctrl2, self._end_p)

        self.setPath(path)

        self._mid_p, self._tangent_angle = self._calculate_midpoint_and_angle(self._start_p, ctrl1, ctrl2, self._end_p)

    def boundingRect(self):
        rect = self.path().boundingRect()

        extra = self._arrow_size*2
        return rect.adjusted(-extra, -extra, extra, extra)

    def hoverEnterEvent(self, event):
        if self._hover_enable is True:
            self._hover_flag = True
            self._hover_region = self._get_region(event.pos())
            self.update()
        super(ConnectionGui, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if self._hover_enable is True:
            self._hover_flag = False
            self._hover_region = None
            self.update()
        super(ConnectionGui, self).hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
        painter.save()

        select_flag = bool(option.state & QtWidgets.QStyle.State_Selected)
        if select_flag is True:
            color = QtGui.QColor(*gui_core.GuiRgba.LightAzureBlue)
            arrow_color = color
        elif self._hover_flag is True:
            color = QtGui.QColor(*gui_core.GuiRgba.LightOrange)
            arrow_color = color
        else:
            color = self.pen().color()
            arrow_color = color

        curve_pen = self._to_pen(color)

        if self._hover_enable is True:
            if self._hover_region is not None:
                start_p, end_p = self._start_p, self._end_p
                color_g = QtGui.QLinearGradient(start_p, end_p)
                if self._hover_region == self.Regions.Source:
                    color_g.setColorAt(.5, color)
                    color_g.setColorAt(.75, self.pen().color())
                elif self._hover_region == self.Regions.Target:
                    color_g.setColorAt(.25, self.pen().color())
                    color_g.setColorAt(.5, color)

                curve_pen = self._to_pen(color_g)

        painter.setPen(curve_pen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        painter.drawPath(self.path())

        arrow_p1 = self._mid_p-QtCore.QPointF(
            self._arrow_size*math.cos(self._tangent_angle-math.radians(30)),
            self._arrow_size*math.sin(self._tangent_angle-math.radians(30)),
        )
        arrow_p2 = self._mid_p-QtCore.QPointF(
            self._arrow_size*math.cos(self._tangent_angle+math.radians(30)),
            self._arrow_size*math.sin(self._tangent_angle+math.radians(30)),
        )

        arrow_head = QtGui.QPolygonF([self._mid_p, arrow_p1, arrow_p2])
        painter.setPen(arrow_color)
        painter.setBrush(arrow_color)
        painter.drawPolygon(arrow_head)

        painter.restore()

    def _get_source_point(self):
        if self._source_port:
            source_port_item = self._source_port._gui
            start = source_port_item.scenePos()
            out_rect = source_port_item.boundingRect()
            out_w, out_h = out_rect.width(), out_rect.height()
            return QtCore.QPointF(start.x()+out_w/2-2, start.y()+out_h/2)
        else:
            return QtCore.QPointF(0, 0)

    def _get_target_point(self):
        if self._target_port:
            target_port_item = self._target_port._gui
            end = target_port_item.scenePos()
            ipt_rect = target_port_item.boundingRect()
            ipt_w, ipt_h = ipt_rect.width(), ipt_rect.height()
            return QtCore.QPointF(end.x()+ipt_w/2-1, end.y()+ipt_h/2)
        else:
            return QtCore.QPointF(0, 0)

    def _get_region(self, point):
        dst_to_source = (point-self._get_source_point()).manhattanLength()
        dst_to_target = (point-self._get_target_point()).manhattanLength()

        if dst_to_source < dst_to_target:
            return self.Regions.Source
        return self.Regions.Target
