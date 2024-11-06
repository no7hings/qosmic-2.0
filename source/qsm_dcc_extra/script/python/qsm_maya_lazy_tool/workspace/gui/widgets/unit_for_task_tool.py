# coding:utf-8
import lxbasic.core as bsc_core

from qsm_lazy_tool.workspace.gui.abstracts import unit_for_task_tool as _abs_unit_for_task_tool

import lxgui.qt.core as gui_qt_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.steps.cfx_rig.core as qsm_mya_stp_cfx_rig_core


class GuiNodeOptForCfxRigTool(_abs_unit_for_task_tool.AbsGuiNodeOptForTaskTool):
    def on_dcc_select_node(self):
        selected_items = self._qt_tree_widget._view_model.get_selected_items()
        if selected_items:
            lst = []
            for i in selected_items:
                i_node = i._item_model.get_assign_data('node')
                if i_node:
                    lst.append(i_node)

            qsm_mya_core.Selection.set(lst)
        else:
            qsm_mya_core.Selection.clear()

    def __init__(self, *args, **kwargs):
        super(GuiNodeOptForCfxRigTool, self).__init__(*args, **kwargs)

        self._component_data = {}

        self._qt_tree_widget._view.item_select_changed.connect(
            self.on_dcc_select_node
        )

    def do_gui_refresh_all(self, force=False):
        if self._page._task_tool_opt is not None:
            data_pre = self._component_data
            group_opt = qsm_mya_stp_cfx_rig_core.CfxGroup()
            data = group_opt.generate_component_data()
            if data != data_pre or force is True:
                self._component_data = data
                self._qt_tree_widget._view_model.restore()
                for i_key, i_value in self._component_data.items():
                    self._gui_add_auto(i_key, i_value)
        else:
            self._qt_tree_widget._view_model.restore()

    def _gui_add_auto(self, key, value):
        _ = self._qt_tree_widget._view_model.find_item(key)
        if _:
            return False, _

        path_opt = bsc_core.BscNodePathOpt(key)

        ancestor_paths = path_opt.get_ancestor_paths()
        ancestor_paths.reverse()

        for i_path in ancestor_paths:
            i_flag, i_qt_item = self._qt_tree_widget._view_model.create_item(i_path)
            if i_flag is True:
                i_qt_item._item_model.set_icon_name('database/group')
                i_qt_item._item_model.set_expanded(True)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(key)

        node_type = qsm_mya_core.Node.get_type(value)

        qt_icon = gui_qt_core.QtMaya.generate_qt_icon_by_name(node_type)
        qt_item._item_model.set_icon(qt_icon)
        qt_item._item_model.set_expanded(True)
        qt_item._item_model.set_assign_data('node', value)

        visible = qsm_mya_core.NodeDisplay.is_visible(value)
        if visible is False:
            qt_item._item_model.set_status(
                qt_item._item_model.Status.Disable
            )


class PrxToolsetForCfxRigTool(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
    UNIT_KEY = 'cfx_rig'

    GUI_NODE_OPT_CLS = GuiNodeOptForCfxRigTool

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForCfxRigTool, self).__init__(*args, **kwargs)

        self._prx_options_node.set('template.create_template', self.on_create_template)

        # cloth
        self._prx_options_node.set(
            'cloth.add_to', self.on_add_to_cloth_geo_by_select
        )

        self._prx_options_node.set(
            'cloth.copy_as', self.on_copy_as_cloth_geo_by_select
        )
        
        # cloth proxy
        self._prx_options_node.set(
            'cloth_proxy.add_to', self.on_add_to_cloth_proxy_geo_by_select
        )

        self._prx_options_node.set(
            'cloth_proxy.copy_as', self.on_copy_as_cloth_proxy_geo_by_select
        )

        # appendix
        self._prx_options_node.set(
            'appendix.add_to', self.on_add_to_appendix_geo_by_select
        )

        self._prx_options_node.set(
            'appendix.copy_as', self.on_copy_as_appendix_geo_by_select
        )

        # collider
        self._prx_options_node.set(
            'collider.add_to', self.on_add_to_collider_geo_by_select
        )

        self._prx_options_node.set(
            'collider.copy_as', self.on_copy_as_collider_geo_by_select
        )

        # bridge
        self._prx_options_node.set(
            'bridge_geometry.add_to', self.on_add_to_bridge_geo_by_select
        )

        self._prx_options_node.set(
            'bridge_geometry.copy_as', self.on_copy_as_bridge_geo_by_select
        )

        self._prx_options_node.set(
            'bridge_control.copy_as', self.on_copy_as_bridge_control_by_select
        )

        # nucleus
        self._prx_options_node.set(
            'nucleus.create_ncloth', self.on_create_ncloth_by_select
        )

        self._prx_options_node.set(
            'nucleus.create_nrigid', self.on_create_nrigid_by_select
        )

        self._prx_options_node.set(
            'nucleus.paint_vertex_input_attract', self.on_paint_vertex_input_attract
        )

        # automation
        self._prx_options_node.set(
            'automation.auto_collection', self.on_auto_collection
        )
        self._prx_options_node.set(
            'automation.auto_name', self.on_auto_name
        )

        self._prx_options_node.set(
            'automation.rest_rig_controls_transformation', self.on_rest_rig_controls_transformation
        )

    def on_create_template(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.create_groups_for('cfx_rig')

    # bridge
    def on_add_to_bridge_geo_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.add_to_bridge_geo_by_select()

    def on_copy_as_bridge_geo_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.copy_as_bridge_geo_by_select(
                auto_blend=self._prx_options_node.get('bridge_geometry.auto_blend')
            )

    def on_copy_as_bridge_control_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.copy_as_bridge_control_by_select(
                auto_constrain=self._prx_options_node.get('bridge_control.auto_constrain')
            )

    # cloth
    def on_add_to_cloth_geo_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.add_to_cloth_geo_by_select()

    def on_copy_as_cloth_geo_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.copy_as_cloth_geo_by_select(
                auto_blend=self._prx_options_node.get('cloth.auto_blend')
            )

    # cloth proxy
    def on_add_to_cloth_proxy_geo_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.add_to_cloth_proxy_geo_by_select()

    def on_copy_as_cloth_proxy_geo_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.copy_as_cloth_proxy_geo_by_select(
                auto_blend=self._prx_options_node.get('cloth.auto_blend')
            )

    # collider
    def on_add_to_collider_geo_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.add_to_collider_geo_by_select()

    def on_copy_as_collider_geo_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.copy_as_collider_geo_by_select(
                auto_blend=self._prx_options_node.get('collider.auto_blend')
            )

    # appendix:
    def on_add_to_appendix_geo_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.add_to_appendix_geo_by_select()

    def on_copy_as_appendix_geo_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.copy_as_appendix_geo_by_select()

    # nucleus
    def on_create_ncloth_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.create_ncloth_by_select()

    def on_create_nrigid_by_select(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.create_nrigid_by_select()

    @staticmethod
    def on_paint_vertex_input_attract():
        # noinspection PyUnresolvedReferences
        qsm_mya_core.maya_mel.eval(
            'setNClothMapType("inputAttract","",1); artAttrNClothToolScript 3 inputAttract;'
        )

    # automation
    def on_auto_collection(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.auto_collection()

    def on_auto_name(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.auto_name()

    def on_rest_rig_controls_transformation(self):
        if self._task_tool_opt is not None:
            self._task_tool_opt.rest_rig_controls_transformation()
