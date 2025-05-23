# coding:utf-8
import six

import lxgui.qt.toolkit as gui_qt_toolkit

from ..core.wrap import *


class QtUtil:
    @classmethod
    def to_qt_widget(cls, maya_gui_name):
        ptr = OpenMayaUI.MQtUtil.findLayout(maya_gui_name)

        if ptr is not None:
            if six.PY2:
                # noinspection PyCompatibility
                return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)
            return shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)

    @classmethod
    def to_qt_layout(cls, maya_gui_name):
        qt_widget = cls.to_qt_widget(maya_gui_name)
        if qt_widget:
            return qt_widget.layout()


class ToolkitDocker:
    @classmethod
    def create_docker(cls, name, label=None, width=400):
        # window
        window_name = '{}_window'.format(name)
        if cmds.window(window_name, query=1, exists=1):
            cmds.deleteUI(window_name)
        window = cmds.window(
            window_name,
            width=width, sizeable=1,
            parent='MayaWindow'
        )

        # tab layout
        tab_layout_name = '{}_tab_layout'.format(name)
        tab_layout = cmds.tabLayout(
            tab_layout_name,
            innerMarginWidth=4, innerMarginHeight=4,
            minChildWidth=width, childResizable=1,
            parent=window,
            # minimum width
            width=240
        )

        # dock control
        dock_control_name = '{}_dock_control'.format(name)
        if cmds.dockControl(dock_control_name, query=1, exists=1):
            cmds.deleteUI(dock_control_name)

        dock_control = cmds.dockControl(
            dock_control_name, label=label or name,
            content=window,
            area='left', allowedArea=['left', 'right'],
            sizeable=1, width=width
        )
        return tab_layout

    @classmethod
    def create_tab_at(cls, dock_tab_layout, name, label=None, tool_tip=None):
        # scroll layout
        scroll_layout_name = '{}_scroll_layout'.format(name)
        scroll_layout = cmds.scrollLayout(scroll_layout_name, childResizable=1, parent=dock_tab_layout)
        cmds.tabLayout(
            dock_tab_layout, edit=1,
            tabLabel=[(scroll_layout_name, label or name)],
            tabTooltip=[(scroll_layout_name, tool_tip or name)]
        )

        # layout
        layout_name = '{}_layout'.format(name)
        layout = cmds.columnLayout(layout_name, adjustableColumn=1, rowSpacing=2, parent=scroll_layout)
        return layout

    @classmethod
    def create_qt_tool_area_at(
        cls, qt_tab_widget, name, label=None, tool_tip=None
    ):
        qt_widget = gui_qt_toolkit.QtToolPage()
        qt_tab_widget.layout().addWidget(qt_widget)
        return qt_widget

    @classmethod
    def create_qt_tool_group_at(
        cls, qt_tool_area, name, label=None, tool_tip=None, column_count=1
    ):
        qt_widget = gui_qt_toolkit.QtToolGroup()
        qt_tool_area.model.add_group(qt_widget)
        qt_widget.model.set_expanded(True)
        qt_widget.model.set_label(label or name)
        qt_widget.model.set_tool_tip(tool_tip)
        qt_widget.model.set_column_count(column_count)
        return qt_widget

    @classmethod
    def create_qt_tool_button_at(
        cls, qt_tool_group_widget, name, label=None, tool_tip=None, icon_file=None, script=None, menu_data=None
    ):
        qt_widget = gui_qt_toolkit.QtTool()
        qt_tool_group_widget.model.add_tool(qt_widget)
        qt_widget.model.set_icon_file(icon_file)
        qt_widget.model.set_label(label or name)
        qt_widget.model.set_tool_tip(tool_tip)
        qt_widget.model.connect_press_clicked_to(script)

        qt_widget.model.set_menu_data(menu_data)

