# coding:utf-8
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

from ...core import base as _scn_cor_base

from ..core import base as _cor_base


# aux
class TextAuxGui(
    QtWidgets.QGraphicsTextItem,
    _cor_base._SbjGuiBase,
):
    ENTITY_TYPE = _scn_cor_base.EntityTypes.Aux

    def __init__(self, *args):
        super(TextAuxGui, self).__init__(*args)
        self.setDefaultTextColor(QtGui.QColor(223, 223, 223))
        self._font = gui_qt_core.QtFont.generate(size=10)
        self.setFont(self._font)
        self._frame_h = 20
        self.setAcceptHoverEvents(False)


class IconAuxGui(
    QtWidgets.QGraphicsRectItem,
    _cor_base._SbjGuiBase,
):
    ENTITY_TYPE = _scn_cor_base.EntityTypes.Aux

    def __init__(self, *args):
        super(IconAuxGui, self).__init__(*args)
        self.setAcceptHoverEvents(False)

    def paint(self, painter, option, widget=None):
        painter.save()

        rect = self.rect()

        gui_qt_core.QtItemDrawBase._draw_icon_by_file(
            painter, rect, gui_core.GuiIcon.get('bypass')
        )

        painter.restore()


class AddInputAuxGui(
    QtWidgets.QGraphicsRectItem,
    _cor_base._SbjGuiBase
):
    ENTITY_TYPE = _scn_cor_base.EntityTypes.Aux

    def __init__(self, *args):
        super(AddInputAuxGui, self).__init__(*args)

        self.setAcceptHoverEvents(True)

        self._set_color(_cor_base._QtColors.AddInput)

        self._hover_flag = False

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
        self.update()
        super(AddInputAuxGui, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._hover_flag = False
        self.update()
        super(AddInputAuxGui, self).hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
        painter.save()

        rect = self.rect()

        if self._hover_flag is True:
            pen = self._to_pen(QtGui.QColor(*gui_core.GuiRgba.LightOrange))
        else:
            pen = self.pen()

        border_color = pen.color()
        background_color = pen.color()

        gui_qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=rect,
            border_color=border_color,
            background_color=background_color,
            border_width=1,
            border_radius=2
        )

        gui_qt_core.QtItemDrawBase._draw_icon_by_file(
            painter, rect, gui_core.GuiIcon.get('add_input')
        )

        painter.restore()


class ActionAuxGui(
    QtWidgets.QGraphicsRectItem,
    _cor_base._SbjGuiBase
):
    ENTITY_TYPE = _scn_cor_base.EntityTypes.Aux

    def __init__(self, *args):
        super(ActionAuxGui, self).__init__(*args)
        self.setAcceptHoverEvents(False)
