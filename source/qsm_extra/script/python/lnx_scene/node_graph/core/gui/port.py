# coding:utf-8
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

from .. import base as _base

from .. import model as _model

from . import aux_ as _aux


# port
class _AbsPortGui(
    QtWidgets.QGraphicsPathItem,
    _base._QtSbjBase,
):
    MODEL_CLS = None

    def __init__(self, parent, w, h):
        super(_AbsPortGui, self).__init__(parent)
        self.setZValue(1)
        self.setFlags(self.ItemSendsScenePositionChanges)

        self.setAcceptHoverEvents(True)

        self._set_color(_base._QtColors.Port)

        self.edges = []

        self._model = self.MODEL_CLS(self)

        self._hover_flag = False
        self._w, self._h = w, h

        self._name_aux = _aux.QtTextAux('', self)
        self._name_aux.hide()

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemScenePositionHasChanged:
            connections = self._model.get_connections()
            for i_model in connections:
                i_model.update_v()
        return super(_AbsPortGui, self).itemChange(change, value)

    def _set_color(self, color):
        self.setPen(self._to_pen(color))
        self.setBrush(color)

    @classmethod
    def _to_pen(cls, color):
        pen = QtGui.QPen(color, 1)
        pen.setCapStyle(QtCore.Qt.SquareCap)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        return pen

    def hoverEnterEvent(self, event):
        self._hover_flag = True
        self._name_aux.show()
        self.update()
        super(_AbsPortGui, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._hover_flag = False
        self._name_aux.hide()
        self.update()
        super(_AbsPortGui, self).hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
        painter.save()

        if self._hover_flag is True:
            pen = self._to_pen(QtGui.QColor(*gui_core.GuiRgba.LightOrange))
        else:
            pen = self.pen()

        painter.setPen(pen)
        painter.setBrush(pen.color())
        painter.drawPath(self.path())

        painter.restore()


class InputGui(_AbsPortGui):
    MODEL_CLS = _model.InputModel

    ENTITY_TYPE = _base.EntityTypes.InputPort

    def __init__(self, *args, **kwargs):
        super(InputGui, self).__init__(*args, **kwargs)

    def _update(self):
        rect = QtCore.QRectF(0, 0, self._w, self._h)
        path = QtGui.QPainterPath()
        path.addRect(rect)
        self.setPath(path)

        text_rect = self._name_aux.boundingRect()
        w, h = text_rect.width(), text_rect.height()

        self._name_aux.setPos(
            0, -h/2
        )
        self._name_aux.setRotation(-45)


class OutputGui(_AbsPortGui):
    MODEL_CLS = _model.OutputModel

    ENTITY_TYPE = _base.EntityTypes.OutputPort

    def __init__(self, *args, **kwargs):
        super(OutputGui, self).__init__(*args, **kwargs)

    def _update(self):
        path = QtGui.QPainterPath()
        polygon = QtGui.QPolygonF(
            [
                QtCore.QPointF(0, 0),
                QtCore.QPointF(self._w, 0),
                QtCore.QPointF(self._w/2, self._h),
                QtCore.QPointF(0, 0),
            ]
        )
        path.addPolygon(polygon)
        self.setPath(path)

        text_rect = self._name_aux.boundingRect()
        w, h = text_rect.width(), text_rect.height()

        self._name_aux.setPos(
            (self._w-w)/2, self._h
        )
