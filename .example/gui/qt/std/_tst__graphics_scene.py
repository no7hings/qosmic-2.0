# coding:utf-8
import sys

from lxgui.qt.core.wrap import *


class S(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(S, self).__init__(*args, **kwargs)
        self._s = QtWidgets.QGraphicsScene()

        self.installEventFilter(self)

        self.setScene(self._s)

        self._l = QtWidgets.QHBoxLayout(self)

        i = QtWidgets.QGraphicsRectItem()
        i.setFlags(
            i.ItemIsMovable | i.ItemIsSelectable | i.ItemIsFocusScope
        )
        i.setRect(
            0, 0, 20, 20
        )
        self._s.addItem(
            i
        )

        self._p = QtCore.QPoint()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                pass
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Control:
                    self._set_action_mdf_flag_add_(
                        self.ActionFlag.KeyControlPress
                    )
                elif event.key() == QtCore.Qt.Key_Alt:
                    self._set_action_mdf_flag_add_(
                        self.ActionFlag.KeyAltPress
                    )
                elif event.key() == QtCore.Qt.Key_Shift:
                    self._set_action_mdf_flag_add_(
                        self.ActionFlag.KeyShiftPress
                    )
                elif event.key() == QtCore.Qt.Key_F:
                    self._set_action_frame_execute_(event)
                elif event.key() == QtCore.Qt.Key_L:
                    self._set_ng_action_graph_layout_select_execute_(event)
                elif event.key() == QtCore.Qt.Key_Z and event.modifiers() == QtCore.Qt.ControlModifier:
                    pass
                    # self._ng_undo_stack.undo()
            elif event.type() == QtCore.QEvent.KeyRelease:
                self._clear_action_modifier_flags_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(
                        self.ActionFlag.NGNodePressClick
                    ) is False:
                        self._set_action_flag_(
                            self.ActionFlag.RectSelectClick
                        )
                        self._set_action_rect_select_start_(event)
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._set_translate_start_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    pass
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    self._set_translate_execute_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_rect_select_end_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._set_translate_stop_(event)
                else:
                    event.ignore()
                #
                self._clear_all_action_flags_()
            #
            elif event.type() == QtCore.QEvent.Wheel:
                self._set_scale_(event)
        return False

    def _set_translate_start_(self, event):
        pass

    def _set_translate_execute_(self, event):
        pass

    def _set_translate_stop_(self, event):
        pass

    def _set_scale_(self, event):
        pass


app = QtWidgets.QApplication(sys.argv)

w = S()

w.setBaseSize(480, 480)
w.show()

sys.exit(app.exec_())

