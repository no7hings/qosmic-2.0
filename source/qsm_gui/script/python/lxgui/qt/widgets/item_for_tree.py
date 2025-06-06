# coding=utf-8
import six

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts
# qt widgets
from . import drag as _qt_wgt_drag


class QtTreeWidgetItem(
    QtWidgets.QTreeWidgetItem,
    _qt_abstracts.AbsQtItemDagLoading,
    #
    _qt_abstracts.AbsQtTypeDef,
    _qt_abstracts.AbsQtPathBaseDef,
    _qt_abstracts.AbsQtNameBaseDef,
    #
    _qt_abstracts.AbsQtIconBaseDef,
    _qt_abstracts.AbsQtShowBaseForVirtualItemDef,
    _qt_abstracts.AbsQtMenuBaseDef,
    #
    _qt_abstracts.AbsQtItemFilterDef,
    #
    _qt_abstracts.AbsQtStateDef,
    #
    _qt_abstracts.AbsQtDagDef,
    _qt_abstracts.AbsQtVisibleDef,
    #
    _qt_abstracts.AbsQtItemVisibleConnectionDef,
    #
    _qt_abstracts.AbsQtActionForDragDef,
):
    def update(self):
        pass

    def _refresh_widget_all_(self):
        pass

    def _refresh_widget_draw_(self):
        self._get_view_().update()

    ValidationStatus = _gui_core.GuiValidationStatus
    ProcessStatus = _gui_core.GuiProcessStatus

    Rgba = _gui_core.GuiRgba

    def __init__(self, *args, **kwargs):
        super(QtTreeWidgetItem, self).__init__(*args, **kwargs)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled
        )
        #
        self._set_item_dag_loading_def_init_(self)
        self._init_show_base_for_virtual_item_def_(self)
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

        self._signals = _qt_core.QtItemSignals()

        self._status = self.ValidationStatus.Normal

        self._process_status = self.ProcessStatus.Unknown

        self._signals.drag_move.connect(
            self._do_drag_move_
        )

    def _do_drag_move_(self, data):
        if self._drag_is_enable is True:
            self._drag = _qt_wgt_drag.QtDragForTreeItem(self.treeWidget())
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
                tree_widget._send_check_changed_emit(self, column)
            #
            tree_widget._send_check_toggled_emit(self, column, checked)
            # update draw
            tree_widget.update()

    def _set_child_add_(self):
        item = self.__class__()
        self.addChild(item)
        item._initialize_item_show_()
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
            _qt_core.QtIcon.generate_by_rgb(rgb)
        )

    def _set_name_icon_text_(self, text, column=0):
        self._name_icon_text = text
        icon = QtGui.QIcon()
        pixmap = _qt_core.QtPixmap.get_by_name(
            self._name_icon_text,
            size=(14, 14)
        )
        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        self.setIcon(column, icon)

    def _set_sub_icon_by_text_(self, text, column=0):
        self._sub_icon_text = text

    def _set_icon_state_update_(self, column=0):
        if column == 0:
            icon = QtGui.QIcon()
            pixmap = None
            if self._icon_file_path is not None:
                pixmap = QtGui.QPixmap(self._icon_file_path)
            elif self._name_icon_text is not None:
                pixmap = _qt_core.QtPixmap.get_by_name(
                    self._name_icon_text,
                    size=(14, 14)
                )
            #
            if pixmap:
                if self._icon_state in [
                    _gui_core.GuiState.ENABLE,
                    _gui_core.GuiState.DISABLE,
                    _gui_core.GuiState.WARNING,
                    _gui_core.GuiState.ERROR,
                    _gui_core.GuiState.LOCKED,
                    _gui_core.GuiState.LOST
                ]:
                    if self._icon_state == _gui_core.GuiState.ENABLE:
                        background_color = _qt_core.QtRgba.TxtEnable
                    elif self._icon_state == _gui_core.GuiState.DISABLE:
                        background_color = _qt_core.QtRgba.TxtDisable
                    elif self._icon_state == _gui_core.GuiState.WARNING:
                        background_color = _qt_core.QtRgba.TxtWarning
                    elif self._icon_state == _gui_core.GuiState.ERROR:
                        background_color = _qt_core.QtRgba.TxtError
                    elif self._icon_state == _gui_core.GuiState.LOCKED:
                        background_color = _qt_core.QtRgba.TxtLock
                    elif self._icon_state == _gui_core.GuiState.LOST:
                        background_color = _qt_core.QtRgba.TxtTemporary
                    else:
                        raise TypeError()
                    #
                    painter = _qt_core.QtPainter(pixmap)
                    rect = pixmap.rect()
                    x, y = rect.x(), rect.y()
                    w, h = rect.width(), rect.height()
                    #
                    border_color = _qt_core.QtRgba.BdrIcon
                    #
                    s_w, s_h = w*.5, h*.5
                    state_rect = qt_rect(
                        x, y+h-s_h, s_w, s_h
                    )
                    if self._icon_state == _gui_core.GuiState.LOCKED:
                        painter._draw_icon_file_by_rect_(
                            state_rect,
                            file_path=_gui_core.GuiIcon.get(
                                'state-locked'
                            )
                        )
                        painter.end()
                    elif self._icon_state == _gui_core.GuiState.LOST:
                        painter._draw_icon_file_by_rect_(
                            state_rect,
                            file_path=_gui_core.GuiIcon.get(
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
        font = _qt_core.QtFont.generate(size=8)
        if status == self.ValidationStatus.Normal:
            color = _qt_core.QtRgba.Text
        elif status in {self.ValidationStatus.Correct, self.ValidationStatus.New}:
            color = _qt_core.QtRgba.TxtCorrect
        elif status == self.ValidationStatus.Warning:
            color = _qt_core.QtRgba.TxtWarning
        elif status in {self.ValidationStatus.Error, self.ValidationStatus.Unreadable}:
            color = _qt_core.QtRgba.TxtError
        elif status == self.ValidationStatus.Active:
            color = _qt_core.QtRgba.TxtActive
        elif status in {self.ValidationStatus.Disable, self.ValidationStatus.Lost}:
            color = _qt_core.QtRgba.TxtDisable
            font.setItalic(True)
        elif status in {self.ValidationStatus.Locked, self.ValidationStatus.Unwritable}:
            color = _qt_core.QtRgba.TxtLock
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

    def _set_process_status_(self, status, column=0):
        self._process_status = status
        font = _qt_core.QtFont.generate(size=8)
        if status in {self.ProcessStatus.Unknown}:
            color = _qt_core.QtRgba.Text
        elif status in {self.ProcessStatus.Waiting}:
            color = QtGui.QColor(*self.Rgba.LightOrange)
        elif status in {self.ProcessStatus.Started, self.ProcessStatus.Running}:
            color = QtGui.QColor(*self.Rgba.LightAzureBlue)
        elif status in {self.ProcessStatus.Suspended}:
            color = QtGui.QColor(*self.Rgba.LightLemonYellow)
        elif status in {self.ProcessStatus.Failed, self.ProcessStatus.Error, self.ProcessStatus.Killed}:
            color = QtGui.QColor(*self.Rgba.LightTorchRed)
        elif status in {self.ProcessStatus.Completed, self.ProcessStatus.Finished}:
            color = QtGui.QColor(*self.Rgba.LightNeonGreen)
        elif status in {self.ProcessStatus.Stopped}:
            color = QtGui.QColor(*self.Rgba.DarkGray)
        else:
            raise TypeError()

        self.setFont(column, font)
        if column == 0:
            c = self.treeWidget().columnCount()
            for i in range(c):
                self.setForeground(i, QtGui.QBrush(color))
        else:
            self.setForeground(column, QtGui.QBrush(color))

    def _get_process_status_(self):
        return self._process_status

    def _get_process_status_from_children_(self):
        status = []
        children = self._get_children_()
        for i in children:
            i_status = i._get_process_status_()
            status.append(i_status)
            if i_status == self.ProcessStatus.Failed:
                return self.ProcessStatus.Failed
        c = len(children)
        if status == [self.ProcessStatus.Completed]*c:
            return self.ProcessStatus.Completed
        return self.ProcessStatus.Unknown

    def _update_wgt_icon_(self, status, column=0):
        if column == 0:
            pixmap = None
            if self._icon:
                pixmap = self._icon.pixmap(20, 20)
            elif self._icon_file_path is not None:
                pixmap = QtGui.QPixmap(self._icon_file_path)
            elif self._name_icon_text is not None:
                pixmap = _qt_core.QtPixmap.get_by_name(
                    self._name_icon_text,
                    size=(14, 14)
                )
            #
            if pixmap:
                painter = _qt_core.QtPainter(pixmap)
                rect = pixmap.rect()
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                #
                if status is not None:
                    draw_status = True
                    if status == self.ValidationStatus.Normal:
                        draw_status = False
                        background_color = _qt_core.QtRgba.Text
                    elif status in {self.ValidationStatus.Correct, self.ValidationStatus.New}:
                        background_color = _qt_core.QtRgba.TxtCorrect
                    elif status == self.ValidationStatus.Warning:
                        background_color = _qt_core.QtRgba.TxtWarning
                    elif status in {self.ValidationStatus.Error, self.ValidationStatus.Unreadable}:
                        background_color = _qt_core.QtRgba.TxtError
                    elif status == self.ValidationStatus.Active:
                        background_color = _qt_core.QtRgba.TxtActive
                    elif status in {self.ValidationStatus.Disable, self.ValidationStatus.Lost}:
                        background_color = _qt_core.QtRgba.TxtDisable
                    elif status in {self.ValidationStatus.Locked, self.ValidationStatus.Unwritable}:
                        background_color = _qt_core.QtRgba.TxtLock
                    else:
                        raise TypeError()
                    #
                    if draw_status is True:
                        border_color = _qt_core.QtRgba.BdrIcon
                        #
                        s_w, s_h = w*.5, h*.5
                        status_rect = qt_rect(
                            x+w-s_w, y+h-s_h, s_w, s_h
                        )
                        # draw status
                        if status in {self.ValidationStatus.Disable, self.ValidationStatus.Lost}:
                            painter._draw_icon_file_by_rect_(
                                rect=status_rect,
                                file_path=_gui_core.GuiIcon.get(
                                    'state-disable'
                                )
                            )
                        elif status in {self.ValidationStatus.Error, self.ValidationStatus.Unreadable}:
                            painter._draw_icon_file_by_rect_(
                                rect=status_rect,
                                file_path=_gui_core.GuiIcon.get(
                                    'state-lost'
                                )
                            )
                        elif status in {self.ValidationStatus.Locked, self.ValidationStatus.Unwritable}:
                            painter._draw_icon_file_by_rect_(
                                rect=status_rect,
                                file_path=_gui_core.GuiIcon.get(
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
                    menu_mark_rect = qt_rect(
                        x+w-m_w, y, m_w, m_h
                    )
                    painter._draw_icon_file_by_rect_(
                        rect=menu_mark_rect,
                        file_path=_gui_core.GuiIcon.get('menu-mark-h'),
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
            column, [_qt_core.QtCore.Qt.Unchecked, _qt_core.QtCore.Qt.Checked][boolean]
        )

    def _set_check_state_extra_(self, column=0):
        if self._check_action_is_enable is True:
            check_state = self.checkState(column)
            descendants = self._get_descendants_()
            [i.setData(column, QtCore.Qt.CheckStateRole, check_state, emit_send_enable=False) for i in descendants]
            ancestors = self._get_ancestors_()
            [
                i.setData(
                    column, QtCore.Qt.CheckStateRole, i._get_check_state_by_descendants_(column), emit_send_enable=False
                ) for i in ancestors
            ]

    def _set_checked_(self, boolean, column=0):
        self._set_check_state_(boolean, column)

    def _get_check_state_by_descendants_(self, column):
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
            return _qt_core.GuiQtTreeWidget.get_item_is_ancestor_hidden(qt_tree_widget, qt_tree_widget_item)
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

    def _initialize_item_show_(self):
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
                _ = bsc_core.ensure_string(text)
            #
            self.setText(column, _)
            self.setFont(column, _qt_core.QtFonts.NameNormal)

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
            text = bsc_core.ensure_string(text)
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
            title_text = bsc_core.ensure_string(title_text)
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

    def _do_delete_(self):
        if self.parent():
            index = self.parent().indexOfChild(self)
            self.parent().takeChild(index)

    def __str__(self):
        return '{}(names="{}")'.format(
            self.__class__.__name__, ', '.join(self._get_name_texts_())
        )

    def __repr__(self):
        return self.__str__()
