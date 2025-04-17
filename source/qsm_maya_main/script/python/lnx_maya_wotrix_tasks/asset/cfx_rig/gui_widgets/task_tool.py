# coding:utf-8
import lxbasic.core as bsc_core

from lnx_wotrix.gui.abstracts import unit_for_task_tool as _abs_unit_for_task_tool

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.preset as qsm_mya_preset

from ..gui_operates import task_tool as _gui_task_tool_opt

from .. import dcc_core as _task_dcc_core


# cfx rig
class _PrxNodeView(_abs_unit_for_task_tool.AbsPrxNodeViewForTaskTool):
    def on_dcc_select_node(self):
        selected_items = self._qt_tree_widget._view_model.get_selected_items()
        if selected_items:
            list_ = []
            for i in selected_items:
                i_node = i._item_model.get_assign_data('dcc_node')
                if i_node:
                    list_.append(i_node)

            qsm_mya_core.Selection.set(list_)
        else:
            qsm_mya_core.Selection.clear()

    def __init__(self, *args, **kwargs):
        super(_PrxNodeView, self).__init__(*args, **kwargs)

        self._component_data = {}

        self._qt_tree_widget._view.item_select_changed.connect(
            self.on_dcc_select_node
        )
        self._qt_tree_widget._view_model.set_item_expand_record_enable(True)

    def do_gui_refresh_all(self, force=False):
        if self._unit._gui_task_tool_opt is not None:
            data_pre = self._component_data
            group_opt = _task_dcc_core.AssetCfxRigHandle()
            data = group_opt.generate_component_data()
            if data != data_pre or force is True:
                self._component_data = data
                self._qt_tree_widget._view_model.restore()
                for i_key, i_value in self._component_data.items():
                    self.gui_add_one(i_key, i_value)
        else:
            self._qt_tree_widget._view_model.restore()

    def gui_add_one(self, path, node):
        _ = self._qt_tree_widget._view_model.find_item(path)
        if _:
            return False, _

        path_opt = bsc_core.BscNodePathOpt(path)

        ancestor_paths = path_opt.get_ancestor_paths()
        ancestor_paths.reverse()

        for i_path in ancestor_paths:
            i_flag, i_qt_item = self._qt_tree_widget._view_model.create_item(i_path)
            if i_flag is True:
                i_qt_item._item_model.set_icon_name('database/group')
                i_qt_item._item_model.set_expanded(True)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)

        node_type = qsm_mya_core.Node.get_type(node)

        qt_icon = gui_qt_core.QtMaya.generate_qt_icon_by_name(node_type)
        qt_item._item_model.set_icon(qt_icon)
        qt_item._item_model.set_expanded(True)
        qt_item._item_model.set_assign_data('dcc_node', node)

        visible = qsm_mya_core.NodeDisplay.is_visible(node)
        if visible is False:
            qt_item._item_model.set_status(
                qt_item._item_model.Status.Disable
            )


