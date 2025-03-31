# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core


class ToolsetForConstraintDeform(
    gui_prx_widgets.PrxVirtualBaseUnit
):
    GUI_KEY = 'constrain_and_deform'

    def do_dcc_replace_motion_path_object(self):
        paths = cmds.ls(selection=1, type='transform', long=1) or []
        if len(paths) < 2:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.less_transforms')
                ),
                status='warning'
            )
            return

        qsm_mya_core.MotionPath.replace_all(paths)

    def do_dcc_curve_warp_path_object(self):
        paths = cmds.ls(selection=1, type='transform', long=1) or []
        if len(paths) < 2:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.less_transforms')
                ),
                status='warning'
            )
            return

        qsm_mya_core.CurveWarp.replace_all(paths)

    def do_dcc_create_for_lattice(self):
        paths = cmds.ls(selection=1, type='transform', long=1) or []
        if len(paths) < 2:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.less_transforms')
                ),
                status='warning'
            )
            return

        node, curve = paths[:2]
        qsm_mya_core.CurveWarp.create_for_lattice_0(node, curve)

    def __init__(self, window, page, session):
        super(ToolsetForConstraintDeform, self).__init__(window, page, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._page._configure.get('build.units.{}.options'.format(self.GUI_KEY))
            )
        )

        self._prx_options_node.build_by_data(
            self._page._configure.get('build.units.{}.options.parameters'.format(self.GUI_KEY)),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key=self.GUI_KEY,
            name=gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._page._configure.get('build.units.{}'.format(self.GUI_KEY))
            ),
            icon_name_text=self.GUI_KEY,
            tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                self._window._language, self._page._configure.get('build.units.{}'.format(self.GUI_KEY))
            )
        )

        self._prx_options_node.set(
            'motion_path.replace_object', self.do_dcc_replace_motion_path_object
        )

        self._prx_options_node.set(
            'curve_warp.replace_object', self.do_dcc_curve_warp_path_object
        )
        self._prx_options_node.set(
            'curve_warp.create_for_lattice', self.do_dcc_create_for_lattice
        )
