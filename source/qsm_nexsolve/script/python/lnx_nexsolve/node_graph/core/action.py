# coding:utf-8
import enum

from ...core import base as _scn_cor_base


class ActionFlags(enum.IntEnum):
    GraphTrackClick = 0x00
    GraphTrackMove = 0x01

    NodePressClick = 0x10
    NodePressMove = 0x11

    PortSourcePressClick = 0x20
    PortSourcePressMove = 0x21
    PortSourceHoverMove = 0x22
    PortTargetPressClick = 0x23
    PortTargetPressMove = 0x24
    PortTargetHoverMove = 0x25

    ConnectionSourcePressClick = 0x30
    ConnectionSourcePressMove = 0x31
    ConnectionSourceHoverMove = 0x32
    ConnectionTargetPressClick = 0x33
    ConnectionTargetPressMove = 0x34
    ConnectionTargetHoverMove = 0x35

    GroupPressClick = 0x50
    GroupPressMove = 0x51
    GroupResizePressClick = 0x52
    GroupResizePressMove = 0x53

    RectSelectPressClick = 0x60
    RectSelectPressMove = 0x61


class _AbsAction(object):
    ActionFlags = ActionFlags

    @property
    def gui_data(self):
        raise NotImplementedError()

    def _init_action(self):
        self.gui_data.action = _scn_cor_base._Dict(
            flag=None,
            sub_flag=None,
        )

    def set_action_flag(self, flag):
        self.gui_data.action.flag = flag

    def set_action_sub_flag(self, flag):
        self.gui_data.action.sub_flag = flag

    def is_action_flag_matching(self, *args):
        return self.gui_data.action.flag in args

    def is_action_sub_flag_matching(self, *args):
        return self.gui_data.action.sub_flag in args

    def clear_action_flag(self):
        self.gui_data.action.flag = None

    def clear_action_sub_flag(self):
        self.gui_data.action.sub_flag = None