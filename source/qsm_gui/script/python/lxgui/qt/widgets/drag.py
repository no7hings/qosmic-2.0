# coding=utf-8
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core


class QtDrag(QtGui.QDrag):
    released = qt_signal(tuple)

    ACTION_MAPPER = {
        QtCore.Qt.IgnoreAction: gui_core.GuiDragFlag.Ignore,
        QtCore.Qt.CopyAction: gui_core.GuiDragFlag.Copy,
        QtCore.Qt.MoveAction: gui_core.GuiDragFlag.Move
    }

    def __init__(self, *args, **kwargs):
        super(QtDrag, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self._current_action = QtCore.Qt.IgnoreAction
        self.actionChanged.connect(self._update_action_)
        self._drag_count = 1

    def _set_drag_count_(self, c):
        self._drag_count = c

    def _do_drag_copy_(self, point_offset):
        """
        text/plain ArnoldSceneBake
        nodegraph/nodes ArnoldSceneBake
        nodegraph/noderefs ArnoldSceneBake
        'python/text': 'NodegraphAPI.GetNode('ArnoldSceneBake')',
        python/getParameters NodegraphAPI.GetNode('ArnoldSceneBake').getParameters()
        'python/GetGeometryProducer': 'Nodes3DAPI.GetGeometryProducer(NodegraphAPI.GetNode(\'ArnoldSceneBake\'))',
        'python/GetRenderProducer': Nodes3DAPI.GetRenderProducer(NodegraphAPI.GetNode('ArnoldSceneBake'), useMaxSamples=True)
        """
        drag = self
        widget = self.parent()

        c = self._drag_count
        c = min(c, 10)
        w, h = widget.width(), widget.height()
        o_x, o_y = 0, 4
        c_w, c_h = w+(c-1)*o_x, h+(c-1)*o_y
        p = QtGui.QPixmap(c_w, c_h)
        painter = gui_qt_core.QtPainter(p)
        rect = QtCore.QRect(0, 0, c_w, c_h)
        painter.fillRect(rect, gui_qt_core.QtBorderColors.Button)
        for i in range(c):
            i_p = QtGui.QPixmap(w, h)
            i_rect = QtCore.QRect(i*o_x, i*o_y, w, h)
            i_p.fill(gui_qt_core.QtBorderColors.Button)
            widget.render(i_p)
            painter.drawPixmap(i_rect, i_p)

        painter.end()
        drag.setPixmap(p)
        drag.setHotSpot(point_offset)
        drag.exec_(QtCore.Qt.CopyAction)

    def _do_drag_move_(self, point_offset):
        drag = self
        widget = self.parent()

        c = self._drag_count
        c = min(c, 10)
        w, h = widget.width(), widget.height()
        o_x, o_y = 0, 4
        c_w, c_h = w+(c-1)*o_x, h+(c-1)*o_y
        p = QtGui.QPixmap(c_w, c_h)
        painter = gui_qt_core.QtPainter(p)
        rect = QtCore.QRect(0, 0, c_w, c_h)
        painter.fillRect(rect, gui_qt_core.QtBorderColors.Button)
        for i in range(c):
            i_p = QtGui.QPixmap(w, h)
            i_rect = QtCore.QRect(i*o_x, i*o_y, w, h)
            i_p.fill(gui_qt_core.QtBorderColors.Button)
            widget.render(i_p)
            painter.drawPixmap(i_rect, i_p)

        painter.end()
        drag.setPixmap(p)
        drag.setHotSpot(point_offset)
        # drag.setDragCursor()
        drag.exec_(QtCore.Qt.MoveAction)

    # noinspection PyUnusedLocal
    def _update_action_(self, *args, **kwargs):
        self._current_action = args[0]

    def _do_release_(self):
        if self._current_action in self.ACTION_MAPPER:
            self.released.emit(
                (self.ACTION_MAPPER[self._current_action], self.mimeData())
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.DeferredDelete:
                self._do_release_()
        return False


class QtDragForTreeItem(QtGui.QDrag):
    def __init__(self, *args, **kwargs):
        super(QtDragForTreeItem, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self._item = None
        self._index = 0

    def _do_drag_copy_(self, point_offset):
        #
        drag = self
        widget = self.parent()
        #
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.BusyCursor
        )
        #
        x, y = 0, 0
        w, h = 48, 20
        name_text = self._item._get_name_text_()
        name_w = widget.fontMetrics().width(name_text)
        w = 20+name_w+10
        p = QtGui.QPixmap(w, h)
        pnt = gui_qt_core.QtPainter(p)
        pnt.setFont(
            gui_qt_core.QtFonts.Button
        )
        icon = self._item.icon(self._index)
        i_f_w, i_f_h = 20, 20
        i_w, i_h = 16, 16
        frame_rect = QtCore.QRect(x, y, w, h)
        pnt._draw_frame_by_rect_(
            rect=frame_rect,
            background_color=gui_qt_core.QtBackgroundColors.Basic,
            border_color=gui_qt_core.QtBorderColors.Basic,
            border_width=2
        )
        icon_rect = QtCore.QRect(x+(i_f_w-i_w)/2, y+(i_f_h-i_h)/2, i_w, i_h)
        pixmap_ = icon.pixmap(QtCore.QSize(i_w, i_h))
        pnt.drawPixmap(icon_rect, pixmap_)
        text_rect = QtCore.QRect(x+i_f_w, y, w-i_f_w, h)
        pnt._draw_text_by_rect_(
            rect=text_rect,
            text=name_text,
            font_color=gui_qt_core.QtFontColors.Basic
        )
        #
        pnt.end()
        drag.setPixmap(p)
        drag.setHotSpot(point_offset)
        drag.exec_(QtCore.Qt.CopyAction)
        #
        QtWidgets.QApplication.restoreOverrideCursor()

    def _do_release_(self):
        pass

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.DeferredDelete:
                self._do_release_()
        return False

    # noinspection PyUnusedLocal
    def set_item(self, item, point):
        self._item = item
