# coding:utf-8
import math

import collections

import functools

import time

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from . import worker as _worker


# item model
class _SpcTaskItemModel(object):
    Status = _gui_core.GuiProcessStatus

    def __init__(self, item):
        self._item = item
        self._data = _gui_core.DictOpt()
        self._data.force_refresh_flag = True
        # main
        self._data.rect = qt_rect()
        # basic
        self._data.basic = _gui_core.DictOpt(
            rect=qt_rect(),
            size=QtCore.QSize(),
        )
        # text option for draw
        self._data.text = _gui_core.DictOpt(
            font=_qt_core.QtFont.generate(size=8),
            color=QtGui.QColor(223, 223, 223),
            action_color=QtGui.QColor(255, 255, 255),
            # all text height
            height=20
        )
        # path
        self._data.path = _gui_core.DictOpt(
            text=None
        )
        # index
        self._data.index = 0
        self._data.icon_enable = False
        # icon
        self._data.icon = _gui_core.DictOpt(
            file_flag=False,
            file=None,
            rect=qt_rect(),
        )
        # type
        self._data.type = _gui_core.DictOpt(
            text=None
        )
        # name
        self._data.name = _gui_core.DictOpt(
            text=None,
            rect=qt_rect(),
        )
        # hover
        self._data.hover = _gui_core.DictOpt(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightOrange),
        )
        # select
        self._data.select = _gui_core.DictOpt(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue),
        )
        # menu
        self._data.menu = _gui_core.DictOpt(
            content=None,
            content_generate_fnc=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )

        color, color_hover = _qt_core.QtItemDrawBase._gen_rgba_args_by_status(
            self.Status.Waiting
        )
        self._percent_mark = 0
        # progress

        self._data.progress = _gui_core.DictOpt(
            base=_gui_core.DictOpt(
                rect=QtCore.QRect(),
                border_color=QtGui.QColor(*_gui_core.GuiRgba.Gray),
                backgroup_color=QtGui.QColor(*_gui_core.GuiRgba.Dim),
            ),
            rect=QtCore.QRect(),
            color=color,
            color_hover=color_hover,
            color_base=QtGui.QColor(*_gui_core.GuiRgba.Gray),
            #
            text=None,
            text_rect=QtCore.QRect(),
            # default us None
            maximum=None,
            value=0,
            index=0,
            height=10,
            #
            start_timestamp=None,
            finish_timestamp=None,
            #
            finish_flag=False,
            stop_flag=False,
            kill_flag=False,
            #
            status=self.Status.Waiting,
            status_text=_gui_core.GuiProcessStatusMapper.get_name(self.Status.Waiting),
            #
            percent_index=0,
            percent=0,
            percent_pre=0,
            percent_rect=QtCore.QRect(),
            percent_text='0%',
        )

        self._trd = None
        self._profile = None
        self._sprc_memory_sizes = []

    @property
    def data(self):
        return self._data

    def set_path(self, path):
        self._data.path.text = path

    def get_path(self):
        return self._data.path.text

    def set_index(self, index):
        self._data.index = index

    def get_index(self):
        return self._data.index

    # icon
    def set_icon_name(self, icon_name):
        # do not check file exists
        file_path = _gui_core.GuiIcon.get(icon_name)
        if file_path:
            self._data.icon_enable = True
            self._data.icon.file_flag = True
            self._data.icon.file = file_path

    # type
    def set_type(self, text):
        if text is not None:
            self._data.type.text = text
            return True
        return False

    def get_type(self):
        return self._data.type.text

    def set_name(self, text):
        if text is not None:
            self._data.name.text = text
            return True
        return False

    def get_name(self):
        return self._data.name.text

    # menu
    def set_menu_content(self, content):
        self._data.menu.content = content

    def get_menu_content(self):
        return self._data.menu.content

    def set_menu_data(self, data):
        self._data.menu.data = data

    def get_menu_data(self):
        return self._data.menu.data

    def set_menu_data_generate_fnc(self, fnc):
        self._data.menu.data_generate_fnc = fnc

    def get_menu_data_generate_fnc(self):
        return self._data.menu.data_generate_fnc

    def set_menu_name_dict(self, dict_):
        if isinstance(dict_, dict):
            self._data.menu.name_dict = dict_

    def get_menu_name_dict(self):
        return self._data.menu.name_dict

    # progress
    def set_maximum(self, value):
        if value != self._data.progress.maximum:
            self._data.progress.maximum = int(value)

    def get_maximum(self):
        return self._data.progress.maximum

    def set_value(self, value):
        if value != self._data.progress.value:
            self._data.progress.value = int(value)
            self._data.progress.percent_pre = self._data.progress.percent
            self._data.progress.percent = float(self._data.progress.value)/float(self._data.progress.maximum)
            # reset progress sub area
            self._data.progress.index = 0

    def set_percent(self, value):
        if value != self._data.progress.percent:
            self._data.progress.percent_pre = self._data.progress.percent
            self._data.progress.percent = float(value)
            # reset progress sub area
            self._data.progress.index = 0

    def get_value(self):
        return self._data.progress.value

    def get_percent(self):
        return self._data.progress.percent

    def append_maximum(self, value):
        if self._data.progress.maximum is None:
            self._data.progress.maximum = int(value)
        else:
            self._data.progress.maximum += int(value)

    def is_stopped(self):
        return self._data.progress.stop_flag is True

    def get_is_finished(self):
        return self._data.progress.finish_flag is True

    def get_is_killed(self):
        return self._data.progress.kill_flag is True

    def set_status(self, status):
        if self._data.progress.stop_flag is True:
            return False

        if status != self._data.progress.status:
            self._data.progress.status = status
            self._data.progress.status_text = _gui_core.GuiProcessStatusMapper.get_name(status)
            color, color_hover = _qt_core.QtItemDrawBase._gen_rgba_args_by_status(
                self._data.progress.status
            )
            self._data.progress.color = color
            self._data.progress.color_hover = color
            return True
        return False

    def get_status(self):
        return self._data.progress.status

    def get_status_name(self):
        return self._data.progress.status_text

    def _check_finish_flag(self):
        return self._data.progress.status in {
            self.Status.Completed,
            self.Status.Failed,
            self.Status.Error,
            self.Status.Killed,
        }

    def _do_stop(self):
        self._data.progress.stop_flag = True

        self._data.progress.text = self._generate_text()
        self._data.progress.finish_timestamp = time.time()
        # when progress is not to end, reset the index
        self._data.progress.index = 0

    def _do_kill(self):
        if self._data.progress.kill_flag is False:
            self._data.progress.kill_flag = True

            if self._trd is not None:
                self._trd.do_kill()
            else:
                self._update_status(self.Status.Killed)

    def _do_quit(self):
        if self._data.progress.finish_flag is False:

            self._do_kill()

            if self._trd is not None:
                self._trd.do_quit()

    def _on_started(self):
        self._profile.update_timestamp('started')
        if self._trd is not None:
            # use tag in profile
            self._profile.update('tag', self._data.type.text)
            self._profile.update('name', self._data.name.text)
            self._profile.update('command', self._trd.fnc_string)

    def _on_finished(self):
        self._profile.update_timestamp('finished')
        if self._trd is not None:
            self._profile.update('status', int(self._trd.status))
            if self._sprc_memory_sizes:
                memory_size = max(self._sprc_memory_sizes)
                self._profile.update('memory_size', memory_size)
                self._profile.update('memory_size_string', bsc_core.BscInteger.to_prettify_as_file_size(memory_size))

    def _on_completed(self):
        pass

    def _on_failed(self, results):
        def fnc_(file_path_):
            bsc_storage.StgPath.start_in_system(file_path_)

        if results:
            file_path = bsc_log.LogBase.get_user_debug_file(
                'process', create=True
            )
            bsc_storage.StgFileOpt(
                file_path
            ).set_write(''.join(results))

            self.set_menu_data(
                [
                    ('Show Error', 'file/file', functools.partial(fnc_, file_path))
                ]
            )

    def _on_killed(self):
        pass

    def _on_system_resource_usage_update_(self, data):
        memory_size = data['memory_size']
        self._sprc_memory_sizes.append(memory_size)

    def _generate_thread(self, widget):
        self._profile = bsc_storage.Profile.generate()

        self._trd = _worker._QtSpcTaskThreadWorker.generate(widget, self)

        self._trd.started.connect(self._on_started)
        self._trd.finished.connect(self._on_finished)
        self._trd.completed.connect(self._on_completed)
        self._trd.failed.connect(self._on_failed)
        self._trd.killed.connect(self._on_killed)

        self._trd.system_resource_usage_update.connect(self._on_system_resource_usage_update_)
        return self._trd

    def _update_status(self, status):
        if self.set_status(status) is True:
            if self._data.progress.status == self.Status.Started:
                self._data.progress.start_timestamp = time.time()

            self._data.progress.finish_flag = self._check_finish_flag()

            if self._data.progress.finish_flag is True:
                self._do_stop()

            self._item.treeWidget().status_changed.emit()

    def _update_percent(self, percent):
        self.set_percent(percent)

    def _update_maximum(self, value):
        self.append_maximum(value)

    def _update_log(self, text):
        pass

    def _generate_text(self):
        cost_time = self._compute_cost_time()
        if self._data.name.text:
            return '{}, {}, {}'.format(
                bsc_core.ensure_string(self._data.name.text),
                bsc_core.BscInteger.second_to_time_prettify(cost_time, mode=1),
                self._data.progress.status_text

            )
        return '{}, {}'.format(
            bsc_core.BscInteger.second_to_time_prettify(cost_time, mode=1),
            self._data.progress.status_text

        )

    def _compute_cost_time(self):
        if self._data.progress.start_timestamp is None:
            return 0
        if self._data.progress.finish_timestamp is None:
            return time.time()-self._data.progress.start_timestamp
        return self._data.progress.finish_timestamp-self._data.progress.start_timestamp

    def _update_hover(self, flag):
        if flag != self._data.hover.flag:
            self._data.hover.flag = flag

    # select
    def _update_select(self, flag):
        if flag != self._data.select.flag:
            self._data.select.flag = flag

    def update(self, rect):
        self._data.progress.index += 1

        # check rect is change
        if rect != self._data.rect or self._data.force_refresh_flag is True:
            self._data.rect = qt_rect(rect)

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

            spc = 2

            text = self._generate_text()
            self._data.progress.text = text

            txt_font = self.data.text.font
            txt_h = self.data.text.height

            icn_w = 16
            icn_y = y+((txt_h-icn_w)/2)
            icon_frm_w = 0
            if self._data.icon_enable is True:
                icon_frm_w = 20
                self._data.icon.rect.setRect(
                    x+(icon_frm_w-icn_w)/2, icn_y, icn_w, icn_w
                )

            prc_w, prc_h = w-2, self._data.progress.height
            prc_x, prc_y = x+1, y+(h-prc_h)

            self._data.progress.base.rect.setRect(
                prc_x, prc_y, prc_w, prc_h
            )

            p_b_w_a = 20
            p_b_w_b = prc_w-p_b_w_a

            if self._data.progress.status == self.Status.Completed:
                percent, percent_pre = 1.0, self._data.progress.percent_pre
            else:
                percent, percent_pre = self._data.progress.percent, self._data.progress.percent_pre

            index = min(self._data.progress.index, 10)
            d = (percent-percent_pre)/2
            p_d = sum([(1.0/(2**i))*d for i in range(index)])

            percent_text = '%3d%%' % (math.ceil((percent_pre+p_d)*100))
            self._data.progress.rect.setRect(
                prc_x+1, prc_y+1, p_b_w_a+math.ceil(p_b_w_b*(percent_pre+p_d))-2, prc_h-2
            )

            self._data.progress.percent_text = percent_text

            percent_txt_w = QtGui.QFontMetrics(txt_font).width(percent_text)+16

            self._data.progress.percent_rect.setRect(
                x+w-percent_txt_w, y, percent_txt_w, txt_h
            )

            txt_w = QtGui.QFontMetrics(txt_font).width(text)+16
            txt_w = min(txt_w, w-percent_txt_w-8)
            self._data.progress.text_rect.setRect(
                x+icon_frm_w+spc, y, txt_w, txt_h
            )
            return True
        return False

    def draw(self, painter, option, index):
        painter.save()

        column = index.column()
        # update for column 1
        if column == 0:
            self.update(option.rect)

        self._update_select(not not option.state & QtWidgets.QStyle.State_Selected)
        self._update_hover(not not option.state & QtWidgets.QStyle.State_MouseOver)

        if column == 0:
            self.draw_base(painter, option, index)
            self.draw_text(painter, option, index)
            if self._data.icon.file_flag is True:
                _qt_core.QtItemDrawBase._draw_icon_by_file(painter, self._data.icon.rect, self._data.icon.file)

        painter.restore()

    def draw_base(self, painter, option, index):
        assert isinstance(painter, QtGui.QPainter)

        painter.setRenderHint(painter.Antialiasing, True)

        _qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=self._data.progress.base.rect,
            border_color=self._data.progress.base.border_color,
            background_color=self._data.progress.base.backgroup_color,
            border_radius=2
        )

        if self._data.progress.finish_flag is True:
            _qt_core.QtItemDrawBase._draw_frame(
                painter,
                rect=self._data.progress.rect,
                border_color=self._data.progress.color,
                background_color=self._data.progress.color,
                border_radius=2
            )
        else:
            _qt_core.QtItemDrawBase._draw_alternating_frame(
                painter,
                rect=self._data.progress.rect,
                colors=[self._data.progress.color, self._data.progress.color_base],
                border_radius=2,
                running=not self._data.progress.finish_flag
            )

    def draw_text(self, painter, option, index):
        column = index.column()
        if column == 0:
            text_color = [
                self._data.text.color, self._data.text.action_color
            ][self._data.select.flag or self._data.hover.flag]

            painter.setFont(self._data.text.font)
            _qt_core.QtItemDrawBase._draw_name_text(
                painter, self._data.progress.text_rect, self._data.progress.text,
                text_color, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
            )

            _qt_core.QtItemDrawBase._draw_name_text(
                painter, self._data.progress.percent_rect, self._data.progress.percent_text,
                text_color, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
            )


