# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

from . import qt as _qt


class ToolkitDockerBuild(object):
    @classmethod
    def test(cls):
        cls('maya/toolkits/main').execute()

    def __init__(self, cfg_key):
        self._c = bsc_resource.BscConfigure.get_as_content(cfg_key)
        self._language = gui_core.GuiUtil.get_language()

    def execute(self):
        dock_data = self._c.get('build.options')
        key = dock_data['key']
        if self._language == 'chs':
            label = dock_data['name_chs']
        else:
            label = dock_data['name']

        dock_tab_layout = _qt.ToolkitDocker.create_docker(key, label)

        tab_cfg_keys = dock_data['tabs']
        for i_cfg_key in tab_cfg_keys:
            ToolkitBuild(i_cfg_key).execute(dock_tab_layout)


class ToolkitBuild(object):

    def __init__(self, cfg_key):
        self._cfg_key = cfg_key
        self._c = bsc_resource.BscConfigure.get_as_content(cfg_key)
        self._language = gui_core.GuiUtil.get_language()

    def create_tab(self, dock_tab_layout, key, data):
        if self._language == 'chs':
            label = data.get('name_chs')
            tool_tip = data.get('tool_tip_chs')
        else:
            label = data.get('name')
            tool_tip = data.get('tool_tip')

        return _qt.ToolkitDocker.create_tab_at(dock_tab_layout, key, label, tool_tip)

    def create_qt_tool_area(self, qt_tab_widget, key, data):
        if self._language == 'chs':
            label = data.get('name_chs')
            tool_tip = data.get('tool_tip_chs')
        else:
            label = data.get('name')
            tool_tip = data.get('tool_tip')

        return _qt.ToolkitDocker.create_qt_tool_area_at(qt_tab_widget, key, label, tool_tip)

    def create_qt_tool_group(self, qt_tool_area, key, data, column_count=2):
        if self._language == 'chs':
            label = data.get('name_chs')
            tool_tip = data.get('tool_tip_chs')
        else:
            label = data.get('name')
            tool_tip = data.get('tool_tip')

        return _qt.ToolkitDocker.create_qt_tool_group_at(qt_tool_area, key, label, tool_tip, column_count)

    def create_qt_tool_button(self, qt_tool_group_widget, key, data):
        if self._language == 'chs':
            label = data.get('name_chs')
            tool_tip = data.get('tool_tip_chs')
        else:
            label = data.get('name')
            tool_tip = data.get('tool_tip')

        icon = data.get('icon')
        if icon:
            icon_file = gui_core.GuiIcon.get(data['icon'])
        else:
            icon_file = None

        script = data.get('script')

        actions = data.get('actions')
        if actions:
            menu_data = []
            for k, v in actions.items():
                if self._language == 'chs':
                    i_label = v['name_chs']
                else:
                    i_label = v['name']

                menu_data.append(
                    (i_label, None, v.get('script'))
                )
        else:
            menu_data = None

        return _qt.ToolkitDocker.create_qt_tool_button_at(
            qt_tool_group_widget, key, label, tool_tip, icon_file, script, menu_data
        )

    def execute(self, dock_tab_layout):
        shelf_data = self._c.get('build.options')

        qt_tool_area = None
        qt_tool_group = None
        for k, v in shelf_data.items():
            i_type = v['type']
            if i_type in {'tab', 'shelf'}:
                i_key = self._cfg_key.replace('/', '__')
                tab_layout = self.create_tab(dock_tab_layout, i_key, v)
                qt_tab_widget = _qt.QtUtil.to_qt_widget(tab_layout)
                qt_tool_area = self.create_qt_tool_area(qt_tab_widget, i_key, v)

            elif i_type in {'group', 'separator'}:
                i_key = k.replace('/', '__')
                # general instance all time
                qt_tool_group = self.create_qt_tool_group(qt_tool_area, i_key, v)

            elif i_type in {'tool', 'button'}:
                i_key = k.replace('/', '__')
                self.create_qt_tool_button(qt_tool_group, i_key, v)

