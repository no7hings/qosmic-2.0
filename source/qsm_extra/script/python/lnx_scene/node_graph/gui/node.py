# coding:utf-8
from lxgui.qt.core.wrap import *

from ...core import base as _scn_cor_base

from ..core import base as _cor_base

from ..core import action as _cor_action

from . import aux_ as _aux

from . import port as _port


# node
class _AbsNodeGui(
    QtWidgets.QGraphicsRectItem,
    _cor_base._SbjGuiBase
):
    def __init__(self, *args, **kwargs):
        super(_AbsNodeGui, self).__init__(*args)


# standard
class StandardNodeGui(_AbsNodeGui):
    ActionFlags = _cor_action.ActionFlags

    ENTITY_TYPE = _scn_cor_base.EntityTypes.Node

    MODEL_CLS = None

    def __init__(self, *args, **kwargs):
        super(StandardNodeGui, self).__init__(*args)
        self.setZValue(1)

        self.setFlags(
            self.ItemIsMovable |
            self.ItemIsSelectable |
            self.ItemSendsScenePositionChanges
        )

        self.setAcceptHoverEvents(True)

        self._name_aux = _aux.TextAuxGui('', self)

        self._add_input_aux = _aux.AddInputAuxGui(self)
        self._add_input_aux.hide()
        self._add_input_aux.setZValue(2)

        self._bypass_aux = _aux.IconAuxGui(self)
        self._bypass_aux.hide()
        self._bypass_aux.setZValue(3)
        self._bypass_aux.setOpacity(.5)

        self._model = self.MODEL_CLS(self)
        self._model._builtin_data.port.input.gui_cls = _port.InputGui
        self._model._builtin_data.port.output.gui_cls = _port.OutputGui

        # glow_effect = QtWidgets.QGraphicsDropShadowEffect()
        # glow_effect.setBlurRadius(20)
        # glow_effect.setOffset(0, 0)
        # glow_effect.setColor(QtGui.QColor(255, 255, 0, 255))
        #
        # self.setGraphicsEffect(glow_effect)

    def __str__(self):
        return 'Node(path={})'.format(
            self._model.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemScenePositionHasChanged:
            # update position option
            self._model._data.options.position.x = self.x()
            self._model._data.options.position.y = self.y()
        return super(StandardNodeGui, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        self._model._update_hover(True)
        self.update()
        super(StandardNodeGui, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._model._update_hover(False)
        self.update()
        super(StandardNodeGui, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            point = event.pos()
            if self._model._check_viewed(point) is True:
                self._model._on_swap_viewed()
            elif self._model._check_edited(point) is True:
                self._model._on_swap_edited()
        super(StandardNodeGui, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._model.clear_action_flag()
        super(StandardNodeGui, self).mouseReleaseEvent(event)

    def paint(self, painter, option, widget=None):
        self._model.draw(painter, option)


# imaging
class ImagingNodeGui(
    StandardNodeGui
):
    def __init__(self, *args, **kwargs):
        super(ImagingNodeGui, self).__init__(*args, **kwargs)


# backdrop
class BackdropGui(_AbsNodeGui):
    ActionFlags = _cor_action.ActionFlags

    ENTITY_TYPE = _scn_cor_base.EntityTypes.Backdrop

    def __init__(self, *args, **kwargs):
        super(BackdropGui, self).__init__(*args)
        self.setZValue(-1)

        self.setFlags(
            # do not add movable
            # self.ItemIsMovable |
            self.ItemIsSelectable
        )

        self._model = self.MODEL_CLS(self)

    def __str__(self):
        return 'Backdrop(path={})'.format(
            self._model.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def hoverEnterEvent(self, event):
        self._model._update_hover(True)
        self.update()
        super(BackdropGui, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._model._update_hover(False)
        self.update()
        super(BackdropGui, self).hoverLeaveEvent(event)

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
        super(BackdropGui, self).mouseMoveEvent(event)

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