class _SpcTaskGroupItemModel(object):
    def __init__(self, item):
        self._item = item
        self._data = _gui_core.DictOpt()
        self._data.force_refresh_flag = True
        # main
        self._data.rect = qt_rect()
        # basic
        self._data.basic = _gui_core.DictOpt(
            rect=qt_rect(),
            size=QtCore.QSize(),
        )
        # text option for draw
        self._data.text = _gui_core.DictOpt(
            font=_qt_core.QtFont.generate(size=8),
            color=QtGui.QColor(223, 223, 223),
            action_color=QtGui.QColor(255, 255, 255),
            # all text height
            height=20
        )
        # path
        self._data.path = _gui_core.DictOpt(
            text=None
        )
        # index
        self._data.index = 0
        self._data.icon_enable = False
        # icon
        self._data.icon = _gui_core.DictOpt(
            file_flag=False,
            file=None,
            rect=qt_rect(),
        )
        # type
        self._data.type = _gui_core.DictOpt(
            text=None
        )
        # name
        self._data.name = _gui_core.DictOpt(
            text=None,
            rect=qt_rect(),
        )
        # hover
        self._data.hover = _gui_core.DictOpt(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightOrange),
        )
        # select
        self._data.select = _gui_core.DictOpt(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue),
        )
        # menu
        self._data.menu = _gui_core.DictOpt(
            content=None,
            content_generate_fnc=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )

    @property
    def data(self):
        return self._data

    def set_path(self, path):
        self._data.path.text = path

    def get_path(self):
        return self._data.path.text

    def set_index(self, index):
        self._data.index = index

    def get_index(self):
        return self._data.index

    # icon
    def set_icon_name(self, icon_name):
        # do not check file exists
        file_path = _gui_core.GuiIcon.get(icon_name)
        if file_path:
            self._data.icon_enable = True
            self._data.icon.file_flag = True
            self._data.icon.file = file_path

    # type
    def set_type(self, text):
        if text is not None:
            self._data.type.text = text
            return True
        return False

    def get_type(self):
        return self._data.type.text

    def set_name(self, text):
        if text is not None:
            self._data.name.text = text
            return True
        return False

    def get_name(self):
        return self._data.name.text

    # menu
    def set_menu_content(self, content):
        self._data.menu.content = content

    def get_menu_content(self):
        return self._data.menu.content

    def set_menu_data(self, data):
        self._data.menu.data = data

    def get_menu_data(self):
        return self._data.menu.data

    def set_menu_data_generate_fnc(self, fnc):
        self._data.menu.data_generate_fnc = fnc

    def get_menu_data_generate_fnc(self):
        return self._data.menu.data_generate_fnc

    def set_menu_name_dict(self, dict_):
        if isinstance(dict_, dict):
            self._data.menu.name_dict = dict_

    def get_menu_name_dict(self):
        return self._data.menu.name_dict

    def _update_hover(self, flag):
        if flag != self._data.hover.flag:
            self._data.hover.flag = flag

    # select
    def _update_select(self, flag):
        if flag != self._data.select.flag:
            self._data.select.flag = flag

    def update(self, rect):
        # check rect is change
        if rect != self._data.rect or self._data.force_refresh_flag is True:
            self._data.rect = qt_rect(rect)

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

            spc = 2

            text = self._data.name.text

            txt_font = self.data.text.font
            txt_h = self.data.text.height

            icn_w = 16
            icn_y = y+((txt_h-icn_w)/2)
            icon_frm_w = 0
            if self._data.icon_enable is True:
                icon_frm_w = 20
                self._data.icon.rect.setRect(
                    x+(icon_frm_w-icn_w)/2, icn_y, icn_w, icn_w
                )

            txt_w = QtGui.QFontMetrics(txt_font).width(text)+16
            self._data.name.rect.setRect(
                x+icon_frm_w+spc, y, txt_w, txt_h
            )

            return True
        return False

    def draw(self, painter, option, index):
        painter.save()

        column = index.column()
        # update for column 1
        if column == 0:
            self.update(option.rect)

        self._update_select(not not option.state & QtWidgets.QStyle.State_Selected)
        self._update_hover(not not option.state & QtWidgets.QStyle.State_MouseOver)

        if column == 0:
            self.draw_base(painter, option, index)
            self.draw_text(painter, option, index)
            if self._data.icon.file_flag is True:
                _qt_core.QtItemDrawBase._draw_icon_by_file(painter, self._data.icon.rect, self._data.icon.file)

        painter.restore()

    def draw_base(self, painter, option, index):
        pass

    def draw_text(self, painter, option, index):
        column = index.column()
        if column == 0:
            text_color = [
                self._data.text.color, self._data.text.action_color
            ][self._data.select.flag or self._data.hover.flag]

            painter.setFont(self._data.text.font)
            _qt_core.QtItemDrawBase._draw_name_text(
                painter, self._data.name.rect, self._data.name.text,
                text_color, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
            )


