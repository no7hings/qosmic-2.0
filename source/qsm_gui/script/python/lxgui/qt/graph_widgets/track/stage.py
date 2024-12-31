# coding=utf-8
import lxbasic.model as bsc_model
# gui
from .... import core as _gui_core
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ... import abstracts as _qt_abstracts


class QtTrackStage(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
):
    stage_changed = qt_signal()

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y, w, h = 0, 0, self.width(), self.height()

        self._frame_rect.setRect(
            x, y, w, h
        )

        start_x = self._stage_model.compute_start_x()
        track_w = self._stage_model.compute_width()
        txt_w = self._text_w
        txt_h = h/2

        self._track_start_rect.setRect(
            start_x-txt_w, y, txt_w, h
        )

        self._track_end_rect.setRect(
            start_x+track_w, y, txt_w, h
        )
        # trim
        self._left_trim_rect.setRect(
            x, y, max(start_x, 0), h
        )
        self._right_trim_rect.setRect(
            start_x+track_w, y, max(w-start_x+track_w, 0), h
        )

    def _update_stage_(self):
        self._stage_model.update()
        self.stage_changed.emit()

        self._refresh_widget_all_()

    def __init__(self, *args, **kwargs):
        super(QtTrackStage, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(40)

        self._init_action_base_def_(self)

        self._frame_rect = QtCore.QRect()

        self._text_w = 48

        self._track_start_rect = QtCore.QRect()
        self._track_end_rect = QtCore.QRect()

        self._left_trim_rect = QtCore.QRect()
        self._right_trim_rect = QtCore.QRect()

        self._graph = None

        self._stage_model = bsc_model.TrackWidgetStage()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            # track
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.PressClick)
                    # self._do_press_click_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._graph.eventFilter(self._graph, event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.NoButton:
                    pass
                    # self._do_hover_move_(event)
                elif event.buttons() == QtCore.Qt.LeftButton:
                    pass
                    # self._do_press_move_(event)
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    self._graph.eventFilter(self._graph, event)
                else:
                    event.ignore()
            # zoom
            elif event.type() == QtCore.QEvent.Wheel:
                self._graph.eventFilter(self._graph, event)
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)
        painter._set_antialiasing_(False)

        bottom_line = QtCore.QLine(self._frame_rect.bottomLeft(), self._frame_rect.bottomRight())

        painter._set_border_color_(_gui_core.GuiRgba.Dim)
        painter._set_background_color_(_gui_core.GuiRgba.Dim)
        painter.drawRect(self._frame_rect)
        # trim
        painter._draw_alternating_colors_by_rect_(
            self._left_trim_rect, [_gui_core.GuiRgba.LightBlack, _gui_core.GuiRgba.Transparent]
        )
        painter._draw_alternating_colors_by_rect_(
            self._right_trim_rect, [_gui_core.GuiRgba.LightBlack, _gui_core.GuiRgba.Transparent],
            x_offset=-self._right_trim_rect.x()
        )
        # frame range
        self._draw_track_frame_ranges_(painter)
        # line
        painter._set_border_color_(_gui_core.GuiRgba.Gray)
        painter.drawLine(bottom_line)

        painter._set_border_color_(_gui_core.GuiRgba.DarkWhite)
        painter._set_font_(_qt_core.QtFont.generate(size=10))

        painter.drawText(
            self._track_start_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            str(self._stage_model.track_start)
        )
        painter.drawText(
            self._track_end_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            str(self._stage_model.track_end)
        )

    def _draw_track_frame_ranges_(self, painter):
        h = self.height()

        tvl = self._stage_model.generate_travel()
        while tvl.is_valid():

            frame_range, model = tvl.current_data()

            is_start, is_end = tvl.is_start(), tvl.is_end()

            last_key = tvl.last_key()
            if last_key:
                last_node = self._stage_model.get_one_node(last_key)
            else:
                last_node = None

            next_key = tvl.next_key()
            if next_key:
                next_node = self._stage_model.get_one_node(next_key)
            else:
                next_node = None

            if model is not None:
                key = model.key
                frame_range_index = model.get_frame_range_index(frame_range)
                if frame_range_index > 0:
                    name = '{}({})'.format(key, frame_range_index)
                else:
                    name = key
                node = self._stage_model.get_one_node(key)
                if last_node is None:
                    last_last_key = tvl.last_last_key()
                    last_last_node = self._stage_model.get_one_node(last_last_key)
                    self._draw_frame_range_(
                        painter, last_last_node, node, next_node,
                        frame_range, name, model.rgb, h, is_start, is_end
                    )
                elif next_node is None:
                    next_next_key = tvl.next_next_key()
                    next_next_node = self._stage_model.get_one_node(next_next_key)
                    self._draw_frame_range_(
                        painter, last_node, node, next_next_node,
                        frame_range, name, model.rgb, h, is_start, is_end
                    )
                else:
                    self._draw_frame_range_(
                        painter, last_node, node, next_node,
                        frame_range, name, model.rgb, h, is_start, is_end
                    )
            else:
                name = '{}(missing)'.format(last_key)
                self._draw_frame_range_(
                    painter, last_node, None, next_node,
                    frame_range, name, (255, 0, 0), h, is_start, is_end
                )

            tvl.next()

    def _draw_frame_range_(
        self, painter, last_node, node, next_node,
        frame_range, text, rgb, h, is_start, is_end
    ):
        y = 0
        start, end = frame_range
        if start == end:
            time_text = str(start)
        else:
            time_text = '{}-{}'.format(start, end)

        count = end-start+1

        start_x = self._stage_model.compute_start_x_at(start)
        count_w = self._stage_model.compute_width_for(count)
        end_x = start_x+count_w
        #
        if node is not None:
            node_pre_blend = node._track_model.pre_blend
            node_pre_blend_w = self._stage_model.compute_width_for(node_pre_blend)
            node_post_blend_w = self._stage_model.compute_width_for(node._track_model.post_blend)
        else:
            node_pre_blend = last_node._track_model.pre_blend
            node_pre_blend_w = self._stage_model.compute_width_for(last_node._track_model.pre_blend)
            node_post_blend_w = self._stage_model.compute_width_for(last_node._track_model.post_blend)

        # last node
        if last_node is not None:
            last_node_post_blend = last_node._track_model.post_blend
            last_node_post_blend_w = self._stage_model.compute_width_for(last_node_post_blend)
        else:
            last_node_post_blend = 0
            last_node_post_blend_w = 0
        # next node
        if next_node is not None:
            next_node_pre_blend_w = self._stage_model.compute_width_for(next_node._track_model.pre_blend)
        else:
            next_node_pre_blend_w = 0

        # node blend
        node_pre_blend_start_x = start_x-node_pre_blend_w
        # last node post blend
        last_node_post_blend_end_x = start_x+last_node_post_blend_w
        # next node post blend
        next_node_pre_blend_start_x = end_x-next_node_pre_blend_w
        # node blend
        node_post_blend_end_x = end_x+node_post_blend_w

        path = _qt_core.QtPainterPath()

        text_h = h/2

        condition = [is_start, is_end]

        if condition == [True, True]:
            name_rect = QtCore.QRect(
                start_x, y, end_x-start_x, text_h
            )
            frame_rect = QtCore.QRect(
                start_x, y+text_h, end_x-start_x, text_h
            )
            points = [
                (start_x, y),
                (end_x, y),
                (end_x, h),
                (start_x, h),
            ]
        elif condition == [True, False]:
            name_rect = QtCore.QRect(
                start_x, y, node_post_blend_end_x-start_x, text_h
            )
            frame_rect = QtCore.QRect(
                start_x, y+text_h, next_node_pre_blend_start_x-start_x, text_h
            )
            points = [
                (start_x, y),
                (node_post_blend_end_x, y),
                (next_node_pre_blend_start_x, h),
                (start_x, h),
            ]
        elif condition == [False, True]:
            name_rect = QtCore.QRect(
                last_node_post_blend_end_x, y, end_x-last_node_post_blend_end_x, text_h
            )
            frame_rect = QtCore.QRect(
                node_pre_blend_start_x, y+text_h, end_x-node_pre_blend_start_x, text_h
            )
            points = [
                (last_node_post_blend_end_x, y),
                (end_x, y),
                (end_x, h),
                (node_pre_blend_start_x, h),
            ]
        else:
            name_rect = QtCore.QRect(
                last_node_post_blend_end_x, y, node_post_blend_end_x-last_node_post_blend_end_x, text_h
            )
            frame_rect = QtCore.QRect(
                node_pre_blend_start_x, y+text_h, next_node_pre_blend_start_x-node_pre_blend_start_x, text_h
            )
            points = [
                # top left
                (last_node_post_blend_end_x, y),
                # top right
                (node_post_blend_end_x, y),
                # bottom right
                (next_node_pre_blend_start_x, h),
                # bottom left
                (node_pre_blend_start_x, h),
            ]

        points += points[:1]

        path._add_points_(points)
        painter._set_background_color_(rgb)
        painter._set_border_color_(rgb)
        painter._set_antialiasing_(True)
        painter.drawPath(path)
        painter._set_antialiasing_(False)

        painter._set_text_color_(
            _gui_core.GuiRgba.LightBlack
        )
        # name and frame
        painter._set_font_(_qt_core.QtFont.generate(size=8))

        name_text_0 = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideMiddle,
            name_rect.width()-4,
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            name_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, name_text_0
        )

        time_text_0 = painter.fontMetrics().elidedText(
            str(time_text),
            QtCore.Qt.ElideMiddle,
            frame_rect.width()-4,
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            frame_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, time_text_0
        )
        # node blend rect
        bld_s = 12
        # node pre blend
        if node is not None and is_start is False:
            node._pre_blend_rect.setRect(
                node_pre_blend_start_x, h-bld_s-2, bld_s, bld_s
            )
            painter._set_background_color_(rgb)
            painter.drawRect(node._pre_blend_rect)
            painter.drawText(
                node._pre_blend_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, str(node_pre_blend)
            )
        # last node post blend
        if node is not None and last_node is not None:
            last_rgb = last_node._track_model.rgb
            last_node._post_blend_rect.setRect(
                last_node_post_blend_end_x-bld_s, y, bld_s, bld_s
            )
            painter._set_background_color_(last_rgb)
            painter.drawRect(last_node._post_blend_rect)
            painter.drawText(
                last_node._post_blend_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, str(last_node_post_blend)
            )

    def _set_graph_(self, widget):
        self._graph = widget

    def _restore_stage_(self):
        self._stage_model.restore()
        self._refresh_widget_all_()

    def _delete_node_(self, track_model):
        self._stage_model.delete_one(track_model)
