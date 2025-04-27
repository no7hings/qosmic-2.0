# coding:utf-8
import functools

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_resora.core.drag as lnx_rsr_cor_drag

import lnx_resora.gui.abstracts as lnx_rsr_gui_abstracts


class GuiResourceManagerMain(lnx_rsr_gui_abstracts.AbsPrxPageForManager):
    class DragMode:
        Reference = 'reference'
        Import = 'import'
        Open = 'open'

    def __init__(self, window, session, *args, **kwargs):
        super(GuiResourceManagerMain, self).__init__(window, session, *args, **kwargs)

    def _gui_add_drag_mode_switch_tools(self):
        cfg = [
            ('reference', 'resora/maya_reference'),
            ('import', 'resora/maya_import'),
            ('open', 'resora/maya_open')
        ]
        tools = []
        for i_drag_mode, i_icon_name in cfg:
            i_tool = gui_prx_widgets.PrxToggleButton()
            self._drag_mode_switch_prx_tool_box.add_widget(i_tool)

            i_tool._qt_widget._set_exclusive_widgets_(tools)
            i_tool.set_name(i_drag_mode)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip('"LMB-click" for switch to scale to "{}"'.format(i_drag_mode))

            if i_drag_mode == self._drag_mode:
                i_tool.set_checked(True)

            tools.append(i_tool._qt_widget)
            i_tool.connect_check_changed_as_exclusive_to(
                functools.partial(self._gui_switch_drag_mode, i_drag_mode)
            )

    def _gui_switch_drag_mode(self, drag_mode):
        if drag_mode != self._drag_mode:
            self._drag_mode = drag_mode

    def _gui_get_drag_mode(self):
        return self._drag_mode

    def gui_page_setup_sup_fnc(self):
        self._drag_mode = 'reference'

        self._drag_mode_switch_prx_tool_box = self.gui_add_top_tool_box('drag mode switch')
        self._gui_add_drag_mode_switch_tools()

    def gui_node_drag_data_generate_fnc(self, scr_entity):
        scr_entity_path = scr_entity.path

        source_path = self._scr_stage.get_node_parameter(scr_entity_path, 'source')
        if source_path:
            if self._drag_mode == self.DragMode.Import:
                lnx_rsr_cor_drag.MayaSceneFileMel.generate_import_mel(source_path)
            elif self._drag_mode == self.DragMode.Reference:
                lnx_rsr_cor_drag.MayaSceneFileMel.generate_reference_mel(source_path)
            elif self._drag_mode == self.DragMode.Open:
                lnx_rsr_cor_drag.MayaSceneFileMel.generate_open_mel(source_path)

            return dict(
                file=source_path,
                scr_entity_path=scr_entity_path
            )
