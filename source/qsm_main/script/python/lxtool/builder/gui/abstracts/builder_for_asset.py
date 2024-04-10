# coding:utf-8
# gui
import lxgui.proxy.core as gui_prx_core

import lxgui.proxy.widgets as prx_widgets


class AbsPnlBuilderForAsset(prx_widgets.PrxSessionToolWindow):
    CONFIGURE_FILE_PATH = 'utility/panel/asset-builder'

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlBuilderForAsset, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._hook_build_configure = self._session.configure.get_as_content('build')
        self._set_group_0_build_()

    def _set_tool_panel_setup_(self):
        self.refresh_all_fnc()

    def _set_group_0_build_(self):
        self._options_prx_node = prx_widgets.PrxNode('options')
        self.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._hook_build_configure.get('node.options')
        )
        #
        _port = self._options_prx_node.get_port('project')
        histories = _port.get_histories()
        if histories:
            _port.set(histories[-1])
        #
        current_project = self._get_current_project_()
        if current_project:
            if current_project in _port.get_histories():
                _port.set(
                    current_project
                )
        #
        self._options_prx_node.set('refresh', self.refresh_all_fnc)
        self._options_prx_node.set('check_all', self._set_check_all_)
        self._options_prx_node.set('check_clear', self._set_check_clear_)
        self._options_prx_node.set('build', self._set_build_run_)

    @classmethod
    def _get_current_project_(cls):
        import os

        _ = os.environ.get('PG_SHOW')
        if _:
            return _.lower()

    def _set_assets_(self):
        import lxresolver.core as rsv_core

        project = self._options_prx_node.get_port('project').get()
        resolver = rsv_core.RsvBase.generate_root()
        rsv_project = resolver.get_rsv_project(project=project)
        rsv_assets = rsv_project.get_rsv_resources(branch='asset')
        assets = [
            i.name for i in rsv_assets
        ]
        self._options_prx_node.set(
            'asset', rsv_assets
        )

    def _set_check_all_(self):
        for i in self._options_prx_node.get_port('build_options').get_children():
            i.set(True)

    def _set_check_clear_(self):
        for i in self._options_prx_node.get_port('build_options').get_children():
            i.set(False)

    @gui_prx_core.GuiProxyModifier.window_proxy_waiting
    def refresh_all_fnc(self):
        self._set_assets_()

    @gui_prx_core.GuiProxyModifier.window_proxy_waiting
    def _set_build_run_(self):
        pass
