# coding=utf-8
import lxbasic.model as bsc_model
# gui
from .... import core as _gui_core
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ... import abstracts as _qt_abstracts


class QtTrackGuide(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
):
    stage_changed = qt_signal()

    class BlendMode:
        Previous = 0
        Post = 1

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

        start_x = self._track_model_stage.compute_start_x()
        track_w = self._track_model_stage.compute_width()
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

    def _do_press_click_(self, event):
        p = event.pos()

        self._press_point = event.pos()
        self._current_blend_offset_timeframe = 0
        self._current_blend_flag = -1
        self._current_track_key = None
        self._current_blend_move_flag = False
        for i in self._track_model_stage.get_all_nodes():
            if i._pre_blend_flag is True:
                if i._pre_blend_rect.contains(p):
                    self._current_track_key = i._track_model.key
                    self._current_blend_flag = 0
                    break
            if i._post_blend_flag is True:
                if i._post_blend_rect.contains(p):
                    self._current_track_key = i._track_model.key
                    self._current_blend_flag = 1
                    break

    def _do_press_move_(self, event):
        if self._current_track_key is not None:
            self._current_blend_move_flag = True
            p_d = event.pos()-self._press_point
            offset = self._track_model_stage._time_coord_model.compute_unit_count_by(p_d.x())
            if offset != self._current_blend_offset_timeframe:
                node = self._track_model_stage.get_one_node(self._current_track_key)
                self._current_blend_offset_timeframe = offset
                if self._current_blend_flag == 0:
                    node._update_pre_blend_tmp_(offset)
                elif self._current_blend_flag == 1:
                    node._update_post_blend_tmp_(offset)

                self._refresh_widget_all_()

    def _do_press_release_(self, evnt):
        if self._current_blend_move_flag is True:
            self._graph._graph_node_update_blend_(self._current_track_key, self._current_blend_flag)

    def _update_stage_(self):
        self._track_model_stage.update()
        self.stage_changed.emit()

        self._refresh_widget_all_()

    def __init__(self, *args, **kwargs):
        super(QtTrackGuide, self).__init__(*args, **kwargs)
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

        self._track_model_stage = bsc_model.TrackModelStage()

        self._current_track_key = None
        self._current_blend_flag = 0
        self._current_blend_offset_timeframe = 0
        self._current_blend_move_flag = False

        self._press_point = QtCore.QPoint()

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
                    self._do_press_click_(event)
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
                    self._do_press_move_(event)
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    self._graph.eventFilter(self._graph, event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_press_release_(event)
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
        self._draw_nodes_(painter)
        # line
        painter._set_border_color_(_gui_core.GuiRgba.Gray)
        painter.drawLine(bottom_line)

        painter._set_border_color_(_gui_core.GuiRgba.DarkWhite)
        painter._set_font_(_qt_core.QtFont.generate(size=10))

        painter.drawText(
            self._track_start_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            str(self._track_model_stage.track_start)
        )
        painter.drawText(
            self._track_end_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            str(self._track_model_stage.track_end)
        )

    def _draw_nodes_(self, painter):
        h = self.height()

        tvl = self._track_model_stage.generate_travel()
        while tvl.is_valid():
            frame_range, track_model = tvl.current_data()

            is_start, is_end = tvl.is_start(), tvl.is_end()

            pre_key = tvl.pre_key()
            if pre_key:
                pre_node = self._track_model_stage.get_one_node(pre_key)
            else:
                pre_node = None

            next_key = tvl.next_key()
            if next_key:
                next_node = self._track_model_stage.get_one_node(next_key)
            else:
                next_node = None

            if track_model is not None:
                key = track_model.key

                node = self._track_model_stage.get_one_node(key)

                # is starting
                if pre_node is None:
                    pre_pre_key = tvl.pre_pre_key()
                    pre_pre_node = self._track_model_stage.get_one_node(pre_pre_key)
                    self._draw_node_(
                        painter, pre_pre_node, node, next_node,
                        frame_range, h, is_start, is_end
                    )

                # is ending
                elif next_node is None:
                    next_next_key = tvl.next_next_key()
                    next_next_node = self._track_model_stage.get_one_node(next_next_key)
                    self._draw_node_(
                        painter, pre_node, node, next_next_node,
                        frame_range, h, is_start, is_end
                    )
                # middle
                else:
                    self._draw_node_(
                        painter, pre_node, node, next_node,
                        frame_range, h, is_start, is_end
                    )
            else:
                self._draw_node_(
                    painter, pre_node, None, next_node,
                    frame_range, h, is_start, is_end
                )

            tvl.next()

    def _draw_node_(
        self, painter, pre_node, node, next_node,
        frame_range, h, is_start, is_end
    ):
        y = 0
        start, end = frame_range
        if start == end:
            time_text = str(start)
        else:
            time_text = '{}-{}'.format(start, end)

        count = end-start+1

        start_x = self._track_model_stage.compute_start_x_at(start)
        count_w = self._track_model_stage.compute_width_for(count)
        end_x = start_x+count_w

        # check node is valid
        if node is not None:
            track_model = node._track_model

            key = track_model.key
            if key == self._current_track_key:
                hover_flag = True
            else:
                hover_flag = False

            node_pre_blend = node._get_pre_blend_(self._current_blend_move_flag)
            node_pre_blend_w = self._track_model_stage.compute_width_for(node_pre_blend)

            node_post_blend = node._get_post_blend_(self._current_blend_move_flag)
            node_post_blend_w = self._track_model_stage.compute_width_for(node_post_blend)

            frame_range_index = track_model.get_frame_range_index(frame_range)
            if frame_range_index > 0:
                text = '{}({})'.format(key, frame_range_index)
            else:
                text = key

            rgb = track_model.rgb

        else:
            node_pre_blend = pre_node._get_pre_blend_(self._current_blend_move_flag)
            node_pre_blend_w = self._track_model_stage.compute_width_for(node_pre_blend)

            node_post_blend = pre_node._get_post_blend_(self._current_blend_move_flag)
            node_post_blend_w = self._track_model_stage.compute_width_for(node_post_blend)

            text = '{}(missing)'.format(pre_node._track_model.key)

            rgb = (255, 0, 0)

            hover_flag = False

        # pre node
        if pre_node is not None:
            pre_node_post_blend = pre_node._get_post_blend_(self._current_blend_move_flag)
            pre_node_post_blend_w = self._track_model_stage.compute_width_for(pre_node_post_blend)
        else:
            pre_node_post_blend = 0
            pre_node_post_blend_w = 0

        # next node
        if next_node is not None:
            next_node_pre_blend = next_node._get_pre_blend_(self._current_blend_move_flag)
            next_node_pre_blend_w = self._track_model_stage.compute_width_for(next_node_pre_blend)
            next_rgb = next_node._track_model.rgb
        else:
            next_node_pre_blend_w = 0
            next_rgb = rgb

        # node blend
        node_pre_blend_start_x = start_x-node_pre_blend_w
        # last node post blend
        pre_node_post_blend_end_x = start_x+pre_node_post_blend_w
        # next node post blend
        next_node_pre_blend_start_x = end_x-next_node_pre_blend_w
        # node blend
        node_post_blend_end_x = end_x+node_post_blend_w

        text_h = h/2
        bld_s = 12
        bld_s_0 = bld_s/2

        condition = [is_start, is_end]

        # one track
        if condition == [True, True]:
            name_rect = QtCore.QRect(
                start_x, y, end_x-start_x, text_h
            )
            frame_rect = QtCore.QRect(
                start_x, y+text_h, end_x-start_x, text_h
            )

            basic_rect = QtCore.QRect(
                start_x-1, y, end_x-start_x+2, h
            )

            curve_coords = []
            if node is not None:
                node._pre_blend_flag = False
                node._post_blend_flag = False

        # start track, more than one
        elif condition == [True, False]:
            name_rect = QtCore.QRect(
                start_x, y, node_post_blend_end_x-start_x, text_h
            )
            frame_rect = QtCore.QRect(
                start_x, y+text_h, next_node_pre_blend_start_x-start_x, text_h
            )

            basic_rect = QtCore.QRect(
                start_x-1, y, node_post_blend_end_x-start_x+2, h
            )

            curve_coords = []
            if node is not None:
                node._pre_blend_flag = False
                node._post_blend_flag = True

        # end track
        elif condition == [False, True]:
            name_rect = QtCore.QRect(
                pre_node_post_blend_end_x, y, end_x-pre_node_post_blend_end_x, text_h
            )
            frame_rect = QtCore.QRect(
                node_pre_blend_start_x, y+text_h, end_x-node_pre_blend_start_x, text_h
            )

            basic_rect = QtCore.QRect(
                pre_node_post_blend_end_x-1, y, end_x-pre_node_post_blend_end_x+2, h
            )

            curve_coords = [
                (node_pre_blend_start_x, h-bld_s_0),
                (pre_node_post_blend_end_x, y+bld_s_0)
            ]
            if node is not None:
                node._pre_blend_flag = True
                node._post_blend_flag = False

        # middle track
        else:
            name_rect = QtCore.QRect(
                pre_node_post_blend_end_x, y, node_post_blend_end_x-pre_node_post_blend_end_x, text_h
            )
            frame_rect = QtCore.QRect(
                node_pre_blend_start_x, y+text_h, next_node_pre_blend_start_x-node_pre_blend_start_x, text_h
            )

            basic_rect = QtCore.QRect(
                pre_node_post_blend_end_x-1, y, node_post_blend_end_x-pre_node_post_blend_end_x+2, h
            )

            curve_coords = [
                (node_pre_blend_start_x, h-bld_s_0),
                (pre_node_post_blend_end_x, y+bld_s_0)
            ]

            if node is not None:
                node._pre_blend_flag = True
                node._post_blend_flag = True

        # basic path
        basic_color = QtGui.QLinearGradient(
            basic_rect.topLeft(), basic_rect.topRight()
        )
        basic_color.setColorAt(0, QtGui.QColor(*rgb))
        basic_color.setColorAt(0.875, QtGui.QColor(*rgb))
        basic_color.setColorAt(1.0, QtGui.QColor(*next_rgb))
        painter.setBrush(basic_color)
        painter.setPen(QtGui.QColor(0, 0, 0, 0))
        painter.drawRect(basic_rect)

        # draw hover
        # if hover_flag is True:
        #     hover_color = QtGui.QLinearGradient(
        #         basic_rect.topLeft(), basic_rect.topRight()
        #     )
        #     if self._current_blend_flag == 0:
        #         hover_color.setColorAt(0, QtGui.QColor(0, 0, 0, 0))
        #         hover_color.setColorAt(.05, _qt_core.QtRgba.LightAzureBlue)
        #         hover_color.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
        #     else:
        #         hover_color.setColorAt(0, QtGui.QColor(0, 0, 0, 0))
        #         hover_color.setColorAt(.95, _qt_core.QtRgba.LightAzureBlue)
        #         hover_color.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
        #
        #     painter.setBrush(hover_color)
        #     painter.setPen(QtGui.QColor(0, 0, 0, 0))
        #     painter.drawRect(basic_rect)

        painter._set_antialiasing_(True)
        if node is not None:
            if curve_coords:
                self._draw_blend_curve_(painter, curve_coords)
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

        # node blend rect, second node or latest node
        # node pre blend
        if node is not None and is_start is False:
            node._pre_blend_rect.setRect(
                node_pre_blend_start_x-bld_s_0, h-bld_s-2, bld_s, bld_s
            )
            painter.setBrush(QtGui.QColor(*rgb))
            if hover_flag is True:
                if self._current_blend_flag == 0:
                    painter.setBrush(_qt_core.QtRgba.LightAzureBlue)

            painter.drawRect(node._pre_blend_rect)
            painter.drawText(
                node._pre_blend_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, str(node_pre_blend)
            )

        # last node post blend
        if node is not None and pre_node is not None:
            pre_track_model = pre_node._track_model
            pre_key = pre_track_model.key
            pre_rgb = pre_track_model.rgb
            pre_node._post_blend_rect.setRect(
                pre_node_post_blend_end_x-bld_s_0, y, bld_s, bld_s
            )
            painter.setBrush(QtGui.QColor(*pre_rgb))
            if pre_key == self._current_track_key:
                if self._current_blend_flag == 1:
                    painter.setBrush(_qt_core.QtRgba.LightAzureBlue)

            painter.drawRect(pre_node._post_blend_rect)
            painter.drawText(
                pre_node._post_blend_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, str(pre_node_post_blend)
            )

    def _draw_blend_curve_(self, painter, coords):
        points = [QtCore.QPointF(*x) for x in coords]
        basic_path = QtGui.QPainterPath()

        point_first = points[0]
        basic_path.moveTo(point_first)

        painter.setBrush(QtGui.QColor(0, 0, 0, 0))

        handle_width = (coords[1][0]-coords[0][0])/2

        for i in range(len(points)-1):
            i_point_pre = points[i]
            i_point = points[i+1]

            i_out_tangent_point = QtCore.QPointF(i_point_pre.x()+handle_width, i_point_pre.y())
            i_in_tangent_point = QtCore.QPointF(i_point.x()-handle_width, i_point.y())

            basic_path.cubicTo(i_out_tangent_point, i_in_tangent_point, i_point)

        painter.setPen(QtGui.QPen(QtGui.QColor(47, 47, 47, 255), 2))
        painter.drawPath(basic_path)

    def _set_graph_(self, widget):
        self._graph = widget

    def _restore_stage_(self):
        self._track_model_stage.restore()
        self._refresh_widget_all_()

    def _delete_node_(self, track_model):
        self._track_model_stage.delete_one(track_model)
