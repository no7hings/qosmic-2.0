# coding:utf-8
import collections

import lxbasic.core as bsc_core
# gui
from .... import core as _gui_core

from ...core.wrap import *

from ....qt import core as _qt_core


# item model
class _QtSceneItemModel(object):
    def __init__(self, item):
        self._item = item
        self._data = _gui_core.BaseData()
        # refresh
        self._data.force_refresh_flag = True
        # main
        self._data.rect = qt_rect()
        # basic
        self._data.basic = _gui_core.BaseData(
            rect=qt_rect(),
            size=QtCore.QSize(),
        )
        # text option for draw
        self._data.text = _gui_core.BaseData(
            font=_qt_core.QtFont.generate(size=8),
            color=QtGui.QColor(223, 223, 223),
            action_color=QtGui.QColor(255, 255, 255),
            # all text height
            height=20
        )
        # path
        self._data.path = _gui_core.BaseData(
            text=None
        )
        # index
        self._data.index = 0
        self._data.icon_enable = False
        # icon
        self._data.icon = _gui_core.BaseData(
            file_flag=False,
            file=None,
            rect=qt_rect(),
        )
        # type
        self._data.type = _gui_core.BaseData(
            text=None
        )
        # name
        self._data.name = _gui_core.BaseData(
            text=None,
            rect=qt_rect(),
        )
        # hover
        self._data.hover = _gui_core.BaseData(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightOrange),
        )
        # select
        self._data.select = _gui_core.BaseData(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue),
        )
        # menu
        self._data.menu = _gui_core.BaseData(
            content=None,
            content_generate_fnc=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )

    @property
    def data(self):
        return self._data

    def update(self, rect):
        print(rect)

    def draw(self, painter, option):
        painter.save()

        self.update(option.rect)

        painter.restore()


# view model
class _QtSceneViewModel(object):
    def __init__(self, widget):
        self._widget = widget
        self._data = _gui_core.BaseData()

        self._data.item_dict = collections.OrderedDict()

    @property
    def data(self):
        return self._data

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

        item_model = item._item_model
        item_model.set_path(path)
        item_model.set_index(index_cur)
        item_model.set_name(kwargs.get('name', path_opt.get_name()))
        item_model.set_icon_name(kwargs.get('icon_name', 'database/object'))

        item.setSizeHint(0, self.data.item.grid_size)

        self._data.item_dict[path] = item
        return True, item


class _QtSceneItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args):
        super(_QtSceneItem, self).__init__(*args)
        self.setFlag(self.ItemIsMovable)

        self._item_model = _QtSceneItemModel(self)

    def paint(self, painter, option, widget=None):
        self._item_model.draw(painter, option)


class _QtSceneView(QtWidgets.QGraphicsView):
    def __init__(self, *args):
        super(_QtSceneView, self).__init__(*args)
        self.setAutoFillBackground(True)
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)

        self.setStyleSheet(_qt_core.QtStyle.get('QGraphicsView'))

        self._view_model = _QtSceneViewModel(self)


class QtSceneWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSceneWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._mrg = 4

        self._grid_lot = QtWidgets.QGridLayout(self)
        self._grid_lot.setContentsMargins(*[self._mrg]*4)
        self._grid_lot.setSpacing(2)

        self._view = _QtSceneView()
        self._grid_lot.addWidget(self._view, 0, 0, 1, 1)
        self._view.setFocusProxy(self)

        self._scene = QtWidgets.QGraphicsScene()
        self._view.setScene(self._scene)

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
        painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Dim))
        painter.drawRect(f_x, f_y, f_w, f_h)
