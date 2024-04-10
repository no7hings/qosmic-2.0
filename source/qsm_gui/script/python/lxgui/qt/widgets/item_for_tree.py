# coding=utf-8
import six

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import drag as gui_qt_wgt_drag


class QtTreeWidgetItem(
    QtWidgets.QTreeWidgetItem,
    gui_qt_abstracts.AbsQtItemDagLoading,
    #
    gui_qt_abstracts.AbsQtTypeDef,
    gui_qt_abstracts.AbsQtPathBaseDef,
    gui_qt_abstracts.AbsQtNameBaseDef,
    #
    gui_qt_abstracts.AbsQtIconBaseDef,
    gui_qt_abstracts.AbsQtShowBaseForItemDef,
    gui_qt_abstracts.AbsQtMenuBaseDef,
    #
    gui_qt_abstracts.AbsQtItemFilterDef,
    #
    gui_qt_abstracts.AbsQtStateDef,
    #
    gui_qt_abstracts.AbsQtDagDef,
    gui_qt_abstracts.AbsQtVisibleDef,
    #
    gui_qt_abstracts.AbsQtItemVisibleConnectionDef,
    #
    gui_qt_abstracts.AbsQtActionForDragDef,
):
    def update(self):
        pass

    def _refresh_widget_all_(self):
        pass

    def _refresh_widget_draw_(self):
        self._get_view_().update()

    ValidationStatus = gui_core.GuiValidationStatus

    def __init__(self, *args, **kwargs):
        super(QtTreeWidgetItem, self).__init__(*args, **kwargs)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled
        )
        #
        self._set_item_dag_loading_def_init_(self)
        self._init_show_base_for_item_def_(self)
        #
        self._check_action_is_enable = True
        self._emit_send_enable = False
        #
        self._init_type_base_def_(self)
        self._init_path_base_def_(self)
        self._init_name_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_menu_base_def_(self)
        #
        self._init_item_filter_extra_def_(self)
        #
        self._set_state_def_init_()
        #
        self._set_dag_def_init_()
        self._init_visible_base_def_(self)
        #
        self._set_item_visible_connection_def_init_()

        self._init_action_for_drag_def_(self)

        self._signals = gui_qt_core.QtItemSignals()

        self._status = self.ValidationStatus.Normal

        self._signals.drag_move.connect(
            self._do_drag_move_
        )

    def _do_drag_move_(self, data):
        if self._drag_is_enable is True:
            self._drag = gui_qt_wgt_drag.QtDragForTreeItem(self.treeWidget())
            self._drag.set_item(*data)
            self._drag.setMimeData(self._generate_drag_mime_data_())
            self._drag._do_drag_copy_(self._drag_point_offset)

    def setCheckState(self, column, state):
        self.setData(column, QtCore.Qt.CheckStateRole, state, emit_send_enable=False)

    def checkState(self, column):
        if self._check_action_is_enable is True:
            return self.data(column, QtCore.Qt.CheckStateRole)
        return QtCore.Qt.Unchecked

    def setData(self, column, role, value, **kwargs):
        emit_send_enable = False
        tree_widget = self.treeWidget()
        #
        check_state_pre = self.checkState(column)
        if role == QtCore.Qt.CheckStateRole:
            if self._check_action_is_enable is False:
                value = QtCore.Qt.Unchecked
            #
            emit_send_enable = kwargs.get('emit_send_enable', True)
        #
        super(QtTreeWidgetItem, self).setData(column, role, value)
        #
        if emit_send_enable is True:
            self._set_check_state_extra_(column)
            #
            check_state_cur = self.checkState(column)
            checked = [False, True][check_state_cur == QtCore.Qt.Checked]
            # send emit when value changed
            if check_state_pre != check_state_cur:
                tree_widget._send_check_changed_emit_(self, column)
            #
            tree_widget._send_check_toggled_emit_(self, column, checked)
            # update draw
            tree_widget.update()

    def _set_child_add_(self):
        item = self.__class__()
        self.addChild(item)
        item._connect_item_show_()
        return item

    def _get_item_is_hidden_(self):
        return self.isHidden()

    def _set_icon_(self, icon, column=0):
        self._icon = icon
        self.setIcon(column, self._icon)

    def _set_icon_file_path_(self, file_path, column=0):
        self._icon_file_path = file_path
        self._icon = QtGui.QIcon()
        self._icon.addPixmap(
            QtGui.QPixmap(self._icon_file_path),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        self.setIcon(column, self._icon)

    def _set_icon_color_rgb_(self, rgb, column=0):
        self.setIcon(
            column,
            gui_qt_core.GuiQtIcon.generate_by_rgb(rgb)
        )

    def _set_icon_name_text_(self, text, column=0):
        self._icon_text = text
        icon = QtGui.QIcon()
        pixmap = gui_qt_core.GuiQtPixmap.get_by_name(
            self._icon_text,
            size=(14, 14)
        )
        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        self.setIcon(column, icon)

    def _set_icon_state_update_(self, column=0):
        if column == 0:
            icon = QtGui.QIcon()
            pixmap = None
            if self._icon_file_path is not None:
                pixmap = QtGui.QPixmap(self._icon_file_path)
            elif self._icon_text is not None:
                pixmap = gui_qt_core.GuiQtPixmap.get_by_name(
                    self._icon_text,
                    size=(14, 14)
                )
            #
            if pixmap:
                if self._icon_state in [
                    gui_core.GuiState.ENABLE,
                    gui_core.GuiState.DISABLE,
                    gui_core.GuiState.WARNING,
                    gui_core.GuiState.ERROR,
                    gui_core.GuiState.LOCKED,
                    gui_core.GuiState.LOST
                ]:
                    if self._icon_state == gui_core.GuiState.ENABLE:
                        background_color = gui_qt_core.QtColors.TextEnable
                    elif self._icon_state == gui_core.GuiState.DISABLE:
                        background_color = gui_qt_core.QtColors.TextDisable
                    elif self._icon_state == gui_core.GuiState.WARNING:
                        background_color = gui_qt_core.QtColors.TextWarning
                    elif self._icon_state == gui_core.GuiState.ERROR:
                        background_color = gui_qt_core.QtColors.TextError
                    elif self._icon_state == gui_core.GuiState.LOCKED:
                        background_color = gui_qt_core.QtColors.TextLock
                    elif self._icon_state == gui_core.GuiState.LOST:
                        background_color = gui_qt_core.QtColors.TextTemporary
                    else:
                        raise TypeError()
                    #
                    painter = gui_qt_core.QtPainter(pixmap)
                    rect = pixmap.rect()
                    x, y = rect.x(), rect.y()
                    w, h = rect.width(), rect.height()
                    #
                    border_color = gui_qt_core.QtBorderColors.Icon
                    #
                    s_w, s_h = w*.5, h*.5
                    state_rect = QtCore.QRect(
                        x, y+h-s_h, s_w, s_h
                    )
                    if self._icon_state == gui_core.GuiState.LOCKED:
                        painter._draw_icon_file_by_rect_(
                            state_rect,
                            file_path=gui_core.GuiIcon.get(
                                'state-locked'
                            )
                        )
                        painter.end()
                    elif self._icon_state == gui_core.GuiState.LOST:
                        painter._draw_icon_file_by_rect_(
                            state_rect,
                            file_path=gui_core.GuiIcon.get(
                                'state-lost'
                            )
                        )
                        painter.end()
                    else:
                        painter._draw_frame_by_rect_(
                            state_rect,
                            border_color=border_color,
                            background_color=background_color,
                            border_radius=w/2
                        )
                        painter.end()
                #
                icon.addPixmap(
                    pixmap,
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.On
                )
                self.setIcon(column, icon)

    # status
    def _set_status_(self, status, column=0):
        if status != self._status:
            self._status = status
            #
            self._set_name_status_(status, column)
            self._update_wgt_icon_(status, column)

    def _set_menu_content_(self, content):
        super(QtTreeWidgetItem, self)._set_menu_content_(content)
        self._update_wgt_icon_(status=self._status)

    def _set_menu_data_(self, raw):
        super(QtTreeWidgetItem, self)._set_menu_data_(raw)
        self._update_wgt_icon_(status=self._status)

    def _set_name_status_(self, status, column=0):
        font = gui_qt_core.GuiQtFont.generate(size=8)
        if status == self.ValidationStatus.Normal:
            color = gui_qt_core.QtColors.Text
        elif status in {self.ValidationStatus.Correct, self.ValidationStatus.New}:
            color = gui_qt_core.QtColors.TextCorrect
        elif status == self.ValidationStatus.Warning:
            color = gui_qt_core.QtColors.TextWarning
        elif status in {self.ValidationStatus.Error, self.ValidationStatus.Unreadable}:
            color = gui_qt_core.QtColors.TextError
        elif status == self.ValidationStatus.Active:
            color = gui_qt_core.QtColors.TextActive
        elif status in {self.ValidationStatus.Disable, self.ValidationStatus.Lost}:
            color = gui_qt_core.QtColors.TextDisable
            font.setItalic(True)
        elif status in {self.ValidationStatus.Locked, self.ValidationStatus.Unwritable}:
            color = gui_qt_core.QtColors.TextLock
            font.setItalic(True)
        else:
            raise TypeError()

        self.setFont(column, font)
        if column == 0:
            c = self.treeWidget().columnCount()
            for i in range(c):
                self.setForeground(i, QtGui.QBrush(color))
        else:
            self.setForeground(column, QtGui.QBrush(color))

    def _update_wgt_icon_(self, status, column=0):
        if column == 0:
            pixmap = None
            if self._icon:
                pixmap = self._icon.pixmap(20, 20)
            elif self._icon_file_path is not None:
                pixmap = QtGui.QPixmap(self._icon_file_path)
            elif self._icon_text is not None:
                pixmap = gui_qt_core.GuiQtPixmap.get_by_name(
                    self._icon_text,
                    size=(14, 14)
                )
            #
            if pixmap:
                painter = gui_qt_core.QtPainter(pixmap)
                rect = pixmap.rect()
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                #
                if status is not None:
                    draw_status = True
                    if status == self.ValidationStatus.Normal:
                        draw_status = False
                        background_color = gui_qt_core.QtColors.Text
                    elif status in {self.ValidationStatus.Correct, self.ValidationStatus.New}:
                        background_color = gui_qt_core.QtColors.TextCorrect
                    elif status == self.ValidationStatus.Warning:
                        background_color = gui_qt_core.QtColors.TextWarning
                    elif status in {self.ValidationStatus.Error, self.ValidationStatus.Unreadable}:
                        background_color = gui_qt_core.QtColors.TextError
                    elif status == self.ValidationStatus.Active:
                        background_color = gui_qt_core.QtColors.TextActive
                    elif status in {self.ValidationStatus.Disable, self.ValidationStatus.Lost}:
                        background_color = gui_qt_core.QtColors.TextDisable
                    elif status in {self.ValidationStatus.Locked, self.ValidationStatus.Unwritable}:
                        background_color = gui_qt_core.QtColors.TextLock
                    else:
                        raise TypeError()
                    #
                    if draw_status is True:
                        border_color = gui_qt_core.QtBorderColors.Icon
                        #
                        s_w, s_h = w*.5, h*.5
                        status_rect = QtCore.QRect(
                            x+w-s_w, y+h-s_h, s_w, s_h
                        )
                        # draw status
                        if status in {self.ValidationStatus.Disable, self.ValidationStatus.Lost}:
                            painter._draw_icon_file_by_rect_(
                                rect=status_rect,
                                file_path=gui_core.GuiIcon.get(
                                    'state-disable'
                                )
                            )
                        elif status in {self.ValidationStatus.Error, self.ValidationStatus.Unreadable}:
                            painter._draw_icon_file_by_rect_(
                                rect=status_rect,
                                file_path=gui_core.GuiIcon.get(
                                    'state-lost'
                                )
                            )
                        elif status in {self.ValidationStatus.Locked, self.ValidationStatus.Unwritable}:
                            painter._draw_icon_file_by_rect_(
                                rect=status_rect,
                                file_path=gui_core.GuiIcon.get(
                                    'state-locked'
                                )
                            )
                        else:
                            painter._draw_frame_by_rect_(
                                rect=status_rect,
                                border_color=border_color,
                                background_color=background_color,
                                border_width=2,
                                border_radius=w/2
                            )
                #
                if self._menu_content is not None or self._menu_data:
                    m_w, m_h = w/2, h/4
                    menu_mark_rect = QtCore.QRect(
                        x+w-m_w, y, m_w, m_h
                    )
                    painter._draw_icon_file_by_rect_(
                        rect=menu_mark_rect,
                        file_path=gui_core.GuiIcon.get('menu-mark-h'),
                    )
                #
                painter.end()
                #
                icon = QtGui.QIcon()
                icon.addPixmap(
                    pixmap,
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.On
                )
                self.setIcon(column, icon)

    # noinspection PyUnusedLocal
    def _get_status_(self, column=0):
        return self._status

    def _set_update_(self):
        tree_widget = self.treeWidget()
        tree_widget.update()

    def _set_user_data_(self, key, value, column=0):
        raw = self.data(column, QtCore.Qt.UserRole) or {}
        raw[key] = value
        self.setData(
            column, QtCore.Qt.UserRole, raw
        )

    def _get_user_data_(self, key, column=0):
        pass

    def _set_check_enable_(self, boolean, column=0):
        self._check_action_is_enable = boolean
        self.setData(column, QtCore.Qt.CheckStateRole, self.checkState(column))

    def _get_check_action_is_enable_(self):
        return self._check_action_is_enable

    def _set_emit_send_enable_(self, boolean):
        self._emit_send_enable = boolean

    def _get_emit_send_enable_(self):
        return self._emit_send_enable

    def _set_check_state_(self, boolean, column=0):
        self.setCheckState(
            column, [gui_qt_core.QtCore.Qt.Unchecked, gui_qt_core.QtCore.Qt.Checked][boolean]
        )

    def _set_check_state_extra_(self, column=0):
        if self._check_action_is_enable is True:
            check_state = self.checkState(column)
            descendants = self._get_descendants_()
            [i.setData(column, QtCore.Qt.CheckStateRole, check_state, emit_send_enable=False) for i in descendants]
            ancestors = self._get_ancestors_()
            [
                i.setData(
                    column, QtCore.Qt.CheckStateRole, i._get_check_state_by_descendants(column), emit_send_enable=False
                ) for i in ancestors
            ]

    def _set_checked_(self, boolean, column=0):
        self._set_check_state_(boolean, column)

    def _get_check_state_by_descendants(self, column):
        for i in self._get_descendants_():
            if i.checkState(column) == QtCore.Qt.Checked:
                return QtCore.Qt.Checked
        return QtCore.Qt.Unchecked

    def _get_children_(self):
        lis = []
        count = self.childCount()
        for i_index in range(count):
            i_item = self.child(i_index)
            lis.append(i_item)
        return lis

    def _get_descendants_(self):
        def _rcs_fnc(item_):
            _child_count = item_.childCount()
            for _child_index in range(_child_count):
                _child_item = item_.child(_child_index)
                lis.append(_child_item)
                _rcs_fnc(_child_item)

        lis = []
        _rcs_fnc(self)
        return lis

    def _get_ancestors_(self):
        def _rcs_fnc(item_):
            _parent_item = item_.parent()
            if _parent_item is not None:
                lis.append(_parent_item)
                _rcs_fnc(_parent_item)

        lis = []
        _rcs_fnc(self)
        return lis

    def _get_is_hidden_(self, ancestors=False):
        if ancestors is True:
            if self.isHidden():
                return True
            qt_tree_widget, qt_tree_widget_item = self.treeWidget(), self
            return gui_qt_core.GuiQtTreeWidget.get_item_is_ancestor_hidden(qt_tree_widget, qt_tree_widget_item)
        else:
            return self.isHidden()

    def _get_name_texts_(self):
        column_count = self.treeWidget().columnCount()
        return [self.text(i) for i in range(column_count)]

    def _get_name_text_(self, column=0):
        return self.text(column) or ''

    # show
    def _set_view_(self, widget):
        self._tree_widget = widget

    def _connect_item_show_(self):
        self._setup_item_show_(self.treeWidget())

    def _get_view_(self):
        return self.treeWidget()

    def _get_item_is_viewport_showable_(self):
        item = self
        view = self.treeWidget()
        parent = self.parent()
        if parent is None:
            return view._get_view_item_viewport_showable_(item)
        else:
            if parent.isExpanded():
                return view._get_view_item_viewport_showable_(item)
        return False

    def _set_item_widget_visible_(self, boolean):
        pass
        # self.setVisible(boolean)

    def _set_name_text_(self, text, column=0):
        if text is not None:
            if isinstance(text, (tuple, list)):
                if len(text) > 1:
                    _ = '; '.join(('{}.{}'.format(seq+1, i) for seq, i in enumerate(text)))
                elif len(text) == 1:
                    _ = text[0]
                else:
                    _ = ''
            else:
                _ = bsc_core.auto_encode(text)
            #
            self.setText(column, _)
            self.setFont(column, gui_qt_core.QtFonts.NameNormal)

    def _set_tool_tip_(self, raw, column=0):
        if raw is not None:
            if isinstance(raw, six.string_types):
                text = raw
            elif isinstance(raw, dict):
                text = six.u('\n').join([six.u('{}: {}').format(k, v) for k, v in raw.items()])
            elif isinstance(raw, (tuple, list)):
                text = six.u('\n').join(raw)
            else:
                raise TypeError()
            #
            self._set_tool_tip_text_(
                text,
                column,
            )

    def _set_tool_tip_text_(self, text, column=0):
        if hasattr(self, 'setToolTip'):
            text = bsc_core.auto_encode(text)
            #
            text = text.replace(' ', '&nbsp;')
            text = text.replace('<', '&lt;')
            text = text.replace('>', '&gt;')
            #
            css = (
                '<html>\n'
                '<body>\n'
                '<style>.no_wrap{white-space:nowrap;}</style>\n'
                '<style>.no_warp_and_center{white-space:nowrap;text-align: center;}</style>\n'
            )
            name_text_orig = self._get_name_text_orig_()
            if name_text_orig is not None:
                title_text = name_text_orig
            else:
                title_text = self._get_name_text_(column)
            #
            title_text = bsc_core.auto_encode(title_text)
            #
            title_text = title_text.replace('<', '&lt;').replace('>', '&gt;')
            css += '<h3><p class="no_warp_and_center">{}</p></h3>\n'.format(title_text)
            #
            css += '<p><hr></p>\n'
            if isinstance(text, six.string_types):
                texts = text.split('\n')
            elif isinstance(text, (tuple, list)):
                texts = text
            else:
                raise RuntimeError()
            #
            for i in texts:
                css += '<p class="no_wrap">{}</p>\n'.format(i)

            css += '</body>\n</html>'
            # noinspection PyCallingNonCallable
            self.setToolTip(column, css)

    def _get_item_widget_(self):
        pass

    def _get_state_color_(self):
        return self.foreground(0)

    def _set_hidden_(self, boolean, ancestors=False):
        self.setHidden(boolean)
        if ancestors is True:
            [i.set_visible_by_has_visible_children() for i in self.get_ancestors()]
        #
        self._set_item_visible_connection_refresh_()
        if hasattr(self, 'gui_proxy'):
            self.gui_proxy.set_visible_connection_refresh()

    def _set_expanded_(self, boolean, ancestors=False):
        self.setExpanded(boolean)
        self._set_item_show_start_auto_()
        #
        if ancestors is True:
            [i._set_expanded_(boolean) for i in self._get_ancestors_()]

    def _clear_(self):
        self.takeChildren()

    def _set_selected_(self, boolean):
        # self.treeWidget().setItemSelected(self, boolean)
        self.setSelected(boolean)

    def _set_current_(self):
        self.treeWidget().setCurrentItem(self)

    def __str__(self):
        return '{}(names="{}")'.format(
            self.__class__.__name__, ', '.join(self._get_name_texts_())
        )

    def __repr__(self):
        return self.__str__()
