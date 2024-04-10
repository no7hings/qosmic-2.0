# coding:utf-8
import lxbasic.log as bsc_log
# katana
from ..core.wrap import *

from .. import core as ktn_core


class _AbsHotkey(object):
    KEY = 'hot key'


class ScpHotKeyForNodeGraphLayout(_AbsHotkey):
    """
# coding:utf-8
import lxkatana
lxkatana.set_reload()

import lxkatana.core as ktn_core

ktn_core.ScpHotKeyForNodeGraphLayout().register()
    """
    NAME = 'Node Graph Layout'
    ID = 'F4331532-D52B-11ED-8C7C-2CFDA1C062BB'
    HOT_KEY = 'Alt+L'

    @classmethod
    def release_fnc_(cls, ktn_gui):
        ss = NodegraphAPI.GetAllSelectedNodes()
        if ss:
            group = ktn_gui.getEnteredGroupNode()
            if group.getType() in {'NetworkMaterialCreate', 'ShadingGroup'}:
                ss_ = [i_s for i_s in ss if i_s.getParent() == group]
                ktn_core.NGGuiLayout(
                    ss_
                ).layout_shader_graph(
                    size=(320, 320)
                )

    def __init__(self):
        self._ktn_gui = App.Tabs.FindTopTab('Node Graph')

    def do_press(self, *args, **kwargs):
        pass

    def do_release(self, *args, **kwargs):
        ktn_gui = args[0]
        self.release_fnc_(ktn_gui)

    def register(self):
        bsc_log.Log.trace_method_result(
            self.KEY,
            'register: name is "{}", hot key is "{}"'.format(self.NAME, self.HOT_KEY)
        )
        self._ktn_gui.registerKeyboardShortcut(
            self.ID, self.NAME, self.HOT_KEY, self.do_press, self.do_release
        )


class ScpHotKeyForNodeGraphPaste(_AbsHotkey):
    NAME = 'Node Graph Paste'
    ID = 'F4331532-D52B-11ED-8C7C-2CFDA1C062BC'
    HOT_KEY = 'Alt+V'

    @classmethod
    def release_fnc_(cls, ktn_gui):
        node = ktn_gui.getEnteredGroupNode()
        # material and shader
        if node.getType() in {'NetworkMaterialCreate', 'ShadingGroup'}:
            import lxkatana.scripts as ktn_scripts

            ktn_scripts.ScpActionForNodeGraphMaterialPaste(
                node
            ).accept()
        # other
        elif node.getType() in {'RootNode', 'Group'}:
            import lxkatana.scripts as ktn_scripts

            node_under_mouse = ktn_gui.getNodeGraphWidget().getGroupNodeUnderMouse()
            ktn_scripts.ScpActionForNodeGraphGroupPaste(
                node_under_mouse
            ).accept()

    def __init__(self):
        self._ktn_gui = App.Tabs.FindTopTab('Node Graph')

    def do_press(self, *args, **kwargs):
        pass

    def do_release(self, *args, **kwargs):
        ktn_gui = args[0]
        self.release_fnc_(ktn_gui)

    def register(self):
        bsc_log.Log.trace_method_result(
            self.KEY,
            'register: name is "{}", hot key is "{}"'.format(self.NAME, self.HOT_KEY)
        )
        self._ktn_gui.registerKeyboardShortcut(
            self.ID, self.NAME, self.HOT_KEY, self.do_press, self.do_release
        )
