# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import qsm_maya.cfx.core as qsm_mya_cfx_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.general.core as qsm_mya_gnl_core

import qsm_maya.cfx.scripts as qsm_mya_cfx_scripts

import qsm_maya_gui.core as qsm_mya_gui_core


class UnitForCfxRigView(
    qsm_mya_gui_core.PrxUnitForResourceOpt
):
    ROOT_NAME = 'Rigs'

    NAMESPACE = 'rig'

    RESOURCES_QUERY_CLS = qsm_mya_cfx_core.CfxAdvRigsQuery

    CHECK_BOX_FLAG = True

    TOOL_INCLUDES = [
        'isolate-select',
        'reference',
    ]

    def __init__(self, window, unit, session, prx_tree_view):
        super(UnitForCfxRigView, self).__init__(window, unit, session, prx_tree_view)

    def gui_add_components(self, resource, prx_item):
        clothes, meshes = resource.find_all_cloth_export_args()
        if meshes:
            prx_item.set_icon_name('node/maya/reference-cfx')
            for i in meshes:
                self.gui_add_component(i, prx_item)


class ToolSetUnitForCfxRigExport(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    # cloth
    # export
    def do_dcc_export_cloth_cache_by_checked(self):
        resources = self._page._gui_resource_prx_unit.gui_get_checked_resources()
        if not resources:
            self._window.exec_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_resource')
                ),
                status='warning'
            )
            return

        with_alembic_cache = self._prx_options_node.get('cloth.with_alembic_cache')
        with_geometry_cache = self._prx_options_node.get('cloth.with_geometry_cache')

        if sum([with_alembic_cache, with_geometry_cache]) == 0:
            self._window.exec_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_cache_type')
                ),
                status='warning'
            )
            return

        directory_path = self._prx_options_node.get('cloth.version_directory')
        frame_range = self._frame_range_port.get()
        frame_step = self._prx_options_node.get('setting.frame_step')
        frame_offset = self._prx_options_node.get('setting.frame_offset')

        for i_resource in resources:
            i_opt = qsm_mya_cfx_scripts.NClothCacheOpt(i_resource)
            i_opt.do_export(
                directory_path, frame_range, frame_step, frame_offset,
                with_alembic_cache=with_alembic_cache, with_geometry_cache=with_geometry_cache
                )

        self.do_gui_update_version_directory_by_version_scheme_changing()

    # settings
    def do_dcc_refresh_by_fps_changing(self):
        pass

    def do_gui_refresh_by_fps_changing(self):
        fps = qsm_mya_core.Frame.get_fps()
        self._fps_port.set(fps)

    def do_gui_refresh_by_frame_scheme_changing(self):
        frame_scheme = self.gui_get_frame_scheme()
        if frame_scheme == 'frame_range':
            self._frame_range_port.set_locked(False)
        else:
            self._frame_range_port.set_locked(True)
            self.do_gui_refresh_by_dcc_frame_changing()

    def do_gui_refresh_by_dcc_frame_changing(self):
        frame_scheme = self.gui_get_frame_scheme()
        if frame_scheme == 'time_slider':
            frame_range = qsm_mya_core.Frame.get_frame_range()
            self._frame_range_port.set(frame_range)

    def do_gui_update_version_directory_by_version_scheme_changing(self):
        directory_path = self._prx_options_node.get('cloth.directory')
        version_scheme = self._prx_options_node.get('cloth.version_scheme')

        options = dict(
            directory=directory_path,
            scene=bsc_storage.StgFileOpt(qsm_mya_core.SceneFile.get_current()).get_name_base()
        )

        if version_scheme == 'no_version':
            version_directory_ptn = '{directory}/{scene}'
            version_directory_path = version_directory_ptn.format(**options)
        elif version_scheme == 'new_version':
            version_directory_ptn = '{directory}/{scene}.v{{version}}'.format(
                **options
            )
            version_directory_path = bsc_core.PtnVersionPath.generate_as_new_version(version_directory_ptn)
        elif version_scheme == 'specified_version':
            version_directory_ptn = '{directory}/{scene}.v{{version}}'.format(
                **options
            )
            options['version'] = str(self._prx_options_node.get('cloth.specified_version')).zfill(3)
            version_directory_path = version_directory_ptn.format(**options)
        else:
            raise RuntimeError()

        self._prx_options_node.set(
            'cloth.version_directory', version_directory_path
        )

    def __init__(self, window, unit, session):
        super(ToolSetUnitForCfxRigExport, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.unit.export.options')
            )
        )
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.unit.export.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='export',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.unit.export')
            ),
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.main.unit.export')
            )
        )
        self._prx_options_node.get_port('setting.frame_scheme').connect_input_changed_to(
            self.do_gui_refresh_by_frame_scheme_changing
        )

        self._fps_port = self._prx_options_node.get_port('setting.fps')
        self._frame_range_port = self._prx_options_node.get_port('setting.frame_range')

        self.do_gui_update_version_directory_by_version_scheme_changing()

        self._prx_options_node.get_port('cloth.version_scheme').connect_input_changed_to(
            self.do_gui_update_version_directory_by_version_scheme_changing
        )
        self._prx_options_node.get_port('cloth.specified_version').connect_input_changed_to(
            self.do_gui_update_version_directory_by_version_scheme_changing
        )

        self._cloth_export_button = self._prx_options_node.get_port('cloth.export_cfx_cloth_use_localhost')
        self._cloth_export_button.set(
            self.do_dcc_export_cloth_cache_by_checked
        )

        self.do_gui_refresh_by_fps_changing()
        self.do_gui_refresh_by_dcc_frame_changing()

    def gui_get_frame_scheme(self):
        return self._prx_options_node.get('setting.frame_scheme')