# view model
class _SpcTaskViewModel(object):
    def __init__(self, widget):
        self._widget = widget
        self._data = _gui_core.DictOpt()
        # item query
        self._data.item_dict = collections.OrderedDict()
        self._data.item = _gui_core.DictOpt(
            cls=None,
            group_cls=None,
            grid_size=QtCore.QSize(128, 30),
            group_grid_size=QtCore.QSize(128, 20),
        )
        # menu
        self._data.menu = _gui_core.DictOpt(
            content=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )

        self._overview_widget = None

        self._data.overview = _gui_core.DictOpt(
            base_rect=QtCore.QRect(),
            text_font=_qt_core.QtFont.generate(size=10),
            text_color=QtGui.QColor(31, 31, 31),
            keys=[],
            paths=[],
            path_dict=dict(),
            draw_data=[],
        )

    @property
    def data(self):
        return self._data

    def create_root_item(self, **kwargs):
        if 'path' not in kwargs:
            kwargs['path'] = '/'

        if 'name' not in kwargs:
            kwargs['name'] = 'All'

        _ = self.create_group_item(**kwargs)
        if _[0] is True:
            _[1].setExpanded(True)
        return _

    def create_group_item(self, path, *args, **kwargs):
        if path in self._data.item_dict:
            return False, self._data.item_dict[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        index_cur = len(self._data.item_dict)
        item = self._data.item.group_cls()
        if path_opt.get_is_root():
            self._widget.addTopLevelItem(item)
        else:
            parent_path = path_opt.get_parent_path()
            # maybe add a path to root
            if parent_path not in self._data.item_dict:
                self._widget.addTopLevelItem(item)
            else:
                parent_item = self._data.item_dict[parent_path]
                if isinstance(parent_item, QtWidgets.QTreeWidgetItem) is False:
                    raise RuntimeError()

                parent_item.addChild(item)

        item.setText(0, str(index_cur).zfill(4))

        item_model = item._model
        item_model.set_path(path)
        item_model.set_index(index_cur)
        item_model.set_name(kwargs.get('name', path_opt.get_name()))
        item_model.set_icon_name(kwargs.get('icon_name', 'database/all'))

        item.setSizeHint(0, self.data.item.group_grid_size)

        self._data.item_dict[path] = item
        return True, item

    def create_item(self, path, *args, **kwargs):
        if path in self._data.item_dict:
            return False, self._data.item_dict[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        index_cur = len(self._data.item_dict)
        item = self._data.item.cls()
        if path_opt.get_is_root():
            self._widget.addTopLevelItem(item)
        else:
            parent_path = path_opt.get_parent_path()
            # maybe add a path to root
            if parent_path not in self._data.item_dict:
                self._widget.addTopLevelItem(item)
            else:
                parent_item = self._data.item_dict[parent_path]
                if isinstance(parent_item, QtWidgets.QTreeWidgetItem) is False:
                    raise RuntimeError()

                parent_item.addChild(item)

        item.setText(0, str(index_cur).zfill(4))

        item_model = item._model
        item_model.set_path(path)
        item_model.set_index(index_cur)
        item_model.set_name(kwargs.get('name', path_opt.get_name()))
        item_model.set_icon_name(kwargs.get('icon_name', 'database/object'))

        item.setSizeHint(0, self.data.item.grid_size)

        self._data.item_dict[path] = item
        return True, item

    def get_all_items(self, column=0):
        def rcs_fnc_(index_):
            # top level
            if index_ is None:
                _row_count = model.rowCount()
            else:
                _row_count = model.rowCount(index_)
                list_.append(self._widget.itemFromIndex(index_))
            #
            for _i_row in range(_row_count):
                # top level
                if index_ is None:
                    _index = model.index(_i_row, column)
                else:
                    _index = index_.child(_i_row, index_.column())

                if _index.isValid():
                    rcs_fnc_(_index)

        list_ = []
        model = self._widget.model()

        rcs_fnc_(None)
        return list_

    def draw_item(self, painter, option, index):
        self._widget.itemFromIndex(index)._model.draw(painter, option, index)

    # menu
    def set_menu_content(self, content):
        self._data.menu.content = content

    def get_menu_content(self):
        return self._data.menu.content

    def set_menu_data(self, data):
        self._data.menu.data = data

    def get_menu_data(self):
        return self._data.menu.data

    def set_menu_data_generate_fnc(self, fnc):
        self._data.menu.data_generate_fnc = fnc

    def get_menu_data_generate_fnc(self):
        return self._data.menu.data_generate_fnc

    def set_menu_name_dict(self, dict_):
        if isinstance(dict_, dict):
            self._data.menu.name_dict = dict_

    def get_menu_name_dict(self):
        return self._data.menu.name_dict

    def submit_cmd_script(
        self, type_name, name, cmd_script,
        completed_fnc=None, failed_fnc=None,
        check_memory_prc_name=None,
        application='python'
    ):
        flag, item = self.create_item('/{}'.format(name))
        # task name
        item._model.set_icon_name('application/{}'.format(application))
        item._model.set_type(type_name)
        trd = item._model._generate_thread(self._widget)
        trd.set_fnc(cmd_script)
        if completed_fnc is not None:
            if isinstance(completed_fnc, (tuple, list)):
                [trd.completed.connect(x) for x in completed_fnc]
            else:
                trd.completed.connect(completed_fnc)
        if check_memory_prc_name is not None:
            trd.check_memory_for(check_memory_prc_name)
        trd.start()
        return trd

    def submit_fnc(
        self, type_name, name, fnc, args=None, kwargs=None,
        completed_fnc=None, failed_fnc=None,
    ):
        flag, item = self.create_item('/{}'.format(name))
        # task name
        item._model.set_icon_name('application/python')
        item._model.set_type(type_name)
        trd = item._model._generate_thread(self._widget)
        trd.set_fnc(fnc, *args or (), **kwargs or {})
        if completed_fnc is not None:
            if isinstance(completed_fnc, (tuple, list)):
                [trd.completed.connect(x) for x in completed_fnc]
            else:
                trd.completed.connect(completed_fnc)
        trd.start()
        return trd

    def do_quit(self):
        self._widget._thread_terminate_flag = True

        for i in self.get_all_items():
            if i.GROUP_FLAG is False:
                i._model._do_quit()

    def set_overview_widget(self, widget):
        self._overview_widget = widget
        # use signal to update
        self._widget.status_changed.connect(self.update_overview)

    def update_overview(self):
        if self._overview_widget is not None:
            path_dict = {}
            paths = []
            for i in self.get_all_items():
                if i.GROUP_FLAG is False:
                    i_item_model = i._model
                    i_path = i_item_model.get_path()
                    i_status_all = int(i_item_model.Status.All)
                    i_status_all_text = _gui_core.GuiProcessStatusMapper.get_name(i_item_model.Status.All)
                    path_dict.setdefault((i_status_all, i_status_all_text), set()).add(i_path)
                    i_status = int(i_item_model.get_status())
                    i_status_text = i_item_model.get_status_name()
                    path_dict.setdefault((i_status, i_status_text), set()).add(i_path)
                    paths.append(i_path)

            keys = list(path_dict.keys())
            keys.sort()

            self._data.overview.keys = keys
            self._data.overview.path_dict = path_dict
            self._data.overview.paths = paths

            self._overview_widget._refresh_widget_all_()