class _PrxBasicToolset(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
    GUI_KEY = 'basic'

    def __init__(self, *args, **kwargs):
        super(_PrxBasicToolset, self).__init__(*args, **kwargs)

        self._prx_options_node.set('template.create_groups', self.on_create_groups)

        # cloth
        self._prx_options_node.set(
            'cloth.add_to', self.on_add_to_cloth_geo_by_selection
        )

        self._prx_options_node.set(
            'cloth.copy_as', self.on_copy_as_cloth_geo_by_selection
        )

        # cloth proxy
        self._prx_options_node.set(
            'cloth_proxy.add_to', self.on_add_to_cloth_proxy_geo_by_selection
        )

        self._prx_options_node.set(
            'cloth_proxy.copy_as', self.on_copy_as_cloth_proxy_geo_by_selection
        )

        # appendix
        self._prx_options_node.set(
            'appendix.add_to', self.on_add_to_appendix_geo_by_selection
        )

        self._prx_options_node.set(
            'appendix.copy_as', self.on_copy_as_appendix_geo_by_selection
        )

        # collider
        self._prx_options_node.set(
            'collider.add_to', self.on_add_to_collider_geo_by_selection
        )

        self._prx_options_node.set(
            'collider.copy_as', self.on_copy_as_collider_geo_by_selection
        )

        # bridge
        self._prx_options_node.set(
            'bridge_geometry.add_to', self.on_add_to_bridge_geo_by_selection
        )

        self._prx_options_node.set(
            'bridge_geometry.copy_as', self.on_copy_as_bridge_geo_by_selection
        )

        self._prx_options_node.set(
            'bridge_control.copy_as', self.on_copy_as_bridge_control_by_selection
        )

        # nucleus
        self._prx_options_node.set(
            'nucleus.create_ncloth', self.on_create_ncloth_by_selection
        )

        self._prx_options_node.get_port('nucleus.create_ncloth').set_menu_content(
            qsm_mya_preset.NodePreset.generate_menu_content(
                'nCloth',
                key_excludes=[
                    'displayColor', 'inputMeshAttract', 'inputAttractMethod', 'inputAttractMapType'
                ]
            )
        )

        self._prx_options_node.set(
            'nucleus.create_nrigid', self.on_create_nrigid_by_selection
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
            'automation.auto_connection', self.on_auto_connection
        )

        self._prx_options_node.set(
            'automation.rest_rig_controls_transformation', self.on_rest_rig_controls_transformation
        )

        self._prx_options_node.set(
            'automation.auto_color', self.on_auto_color
        )

    def on_create_groups(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.create_groups_for('cfx_rig')

    # bridge
    def on_add_to_bridge_geo_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.add_to_bridge_geo_by_selection()

    def on_copy_as_bridge_geo_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.copy_as_bridge_geo_by_selection(
                auto_blend=self._prx_options_node.get('bridge_geometry.auto_blend')
            )

    def on_copy_as_bridge_control_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.copy_as_bridge_control_by_selection(
                auto_constrain=self._prx_options_node.get('bridge_control.auto_constrain')
            )

    # cloth
    def on_add_to_cloth_geo_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.add_to_cloth_geo_by_selection()

    def on_copy_as_cloth_geo_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.copy_as_cloth_geo_by_selection(
                auto_blend=self._prx_options_node.get('cloth.auto_blend')
            )

    # cloth proxy
    def on_add_to_cloth_proxy_geo_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.add_to_cloth_proxy_geo_by_selection()

    def on_copy_as_cloth_proxy_geo_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.copy_as_cloth_proxy_geo_by_selection(
                auto_blend=self._prx_options_node.get('cloth.auto_blend')
            )

    # collider
    def on_add_to_collider_geo_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.add_to_collider_geo_by_selection()

    def on_copy_as_collider_geo_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.copy_as_collider_geo_by_selection(
                auto_blend=self._prx_options_node.get('collider.auto_blend')
            )

    # appendix:
    def on_add_to_appendix_geo_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.add_to_appendix_geo_by_selection()

    def on_copy_as_appendix_geo_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.copy_as_appendix_geo_by_selection()

    # nucleus
    def on_create_ncloth_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.create_ncloth_by_selection()

    def on_create_nrigid_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.create_nrigid_by_selection()

    @staticmethod
    def on_paint_vertex_input_attract():
        # noinspection PyUnresolvedReferences
        qsm_mya_core.maya_mel.eval(
            'setNClothMapType("inputAttract","",1); artAttrNClothToolScript 3 inputAttract;'
        )

    # automation
    def on_auto_collection(self):
        if self._unit._gui_task_tool_opt is not None:
            result = self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._unit._configure.get('build.messages.auto_collection')
                ),
                status='warning'
            )
            if result is True:
                self._unit._gui_task_tool_opt.auto_collection()

    def on_auto_name(self):
        if self._unit._gui_task_tool_opt is not None:
            result = self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._unit._configure.get('build.messages.auto_name')
                ),
                status='warning'
            )
            if result is True:
                self._unit._gui_task_tool_opt.auto_name()

    def on_auto_connection(self):
        if self._unit._gui_task_tool_opt is not None:
            result = self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._unit._configure.get('build.messages.auto_connection')
                ),
                status='warning'
            )
            if result is True:
                self._unit._gui_task_tool_opt.auto_connection()

    def on_rest_rig_controls_transformation(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.rest_rig_controls_transformation()

    def on_auto_color(self):
        if self._unit._gui_task_tool_opt is not None:
            self._unit._gui_task_tool_opt.auto_color()


class _PrxExtraToolset(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
    GUI_KEY = 'extra'

    def __init__(self, *args, **kwargs):
        super(_PrxExtraToolset, self).__init__(*args, **kwargs)

        self._prx_options_node.set('rig_variant.mark', self.on_mark_rig_variant)

        self._prx_options_node.set('rig_preset.create_or_update', self.on_create_or_update_rig_preset)

        self._prx_options_node.set('rig_preset.load', self.on_load_rig_preset)

    @classmethod
    def on_mark_rig_variant(cls):
        options = _task_dcc_core.AssetCfxRigHandle.get_rig_variant_names()
        variant = _task_dcc_core.AssetCfxRigHandle.get_rig_variant_name()

        result = gui_core.GuiApplication.exec_input_dialog(
            type='choose',
            info='Entry Name for Variant...',
            options=options,
            value=variant,
            title='Mark Rig Variant'
        )
        if result:
            _task_dcc_core.AssetCfxRigHandle.mark_rig_variant(result)

    @classmethod
    def on_create_or_update_rig_preset(cls):
        options = _task_dcc_core.AssetCfxRigHandle.get_rig_preset_names()
        name = _task_dcc_core.AssetCfxRigHandle.get_rig_preset_name()

        result = gui_core.GuiApplication.exec_input_dialog(
            type='choose',
            info='Entry Name for Preset...',
            options=options,
            value=name,
            title='Mark Rig Preset'
        )
        if result:
            _task_dcc_core.AssetCfxRigHandle.create_or_update_rig_preset(result)

    @classmethod
    def on_load_rig_preset(cls):
        options = _task_dcc_core.AssetCfxRigHandle.get_rig_preset_names()
        name = _task_dcc_core.AssetCfxRigHandle.get_rig_preset_name()

        result = gui_core.GuiApplication.exec_input_dialog(
            type='choose',
            info='Entry Name for Preset...',
            options=options,
            value=name,
            title='Mark Rig Preset'
        )
        if result:
            _task_dcc_core.AssetCfxRigHandle.load_rig_preset(result)


class GuiTaskToolMain(_abs_unit_for_task_tool.AbsPrxUnitForTaskTool):
    GUI_KEY = 'cfx_rig'

    GUI_RESOURCE_VIEW_CLS = _PrxNodeView

    TOOLSET_CLASSES = [
        _PrxBasicToolset,
        _PrxExtraToolset
    ]

    TASK_TOOL_OPT_CLS = _gui_task_tool_opt.MayaAssetCfxRigToolOpt

    def __init__(self, *args, **kwargs):
        super(GuiTaskToolMain, self).__init__(*args, **kwargs)
