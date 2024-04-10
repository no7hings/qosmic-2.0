# coding:utf-8
import six

import os

import lxbasic.log as bsc_log
# katana
from .wrap import *


class KtnUtil(object):
    OBJ_PATHSEP = '/'

    PORT_PATHSEP = '.'

    @staticmethod
    def get_is_ui_mode():
        return Configuration.get('KATANA_UI_MODE') == '1'

    @staticmethod
    def get_katana_version():
        return os.environ['KATANA_VERSION']


class ResolutionOpt(object):
    def __init__(self, string):
        r = ResolutionTable.GetResolutionTable().getResolution(string)
        self._x, self._y = r.xres(), r.yres()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def get(self):
        return self._x, self._y


class GuiNodeGraphBase(object):
    @classmethod
    def get_node_position(cls, ktn_obj):
        if isinstance(ktn_obj, six.string_types):
            return NodegraphAPI.GetNodePosition(
                NodegraphAPI.GetNode(ktn_obj)
            )
        return NodegraphAPI.GetNodePosition(ktn_obj)

    @classmethod
    def set_node_position(cls, ktn_obj, position):
        if isinstance(ktn_obj, six.string_types):
            return NodegraphAPI.SetNodePosition(
                NodegraphAPI.GetNode(ktn_obj), position
            )
        return NodegraphAPI.SetNodePosition(ktn_obj, position)


class GuiNodeGraphOpt(GuiNodeGraphBase):
    def __init__(self, ktn_gui=None):
        if ktn_gui is None:
            self._ktn_gui = App.Tabs.FindTopTab('Node Graph').getNodeGraphWidget()
        else:
            self._ktn_gui = ktn_gui

    def get_track_position(self):
        x, y, z = self._ktn_gui.getEyePoint()
        return x, y

    def move_node_to_view_center(self, ktn_obj):
        x, y = self.get_track_position()
        self.set_node_position(ktn_obj, (x, y))

    @classmethod
    def import_nodes_from_file(cls, file_path):
        nodes = KatanaFile.Import(file_path, True)
        if nodes:
            tab = App.Tabs.FindTopTab('Node Graph')
            tab.prepareFloatingLayerWithPasteBounds(nodes)
            tab.enableFloatingLayer()

    @classmethod
    def drop_nodes(cls, nodes):
        if nodes:
            tab = App.Tabs.FindTopTab('Node Graph')
            tab.prepareFloatingLayerWithPasteBounds(nodes)
            tab.enableFloatingLayer()


class GuiNodeGraphTabOpt(GuiNodeGraphBase):
    LAYOUT_NODE_KEY = 'F4331532-D52B-11ED-8C7C-2CFDA1C062BB'

    def __init__(self, ktn_gui=None):
        if ktn_gui is None:
            self._ktn_gui = App.Tabs.FindTopTab('Node Graph')
        else:
            self._ktn_gui = ktn_gui

    def set_current_node(self, ktn_obj):
        self._ktn_gui.setCurrentNodeView(
            ktn_obj
        )

    def set_selection_view_fit(self):
        self._ktn_gui.frameSelection(zoom=False)

    def get_current_group(self):
        return self._ktn_gui.getEnteredGroupNode()

    def get_node_graph(self):
        return self._ktn_gui.getNodeGraphWidget()

    def get_node_graph_opt(self):
        return GuiNodeGraphOpt(self.get_node_graph())

    def add_hot_key(self, shortcut_id, name, shortcut, press_fnc, release_fnc):
        self._ktn_gui.registerKeyboardShortcut(
            shortcut_id, name, shortcut, press_fnc, release_fnc
        )


class Modifier(object):
    @staticmethod
    def undo_run(fnc):
        def sub_fnc_(*args, **kwargs):
            Utils.UndoStack.OpenGroup(fnc.__name__)
            # noinspection PyBroadException
            try:
                _fnc = fnc(*args, **kwargs)
                return _fnc
            except Exception:
                import lxbasic.core as bsc_core

                bsc_core.ExceptionMtd.set_print()
            #
            finally:
                Utils.UndoStack.CloseGroup()

        return sub_fnc_

    @staticmethod
    def undo_debug_run(fnc):
        def sub_fnc_(*args, **kwargs):
            Utils.UndoStack.OpenGroup(fnc.__name__)
            # noinspection PyBroadException
            try:
                _fnc = fnc(*args, **kwargs)
                return _fnc
            except Exception:
                if KtnUtil.get_is_ui_mode() is True:
                    import lxbasic.core as bsc_core
                    bsc_log.LogException.trace()
                else:
                    import lxbasic.core as bsc_core
                    bsc_core.ExceptionMtd.set_print()
                raise
            #
            finally:
                Utils.UndoStack.CloseGroup()

        return sub_fnc_


class CEL(object):
    def __init__(self, ktn_obj, cel):
        self._ktn_obj = ktn_obj
        self._cel = cel

    def parse(self):
        if self._cel:
            return Widgets.CollectAndSelectInScenegraph(
                self._cel, ''
            ).collectAndSelect(
                select=False, node=self._ktn_obj
            )
        return []
