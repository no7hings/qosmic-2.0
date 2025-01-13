# coding:utf-8
import math

import lxbasic.core as bsc_core

from ... import core as _gui_core

from ..core.wrap import *

from .. import core as _qt_core

from . import base as _base


class ChartModelForCurve(object):
    class TangentTypes:
        Linear = 0
        Flag = 1

    def __init__(self):
        self._branches = [
            _base._Data(
                coord=(2, 2)
            ),
            _base._Data(
                coord=(4, 4)
            ),
            _base._Data(
                coord=(6, 6)
            )
        ]

        self._margin = 16

        self._w, self._h = 1, 1

        self._scale_x, self._scale_y = 1, 1

        self._tangent_handle_width = 1

        self._tangent_type = ''

    def generate_pixmap(self, x, y, w, h):
        self.update(x, y, w, h)

        size = QtCore.QSize(w, h)
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtGui.QColor(63, 63, 63, 255))
        painter = QtGui.QPainter(pixmap)
        self._draw_curve(painter)
        painter.end()
        return pixmap

    def update(self, x, y, w, h):
        self._w, self._h = w, h

    def _draw_curve(self, painter):
        painter.setRenderHint(painter.Antialiasing)

        self._tangent_handle_width = self._w*0.25

        offset_x, offset_y, self._scale_x, self._scale_y = self.compute_offset_and_scale()

        path = QtGui.QPainterPath()

        points = []
        if self._branches:
            for i_point in self._branches:
                i_x, i_y = i_point["coord"]
                points.append(
                    QtCore.QPointF(
                        (i_x+offset_x)*self._scale_x+self._margin,
                        self._h-((i_y+offset_y)*self._scale_y+self._margin)
                    )
                )

        self._draw_line(painter, points)

        painter.setPen(QtCore.Qt.black)
        painter.drawPath(path)

    def _draw_line(self, painter, points):
        if len(points) < 2:
            return

        path = QtGui.QPainterPath()

        point_first = points[0]
        path.moveTo(point_first)

        c = len(points)

        for i in range(len(points)-1):
            i_point_pre = points[i]
            i_point = points[i+1]

            i_out_tangent_point = QtCore.QPointF(i_point_pre.x() + self._tangent_handle_width, i_point_pre.y())
            i_in_tangent_point = QtCore.QPointF(i_point.x()-self._tangent_handle_width, i_point.y())

            painter.setPen(QtGui.QPen(QtGui.QColor(95, 95, 95, 255), 2))
            painter.drawLine(i_point_pre, i_out_tangent_point)
            painter.drawLine(i_point, i_in_tangent_point)

            #
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0, 255), 2))
            i_rect = QtCore.QRect(
                i_point.x()-3, i_point.y()-3, 6, 6
            )
            painter.drawEllipse(
                i_rect
            )

            # out tangent
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0, 255), 2))
            i_in_rect = QtCore.QRect(
                i_out_tangent_point.x()-2, i_out_tangent_point.y()-2, 4, 4
            )
            painter.drawEllipse(i_in_rect)

            # in tangent
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0, 255), 2))
            i_out_rect = QtCore.QRect(
                i_in_tangent_point.x()-2, i_in_tangent_point.y()-2, 4, 4
            )
            painter.drawEllipse(i_out_rect)

            path.cubicTo(i_out_tangent_point, i_in_tangent_point, i_point)

        painter.setPen(QtGui.QPen(QtGui.QColor(223, 223, 223, 255), 2))
        painter.drawPath(path)

    def compute_x_maximum(self):
        if self._branches:
            return max([x.coord[0] for x in self._branches])
        return 1

    def compute_y_maximum(self):
        if self._branches:
            return max([x.coord[1] for x in self._branches])
        return 1

    def compute_offset_and_scale(self):
        if self._branches:
            x_min = min([x.coord[0] for x in self._branches])
            x_max = max([x.coord[0] for x in self._branches])
            y_min = min([x.coord[1] for x in self._branches])
            y_max = max([x.coord[1] for x in self._branches])
            x_range = max(x_max-x_min, 1e-5)
            y_range = max(y_max-y_min, 1e-5)
            return -x_min, -y_min, (self._w-self._margin*2)/x_range, (self._h-self._margin*2)/y_range
        return 0, 0, 1, 1