class ToolSetUnitForCfxRigImport(
    qsm_mya_gui_core.PrxUnitBaseOpt
):

    CACHE_PATTERN = '{directory}'

    def do_gui_refresh_by_version_directory_changing(self):
        directory_path = self._prx_options_node.get(
            'cloth.version_directory'
        )
        if not directory_path:
            return

        pot = self._prx_options_node.get_port('cloth.file_tree')
        pot.set_root(directory_path)

        ptn = qsm_mya_gnl_core.FilePatterns.CfxClothAbcFile
        ptn_opt = bsc_core.BscStgParseOpt(
            ptn
        )
        ptn_opt.update_variants(directory=directory_path)
        abc_paths = ptn_opt.get_match_results()
        pot.set(abc_paths)

    def do_dcc_import_cloth_cache_by_checked(self):
        directory_path = self._prx_options_node.get(
            'cloth.version_directory'
        )
        if not directory_path:
            return

        pot = self._prx_options_node.get_port('cloth.file_tree')

        resources_query = self._page._gui_resource_prx_unit.get_resources_query()

        cache_paths = pot.get_all(check_only=True)
        if cache_paths:
            ptn = qsm_mya_gnl_core.FilePatterns.CfxClothAbcFile
            ptn_opt = bsc_core.BscStgParseOpt(
                ptn
            )
            for i_cache_path in cache_paths:
                if ptn_opt.get_is_matched(i_cache_path) is True:
                    i_properties = ptn_opt.get_variants(i_cache_path)
                    i_resource = resources_query.get(i_properties['namespace'])
                    if i_resource:
                        i_resource_opt = qsm_mya_cfx_scripts.NClothCacheOpt(i_resource)
                        i_resource_opt.do_import_abc(i_cache_path)

    def __init__(self, window, unit, session):
        super(ToolSetUnitForCfxRigImport, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.unit.import.options')
            )
        )
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.unit.import.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='import',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.unit.import')
            ),
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.main.unit.import')
            )
        )

        self._prx_options_node.get_port(
            'cloth.version_directory'
        ).connect_input_changed_to(
            self.do_gui_refresh_by_version_directory_changing
        )

        self._prx_options_node.set(
            'cloth.import_cfx_cloth',
            self.do_dcc_import_cloth_cache_by_checked
        )