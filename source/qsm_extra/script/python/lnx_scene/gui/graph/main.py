# coding:utf-8
import functools

import enum

import math
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

from . import base as _base

from . import model as _model


# connection
class _QtConnection(
    QtWidgets.QGraphicsPathItem,
    _base._QtSbjBase,
):
    class Regions(enum.IntEnum):
        Source = 0
        Target = 1

    SBJ_TYPE = _base._QtSbjTypes.Connection

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
        super(_QtConnection, self).__init__()
        self.setZValue(0)
        # allow to select?
        # self.setFlags(self.ItemIsSelectable)

        self._source_port = source_port
        self._target_port = target_port
        self._arrow_size = 12
        self._mid_p = QtCore.QPointF()
        self._tangent_angle = 0
        self._pen_w = 3
        self._set_color(QtGui.QColor(255, 255, 0, 255))

        self._model = _model._ConnectionModel(self)
        
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
        
    def _to_pen(self, color):
        pen = QtGui.QPen(color, self._pen_w)
        pen.setCapStyle(QtCore.Qt.SquareCap)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        return pen

    def _update_h(self, start_point=None, end_point=None):
        if start_point:
            self._start_p = QtCore.QPointF(start_point)
        elif self._source_port:
            source_port_item = self._source_port._item
            start = source_port_item.scenePos()
            out_rect = source_port_item.rect()
            out_w, out_h = out_rect.width(), out_rect.height()
            self._start_p = QtCore.QPointF(start.x()+out_w/2-1, start.y()+out_h/2)
        else:
            self._start_p = QtCore.QPointF()
        if end_point:
            self._end_p = QtCore.QPointF(end_point)
        elif self._target_port:
            target_port_item = self._target_port._item
            end = target_port_item.scenePos()
            ipt_rect = target_port_item.rect()
            ipt_w, ipt_h = ipt_rect.width(), ipt_rect.height()
            self._end_p = QtCore.QPointF(end.x()+ipt_w/2-1, end.y()+ipt_h/2)
        else:
            self._end_p = QtCore.QPointF()

        path = QtGui.QPainterPath()
        path.moveTo(self._start_p)
        dx = (self._end_p.x() - self._start_p.x()) * 0.5
        ctrl1 = QtCore.QPointF(self._start_p.x()+dx, self._start_p.y())
        ctrl2 = QtCore.QPointF(self._end_p.x() - dx, self._end_p.y())
        path.cubicTo(ctrl1, ctrl2, self._end_p)

        self.setPath(path)

        self._mid_p, self._tangent_angle = self._calculate_midpoint_and_angle(self._start_p, ctrl1, ctrl2, self._end_p)

    def _update_v(self, start_point=None, end_point=None):
        if start_point:
            self._start_p = QtCore.QPointF(start_point)
        elif self._source_port:
            source_port_item = self._source_port._item
            start = source_port_item.scenePos()
            out_rect = source_port_item.boundingRect()
            out_w, out_h = out_rect.width(), out_rect.height()
            self._start_p = QtCore.QPointF(start.x()+out_w/2-1, start.y()+out_h/2)
        else:
            self._start_p = QtCore.QPointF()
        if end_point:
            self._end_p = QtCore.QPointF(end_point)
        elif self._target_port:
            target_port_item = self._target_port._item
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
        super(_QtConnection, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if self._hover_enable is True:
            self._hover_flag = False
            self._hover_region = None
            self.update()
        super(_QtConnection, self).hoverLeaveEvent(event)

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

        arrow_p1 = self._mid_p - QtCore.QPointF(
            self._arrow_size * math.cos(self._tangent_angle - math.radians(30)),
            self._arrow_size * math.sin(self._tangent_angle - math.radians(30)),
        )
        arrow_p2 = self._mid_p - QtCore.QPointF(
            self._arrow_size * math.cos(self._tangent_angle+math.radians(30)),
            self._arrow_size * math.sin(self._tangent_angle+math.radians(30)),
        )

        arrow_head = QtGui.QPolygonF([self._mid_p, arrow_p1, arrow_p2])
        painter.setPen(arrow_color)
        painter.setBrush(arrow_color)
        painter.drawPolygon(arrow_head)

        painter.restore()

    def _get_source_point(self):
        if self._source_port:
            source_port_item = self._source_port._item
            start = source_port_item.scenePos()
            out_rect = source_port_item.boundingRect()
            out_w, out_h = out_rect.width(), out_rect.height()
            return QtCore.QPointF(start.x()+out_w/2-2, start.y()+out_h/2)
        else:
            return QtCore.QPointF(0, 0)

    def _get_target_point(self):
        if self._target_port:
            target_port_item = self._target_port._item
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


# port
class _QtPort(
    QtWidgets.QGraphicsPathItem,
    _base._QtSbjBase,
):
    MODEL_CLS = None

    def __init__(self, parent, w, h):
        super(_QtPort, self).__init__(parent)
        self.setZValue(1)
        self.setFlags(self.ItemSendsScenePositionChanges)

        self.setAcceptHoverEvents(True)

        self._set_color(_base._QtColors.PortBorder)

        self.edges = []

        self._model = self.MODEL_CLS(self)

        self._hover_flag = False
        self._w, self._h = w, h

        self._name_aux = _QtTextAux('', self)
        self._name_aux.hide()

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemScenePositionHasChanged:
            connections = self._model.get_connections()
            for i_model in connections:
                i_model.update_v()
        return super(_QtPort, self).itemChange(change, value)

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
        super(_QtPort, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._hover_flag = False
        self._name_aux.hide()
        self.update()
        super(_QtPort, self).hoverLeaveEvent(event)

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


class _QtInputPort(_QtPort):
    MODEL_CLS = _model._InputPortModel

    SBJ_TYPE = _base._QtSbjTypes.InputPort

    def __init__(self, *args, **kwargs):
        super(_QtInputPort, self).__init__(*args, **kwargs)

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


class _QtOutputPort(_QtPort):
    MODEL_CLS = _model._OutputPortModel

    SBJ_TYPE = _base._QtSbjTypes.OutputPort

    def __init__(self, *args, **kwargs):
        super(_QtOutputPort, self).__init__(*args, **kwargs)
    
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


class _QtTextAux(
    QtWidgets.QGraphicsTextItem,
    _base._QtSbjBase,
):
    SBJ_TYPE = _base._QtSbjTypes.Aux

    def __init__(self, *args):
        super(_QtTextAux, self).__init__(*args)
        self.setDefaultTextColor(QtGui.QColor(223, 223, 223))
        self._font = gui_qt_core.QtFont.generate(size=8)
        self.setFont(self._font)
        self._frame_h = 20
        self.setAcceptHoverEvents(False)


class _QtImageAux(
    QtWidgets.QGraphicsRectItem,
    _base._QtSbjBase,
):
    SBJ_TYPE = _base._QtSbjTypes.Aux

    def __init__(self, *args):
        super(_QtImageAux, self).__init__(*args)
        self.setAcceptHoverEvents(False)
        self.setOpacity(.5)

    def paint(self, painter, option, widget=None):
        painter.save()

        rect = self.rect()

        gui_qt_core.QtItemDrawBase._draw_icon_by_file(
            painter, rect, gui_core.GuiIcon.get('bypass')
        )

        painter.restore()


# node
class _QtNode(
    QtWidgets.QGraphicsRectItem,
    _base._QtSbjBase,
):
    ActionFlags = _base._ActionFlags

    SBJ_TYPE = _base._QtSbjTypes.Node

    def __init__(self, *args):
        super(_QtNode, self).__init__(*args)
        self.setZValue(1)

        self.setFlags(
            self.ItemIsMovable |
            self.ItemIsSelectable |
            self.ItemSendsScenePositionChanges
        )

        self.setAcceptHoverEvents(True)

        self._name_aux = _QtTextAux('', self)
        self._bypass_aux = _QtImageAux(self)
        self._bypass_aux.hide()
        self._bypass_aux.setZValue(12)

        self._model = _model._NodeModel(self)
        self._model._gui_data.port.input.cls = _QtInputPort
        self._model._gui_data.port.output.cls = _QtOutputPort

    def __str__(self):
        return 'Node(path={})'.format(
            self._model.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemScenePositionHasChanged:
            self._model._data.options.position.x = self.x()
            self._model._data.options.position.y = self.y()
        return super(_QtNode, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        self._model._update_hover(True)
        self.update()
        super(_QtNode, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._model._update_hover(False)
        self.update()
        super(_QtNode, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            point = event.pos()
            if self._model._check_viewed(point) is True:
                self._model.set_action_flag(self.ActionFlags.NodeViewedClick)
            elif self._model._check_edited(point) is True:
                self._model.set_action_flag(self.ActionFlags.NodeEditedClick)
        super(_QtNode, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self._model.is_action_flag_matching(self.ActionFlags.NodeViewedClick):
                self._model._on_swap_viewed()
            elif self._model.is_action_flag_matching(self.ActionFlags.NodeEditedClick):
                self._model._on_swap_edited()

        self._model.clear_action_flag()
        super(_QtNode, self).mouseReleaseEvent(event)

    def paint(self, painter, option, widget=None):
        self._model.draw(painter, option)


class _QtBackdrop(
    QtWidgets.QGraphicsRectItem,
    _base._QtSbjBase,
):
    ActionFlags = _base._ActionFlags

    SBJ_TYPE = _base._QtSbjTypes.Backdrop

    def __init__(self, *args):
        super(_QtBackdrop, self).__init__(*args)
        self.setZValue(-1)

        self.setFlags(
            # do not add movable
            # self.ItemIsMovable |
            self.ItemIsSelectable
        )

        self._model = _model._BackdropModel(self)

    def __str__(self):
        return 'Backdrop(path={})'.format(
            self._model.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def hoverEnterEvent(self, event):
        self._model._update_hover(True)
        self.update()
        super(_QtBackdrop, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._model._update_hover(False)
        self.update()
        super(_QtBackdrop, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            point = event.pos()
            if self._model._check_move(point) is True:
                self._model.set_action_flag(self.ActionFlags.GroupPressClick)
                self._model.do_move_start(event)
            elif self._model._check_resize(point) is True:
                self._model.set_action_flag(self.ActionFlags.GroupResizePressClick)
                self._model.do_resize_start(event)
            else:
                event.ignore()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self._model.is_action_flag_matching(
                self.ActionFlags.GroupPressClick, self.ActionFlags.GroupPressMove,
            ):
                self._model.set_action_flag(self.ActionFlags.GroupPressMove)
                self._model.do_move(event)
            elif self._model.is_action_flag_matching(
                self.ActionFlags.GroupResizePressClick, self.ActionFlags.GroupResizePressMove,
            ):
                self._model.set_action_flag(self.ActionFlags.GroupResizePressMove)
                self._model.do_resize_move(event)
            else:
                event.ignore()
        super(_QtBackdrop, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self._model.is_action_flag_matching(
                self.ActionFlags.GroupPressClick, self.ActionFlags.GroupPressMove,
            ):
                self._model.do_move_end()
            elif self._model.is_action_flag_matching(
                self.ActionFlags.GroupResizePressClick, self.ActionFlags.GroupResizePressMove,
            ):
                self._model.do_resize_end()
            else:
                event.ignore()
        self._model.clear_action_flag()

    def paint(self, painter, option, widget=None):
        self._model.draw(painter, option)


class _QtScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args):
        super(_QtScene, self).__init__(*args)

        self._model = None

    def _set_model(self, model):
        self._model = model

    def _get_items_by_rect(self, x, y, w, h):
        return self.items(QtCore.QRectF(x, y, w, h), QtCore.Qt.IntersectsItemBoundingRect)


class _QtQRubberBand(QtWidgets.QRubberBand):
    def __init__(self, *args, **kwargs):
        super(_QtQRubberBand, self).__init__(*args, **kwargs)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        x, y, w, h = 0, 0, self.rect().width(), self.rect().height()
        r, g, b, a = gui_core.GuiRgba.LightAzureBlue
        painter.setPen(QtGui.QColor(r, g, b))
        painter.setBrush(QtGui.QColor(r, g, b, 31))
        painter.drawRect(QtCore.QRect(x, y, w-1, h-1))


# graph
class _QtSceneGraph(QtWidgets.QGraphicsView):
    ActionFlags = _base._ActionFlags

    QT_MENU_CLS = gui_qt_widgets.QtMenu

    def _map_from_global(self, point):
        point = self.mapFromGlobal(point)
        return self._get_scaled_point(point.x(), point.y())

    def _get_scaled_point(self, x, y):
        transform = self.transform()
        inverted, success = transform.inverted()
        if success:
            return inverted.map(QtCore.QPointF(x, y))
        return self.mapToScene(0, 0)

    def __init__(self, *args):
        super(_QtSceneGraph, self).__init__(*args)
        self.setAutoFillBackground(True)
        qt_palette = gui_qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setStyleSheet(gui_qt_core.QtStyle.get('QGraphicsView'))

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setDragMode(self.RubberBandDrag)
        self.setTransformationAnchor(self.NoAnchor)
        self.setResizeAnchor(self.NoAnchor)
        self.setInteractive(True)
        self.setDragMode(self.NoDrag)

        self._rubber_band = _QtQRubberBand(QtWidgets.QRubberBand.Rectangle, self)

        self._model = _model._SceneModel(self)
        self._model._gui_data.node.cls = _QtNode
        self._model._gui_data.backdrop.cls = _QtBackdrop
        self._model._gui_data.connection.cls = _QtConnection

        self._drag_start_point = None
        self._drag_port = None
        self._drag_connection = None
        self._drag_threshold = 10

        # undo
        self._undo_stack = QtWidgets.QUndoStack()
        self._undo_stack.setUndoLimit(100)
        self._undo_button = None
        self._undo_action = self._undo_stack.createUndoAction(self, 'undo')
        self._undo_action.setShortcut(
            QtGui.QKeySequence(
                QtCore.Qt.CTRL+QtCore.Qt.Key_Z
            )
        )
        self.addAction(self._undo_action)

        # redo
        self._redo_action = self._undo_stack.createRedoAction(self, 'redo')
        self._redo_button = None
        self._redo_action.setShortcut(
            QtGui.QKeySequence(
                QtCore.Qt.CTRL+QtCore.Qt.SHIFT+QtCore.Qt.Key_Z
            )
        )
        self.addAction(self._redo_action)
        actions = [
            # delete
            (self._model._on_delete_action, 'Delete'),
            # copy
            (self._model._on_copy_action, 'Ctrl+C'),
            # cut
            (self._model._on_cut_action, 'Ctrl+X'),
            # paste
            (self._model._on_paste_action, 'Ctrl+V'),
            # bypass
            (self._model._on_bypass_action, 'D'),
        ]
        for i_fnc, i_shortcut in actions:
            i_action = QtWidgets.QAction(self)
            # noinspection PyUnresolvedReferences
            i_action.triggered.connect(
                i_fnc
            )
            i_action.setShortcut(
                QtGui.QKeySequence(
                    i_shortcut
                )
            )
            self.addAction(i_action)

        self.installEventFilter(self)

    def _accept_source_connect(self, item):
        if isinstance(item, _QtInputPort):
            source_port = self._drag_port
            target_port = item._model
            if target_port.has_source():
                source_port_old = target_port.get_source()
                self._model._push_reconnect_source_cmd(
                    source_port_old, target_port, source_port
                )
            else:
                self._model._push_connect_cmd(source_port, target_port)

        self.scene().removeItem(self._drag_connection._item)

        self._drag_connection = None
        self._drag_port = None

    def _accept_target_connect(self, item):
        if isinstance(item, _QtOutputPort):
            source_port = item._model
            target_port = self._drag_port
            if target_port.has_source():
                source_port_old = target_port.get_source()
                self._model._push_reconnect_source_cmd(
                    source_port_old, target_port, source_port
                )
            else:
                self._model._push_connect_cmd(source_port, target_port)

        self.scene().removeItem(self._drag_connection._item)
        self._drag_connection = None
        self._drag_port = None

    def _cancel_connect(self):
        if self._drag_connection is None:
            return

        self.scene().removeItem(self._drag_connection._item)
        self._drag_connection = None
        self._drag_port = None

    def _accept_source_reconnect(self, item):
        if isinstance(item, _QtOutputPort):
            source_port = self._drag_connection.get_source()
            target_port = self._drag_connection.get_target()
            source_port_new = item._model
            if source_port != source_port_new:
                self._model._push_reconnect_source_cmd(
                    source_port, target_port, source_port_new
                )
            else:
                self._drag_connection.reset_status()
                self._drag_connection.update_v()
        else:
            source_port = self._drag_connection.get_source()
            target_port = self._drag_connection.get_target()
            self._model._push_disconnect_cmd(source_port, target_port)

        self._drag_connection = None

    def _accept_target_reconnect(self, item):
        if isinstance(item, _QtInputPort):
            source_port = self._drag_connection.get_source()
            target_port = self._drag_connection.get_target()
            target_port_new = item._model
            if target_port != target_port_new:
                self._model._push_reconnect_target_cmd(
                    source_port, target_port, target_port_new
                )
            else:
                self._drag_connection.reset_status()
                self._drag_connection.update_v()
        else:
            source_port = self._drag_connection.get_source()
            target_port = self._drag_connection.get_target()
            self._model._push_disconnect_cmd(source_port, target_port)

        self._drag_connection = None

    def _cancel_reconnect(self):
        self._drag_connection = None

    def mousePressEvent(self, event):
        if (
            event.button() == QtCore.Qt.LeftButton
            and event.modifiers() in (QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier)
        ):
            scene_pos = self.mapToScene(event.pos())
            selection_area = QtGui.QPainterPath()
            selection_area.addRect(QtCore.QRectF(scene_pos.x() - 1, scene_pos.y() - 1, 2, 2))
            items_under_cursor = self.scene().items(selection_area, QtCore.Qt.IntersectsItemShape)
            if items_under_cursor:
                for item in items_under_cursor:
                    if isinstance(item, _QtNode):
                        if event.modifiers() == QtCore.Qt.ShiftModifier:
                            item.setSelected(True)
                        elif event.modifiers() == QtCore.Qt.ControlModifier:
                            item.setSelected(False)
            else:
                self._model.set_action_flag(self.ActionFlags.RectSelectPressClick)
                self._model._do_rect_selection_start(event)

        elif event.button() == QtCore.Qt.LeftButton:
            point = event.pos()
            item = self.itemAt(point)
            p = self._get_scaled_point(point.x(), point.y())
            self._drag_start_point = point
            # port
            if self._model.is_action_sub_flag_matching(self.ActionFlags.PortSourceHoverMove):
                self._model.clear_action_sub_flag()
                self._accept_source_connect(item)
            elif self._model.is_action_sub_flag_matching(self.ActionFlags.PortTargetHoverMove):
                self._model.clear_action_sub_flag()
                self._accept_target_connect(item)
            # connection
            elif self._model.is_action_sub_flag_matching(self.ActionFlags.ConnectionSourceHoverMove):
                self._model.clear_action_sub_flag()
                self._accept_source_reconnect(item)
            elif self._model.is_action_sub_flag_matching(self.ActionFlags.ConnectionTargetHoverMove):
                self._model.clear_action_sub_flag()
                self._accept_target_reconnect(item)
            else:
                # node
                if isinstance(item, _QtNode):
                    super(_QtSceneGraph, self).mousePressEvent(event)
                    self._model.set_action_flag(self.ActionFlags.NodePressClick)
                    self._model._do_node_move_start(event)
                # port
                elif isinstance(item, _QtOutputPort):
                    self._model.set_action_flag(self.ActionFlags.PortSourcePressClick)
                    self._model.set_action_sub_flag(self.ActionFlags.PortSourcePressClick)
                    self._drag_port = item._model
                    connection_item = _QtConnection(source_port=self._drag_port)
                    self._drag_connection = connection_item._model
                    self.scene().addItem(connection_item)
                    self._drag_connection.update_v(end_point=p)
                elif isinstance(item, _QtInputPort):
                    self._model.set_action_flag(self.ActionFlags.PortTargetPressClick)
                    self._model.set_action_sub_flag(self.ActionFlags.PortTargetPressClick)
                    self._drag_port = item._model
                    connection_item = _QtConnection(target_port=self._drag_port)
                    self._drag_connection = connection_item._model
                    self.scene().addItem(connection_item)
                    self._drag_connection.update_v(start_point=p)
                # connection
                elif isinstance(item, _QtConnection):
                    self._drag_connection = item._model
                    region = item._get_region(p)
                    if region == _QtConnection.Regions.Source:
                        self._model.set_action_flag(self.ActionFlags.ConnectionSourcePressClick)
                        self._model.set_action_sub_flag(self.ActionFlags.ConnectionSourcePressClick)
                        self._drag_connection.update_v(start_point=p)
                    elif region == _QtConnection.Regions.Target:
                        self._model.set_action_flag(self.ActionFlags.ConnectionTargetPressClick)
                        self._model.set_action_sub_flag(self.ActionFlags.ConnectionTargetPressClick)
                        self._drag_connection.update_v(end_point=p)
                elif isinstance(item, _QtBackdrop):
                    if item._model._check_scene_move(p):
                        super(_QtSceneGraph, self).mousePressEvent(event)
                    elif item._model._check_scene_resize(p):
                        super(_QtSceneGraph, self).mousePressEvent(event)
                    else:
                        self._model.set_action_flag(self.ActionFlags.RectSelectPressClick)
                        self._model._do_rect_selection_start(event)
                        super(_QtSceneGraph, self).mousePressEvent(event)
                elif isinstance(item, _QtImageAux):
                    super(_QtSceneGraph, self).mousePressEvent(event)
                else:
                    self._model.set_action_flag(self.ActionFlags.RectSelectPressClick)
                    self._model._do_rect_selection_start(event)
                    super(_QtSceneGraph, self).mousePressEvent(event)
        elif event.button() == QtCore.Qt.MidButton:
            self._model.set_action_flag(self.ActionFlags.GraphTrackClick)
            self._model._do_track_start(event)
        else:
            super(_QtSceneGraph, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.NoButton:
            # port
            if self._model.is_action_sub_flag_matching(
                self.ActionFlags.PortSourcePressClick, self.ActionFlags.PortSourceHoverMove
            ):
                if self._drag_connection is not None:
                    point = event.pos()
                    item = self.itemAt(point)
                    p = self._get_scaled_point(point.x(), point.y())

                    if isinstance(item, _QtInputPort):
                        self._drag_connection.to_correct_status()
                    else:
                        self._drag_connection.reset_status()

                    self._drag_connection.update_v(end_point=p)
                    self._model.set_action_sub_flag(self.ActionFlags.PortSourceHoverMove)
            elif self._model.is_action_sub_flag_matching(
                self.ActionFlags.PortTargetPressClick, self.ActionFlags.PortTargetHoverMove
            ):
                if self._drag_connection is not None:
                    point = event.pos()
                    item = self.itemAt(point)
                    p = self._get_scaled_point(point.x(), point.y())
                    if isinstance(item, _QtOutputPort):
                        self._drag_connection.to_correct_status()
                    else:
                        self._drag_connection.reset_status()

                    self._drag_connection.update_v(start_point=p)
                    self._model.set_action_sub_flag(self.ActionFlags.PortTargetHoverMove)
            # connections
            elif self._model.is_action_sub_flag_matching(
                self.ActionFlags.ConnectionSourcePressClick, self.ActionFlags.ConnectionSourceHoverMove
            ):
                if self._drag_connection is not None:
                    point = event.pos()
                    item = self.itemAt(point)
                    p = self._get_scaled_point(point.x(), point.y())

                    if isinstance(item, _QtOutputPort):
                        self._drag_connection.to_correct_status()
                    else:
                        self._drag_connection.reset_status()

                    self._drag_connection.update_v(start_point=p)
                    self._model.set_action_sub_flag(self.ActionFlags.ConnectionSourceHoverMove)
            elif self._model.is_action_sub_flag_matching(
                self.ActionFlags.ConnectionTargetPressClick, self.ActionFlags.ConnectionTargetHoverMove
            ):
                if self._drag_connection is not None:
                    point = event.pos()
                    item = self.itemAt(point)
                    p = self._get_scaled_point(point.x(), point.y())
                    if isinstance(item, _QtInputPort):
                        self._drag_connection.to_correct_status()
                    else:
                        self._drag_connection.reset_status()

                    self._drag_connection.update_v(end_point=p)
                    self._model.set_action_sub_flag(self.ActionFlags.ConnectionTargetHoverMove)
            super(_QtSceneGraph, self).mouseMoveEvent(event)
        elif event.buttons() == QtCore.Qt.LeftButton:
            point = event.pos()
            item = self.itemAt(point)
            p = self._get_scaled_point(point.x(), point.y())
            # node
            if self._model.is_action_flag_matching(
                self.ActionFlags.NodePressClick, self.ActionFlags.NodePressMove
            ):
                super(_QtSceneGraph, self).mouseMoveEvent(event)
                self._model._do_node_move(event)
            # port
            elif self._model.is_action_flag_matching(
                self.ActionFlags.PortSourcePressClick, self.ActionFlags.PortSourcePressMove
            ):
                if isinstance(item, _QtInputPort):
                    self._drag_connection.to_correct_status()
                else:
                    self._drag_connection.reset_status()

                self._drag_connection.update_v(end_point=p)
                self._model.set_action_flag(self.ActionFlags.PortSourcePressMove)
            elif self._model.is_action_flag_matching(
                self.ActionFlags.PortTargetPressClick, self.ActionFlags.PortTargetPressMove
            ):
                if isinstance(item, _QtOutputPort):
                    self._drag_connection.to_correct_status()
                else:
                    self._drag_connection.reset_status()

                self._drag_connection.update_v(start_point=p)
                self._model.set_action_flag(self.ActionFlags.PortTargetPressMove)
            # connection
            elif self._model.is_action_flag_matching(
                self.ActionFlags.ConnectionSourcePressClick, self.ActionFlags.ConnectionSourcePressMove
            ):
                if isinstance(item, _QtOutputPort):
                    self._drag_connection.to_correct_status()
                else:
                    self._drag_connection.reset_status()

                self._drag_connection.update_v(start_point=p)
                self._model.set_action_flag(self.ActionFlags.ConnectionSourcePressMove)
            elif self._model.is_action_flag_matching(
                self.ActionFlags.ConnectionTargetPressClick, self.ActionFlags.ConnectionTargetPressMove
            ):
                if isinstance(item, _QtInputPort):
                    self._drag_connection.to_correct_status()
                else:
                    self._drag_connection.reset_status()

                self._drag_connection.update_v(end_point=p)
                self._model.set_action_flag(self.ActionFlags.ConnectionTargetPressMove)
            # rect selection
            elif self._model.is_action_flag_matching(
                self.ActionFlags.RectSelectPressClick, self.ActionFlags.RectSelectPressMove
            ):
                self._model.set_action_flag(self.ActionFlags.RectSelectPressMove)
                self._model._do_rect_selection_move(event)
            else:
                super(_QtSceneGraph, self).mouseMoveEvent(event)
        elif event.buttons() == QtCore.Qt.MidButton:
            if self._model.is_action_flag_matching(
                self.ActionFlags.GraphTrackClick,
                self.ActionFlags.GraphTrackMove
            ):
                self._model.set_action_flag(self.ActionFlags.GraphTrackMove)
                self._model._do_track_move(event)
        else:
            super(_QtSceneGraph, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            item = self.itemAt(event.pos())
            # node
            if self._model.is_action_flag_matching(
                self.ActionFlags.NodePressClick, self.ActionFlags.NodePressMove
            ):
                super(_QtSceneGraph, self).mouseReleaseEvent(event)
                self._model._do_node_move_end()
            # connect
            elif self._model.is_action_flag_matching(self.ActionFlags.PortSourcePressMove):
                self._model.clear_action_sub_flag()
                self._accept_source_connect(item)
            elif self._model.is_action_flag_matching(self.ActionFlags.PortTargetPressMove):
                self._model.clear_action_sub_flag()
                self._accept_target_connect(item)
            # reconnect
            elif self._model.is_action_flag_matching(self.ActionFlags.ConnectionSourcePressMove):
                self._model.clear_action_sub_flag()
                self._accept_source_reconnect(item)
            elif self._model.is_action_flag_matching(self.ActionFlags.ConnectionTargetPressMove):
                self._model.clear_action_sub_flag()
                self._accept_target_reconnect(item)
            # rect selection
            elif self._model.is_action_flag_matching(self.ActionFlags.RectSelectPressMove):
                self._model._do_rect_selection_end(event)
            else:
                super(_QtSceneGraph, self).mouseReleaseEvent(event)
        # track
        elif event.button() == QtCore.Qt.MidButton:
            if self._model.is_action_flag_matching(
                self.ActionFlags.GraphTrackClick,
                self.ActionFlags.GraphTrackMove
            ):
                self._model._do_tack_end()
        else:
            super(_QtSceneGraph, self).mouseReleaseEvent(event)

        self._rubber_band.hide()
        self._model.clear_action_flag()

    def wheelEvent(self, event):
        self._model._do_zoom(event)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            pass
        return False

    def contextMenuEvent(self, event):
        menu = None

        menu_data = self._model.get_menu_data()
        menu_content = self._model.get_menu_content()
        menu_data_generate_fnc = self._model.get_menu_data_generate_fnc()
        menu_name_dict = self._model.get_menu_name_dict()

        if menu_content:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_content_(menu_content, append=True)

        if menu_data:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_data_(menu_data)

        if menu_data_generate_fnc:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_data_(menu_data_generate_fnc())

        # data from item
        item = self.itemAt(event.pos())
        if item:
            if item.SBJ_TYPE in {_base._QtSbjTypes.Node, _base._QtSbjTypes.Backdrop}:
                item_menu_data = item._model.get_menu_data()
                item_menu_content = item._model.get_menu_content()
                item_menu_data_generate_fnc = item._model.get_menu_data_generate_fnc()
                item_menu_name_dict = item._model.get_menu_name_dict()
                menu_name_dict.update(item_menu_name_dict)

                if item_menu_content:
                    if menu is None:
                        menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                    menu._set_menu_content_(item_menu_content, append=True)

                if item_menu_data:
                    if menu is None:
                        menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                    menu._set_menu_data_(item_menu_data)

                if item_menu_data_generate_fnc:
                    if menu is None:
                        menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                    menu._set_menu_data_(item_menu_data_generate_fnc())

                if menu is not None:
                    menu._update_menu_name_dict_(item_menu_name_dict)

        if menu is not None:
            menu._popup_start_()


class QtSceneGraphWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSceneGraphWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._mrg = 4

        self._grid_lot = QtWidgets.QGridLayout(self)
        self._grid_lot.setContentsMargins(*[self._mrg]*4)
        self._grid_lot.setSpacing(2)

        self._view = _QtSceneGraph()
        self._grid_lot.addWidget(self._view, 0, 0, 1, 1)
        self._view.setFocusProxy(self)
        self._model = self._view._model

        self._scene = _QtScene()
        self._view.setScene(self._scene)
        self._scene._set_model(self._model)
        self._scene.setSceneRect(-5000, -5000, 10000, 10000)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        mrg = self._mrg
        x, y, w, h = 0, 0, self.width(), self.height()

        f_x, f_y, f_w, f_h = x+1, y+1, w-2, h-2
        is_focus = self.hasFocus()

        pen = QtGui.QPen(QtGui.QColor(*[(71, 71, 71, 255), (95, 95, 95, 255)][is_focus]))
        pen_width = [1, 2][is_focus]

        pen.setWidth(pen_width)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(*gui_core.GuiRgba.Dim))
        painter.drawRect(f_x, f_y, f_w, f_h)
