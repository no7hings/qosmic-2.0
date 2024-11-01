# coding:utf-8
import lxbasic.core as bsc_core

from qsm_lazy_tool.workspace.gui.abstracts import unit_for_task_tool as _abs_unit_for_task_tool

import lxgui.qt.core as gui_qt_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.steps.cfx.core as qsm_mya_stp_cfx_core


class GuiNodeOptForCfxRig(_abs_unit_for_task_tool.AbsGuiNodeOpt):
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
        super(GuiNodeOptForCfxRig, self).__init__(*args, **kwargs)

        self._component_data = {}

        self._qt_tree_widget._view.item_select_changed.connect(
            self.on_dcc_select_node
        )

    def do_gui_refresh_all(self, force=False):
        if self._page._task_worker is not None:
            data_pre = self._component_data
            group_opt = qsm_mya_stp_cfx_core.CfxGroup()
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


class PrxToolsetForCfxFig(_abs_unit_for_task_tool.AbsPrxToolset):
    UNIT_KEY = 'cfx_rig'

    GUI_NODE_OPT_CLS = GuiNodeOptForCfxRig

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForCfxFig, self).__init__(*args, **kwargs)

        self._prx_options_node.set('template.create_template', self.on_create_template)
        
        # bridge
        self._prx_options_node.set(
            'bridge_geometry.add_to', self.on_add_to_bridge_geometry_by_select
        )
        
        self._prx_options_node.set(
            'bridge_geometry.copy_as', self.on_copy_as_bridge_geometry_by_select
        )
        
        # cloth
        self._prx_options_node.set(
            'cloth.add_to', self.on_add_to_cloth_geometry_by_select
        )

        self._prx_options_node.set(
            'cloth.copy_as', self.on_copy_as_cloth_geometry_by_select
        )
        self._prx_options_node.set(
            'cloth.create_ncloth', self.on_create_ncloth_by_select
        )
        self._prx_options_node.set(
            'cloth.paint_vertex_input_attract', self.on_paint_vertex_input_attract
        )
        
        # collider
        self._prx_options_node.set(
            'collider.add_to', self.on_add_to_collider_geometry_by_select
        )

        self._prx_options_node.set(
            'collider.copy_as', self.on_copy_as_collider_geometry_by_select
        )
        self._prx_options_node.set(
            'collider.create_nrigid', self.on_create_nrigid_by_select
        )

        # appendix
        self._prx_options_node.set(
            'appendix.copy_as', self.on_copy_as_appendix_geometry_by_select
        )

    def on_create_template(self):
        if self._task_worker is not None:
            self._task_worker.create_groups_for('cfx_rig')

    # bridge
    def on_add_to_bridge_geometry_by_select(self):
        if self._task_worker is not None:
            self._task_worker.add_to_bridge_geometry_by_select()

    def on_copy_as_bridge_geometry_by_select(self):
        if self._task_worker is not None:
            self._task_worker.copy_as_bridge_geometry_by_select(
                auto_blend=self._prx_options_node.get('bridge_geometry.auto_blend')
            )

    # cloth
    def on_add_to_cloth_geometry_by_select(self):
        if self._task_worker is not None:
            self._task_worker.add_to_cloth_geometry_by_select()

    def on_copy_as_cloth_geometry_by_select(self):
        if self._task_worker is not None:
            self._task_worker.copy_as_cloth_geometry_by_select(
                auto_blend=self._prx_options_node.get('cloth.auto_blend')
            )

    def on_create_ncloth_by_select(self):
        if self._task_worker is not None:
            self._task_worker.create_ncloth_by_select()

    def on_paint_vertex_input_attract(self):
        # noinspection PyUnresolvedReferences
        qsm_mya_core.maya_mel.eval(
            'setNClothMapType("inputAttract","",1); artAttrNClothToolScript 3 inputAttract;'
        )

    # collider
    def on_add_to_collider_geometry_by_select(self):
        if self._task_worker is not None:
            self._task_worker.add_to_collider_geometry_by_select()

    def on_copy_as_collider_geometry_by_select(self):
        if self._task_worker is not None:
            self._task_worker.copy_as_collider_geometry_by_select(
                auto_blend=self._prx_options_node.get('collider.auto_blend')
            )

    def on_create_nrigid_by_select(self):
        if self._task_worker is not None:
            self._task_worker.create_nrigid_by_select()

    # appendix:
    def on_copy_as_appendix_geometry_by_select(self):
        if self._task_worker is not None:
            self._task_worker.copy_as_appendix_geometry_by_select()
